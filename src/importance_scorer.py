#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""重要性评分模块 - 根据多个因素评估提交的重要性

该模块提供基于规则的重要性评分模型，考虑提交类型、变更规模、
文件类型和影响范围等因素，将提交分为高、中、低三个重要等级。
"""

import re
import logging
from typing import Dict, List, Optional

# 默认配置
DEFAULT_CONFIG = {
    "commit_types": {
        "feat": 8,
        "fix": 7,
        "perf": 6,
        "refactor": 5,
        "test": 3,
        "docs": 2,
        "ci": 2,
        "chore": 1,
        "style": 1,
        "build": 1,
    },
    "change_sizes": {
        "large": 500,      # >500 行
        "medium": 100,     # 100-500 行
        "small": 50,       # 50-100 行
    },
    "file_types": {
        "core": [".py", ".rs", ".cpp", ".cc", ".c", ".h", ".hpp", ".go", ".js", ".ts"],
        "config": [".yaml", ".yml", ".json", ".toml", ".ini", ".cfg", ".conf"],
        "test": ["_test.py", "test_.py", "_test.rs", "_test.go"],
        "doc": [".md", ".rst", ".txt", "adoc"],
    },
    "scopes": {
        "wide": 5,         # >5 个文件
        "medium": 3,       # 3-5 个文件
    },
    "thresholds": {
        "high": 10,        # score >= 10
        "medium": 6,       # 6 <= score < 10
    }
}

logger = logging.getLogger(__name__)


def get_commit_type(message: str) -> str:
    """解析 Conventional Commits 前缀

    Args:
        message: 完整的 commit message

    Returns:
        提交类型 (feat, fix, docs 等)，如果没有前缀则返回 "other"
    """
    if not message:
        return "other"

    # 提取第一行
    first_line = message.split('\n')[0].strip()

    # 匹配 Conventional Commits 格式: type: 或 type(scope):
    match = re.match(r'^([a-z]+)(\(.+\))?:', first_line)
    if match:
        commit_type = match.group(1)
        logger.debug(f"解析到提交类型: {commit_type}")
        return commit_type

    logger.debug(f"未检测到 Conventional Commits 前缀，返回 'other'")
    return "other"


def get_primary_file_type(files: List) -> str:
    """判断主要文件类型

    Args:
        files: 文件对象列表 (需要有 filename 属性)

    Returns:
        文件类型类别: "core", "config", "test", "doc"
    """
    if not files:
        return "core"

    type_counts = {"core": 0, "config": 0, "test": 0, "doc": 0}

    for file in files:
        filename = getattr(file, 'filename', '')
        if not filename:
            continue

        # 检测核心代码文件
        for ext in DEFAULT_CONFIG["file_types"]["core"]:
            if filename.endswith(ext):
                type_counts["core"] += 1
                break
        else:
            # 检测配置文件
            for ext in DEFAULT_CONFIG["file_types"]["config"]:
                if filename.endswith(ext):
                    type_counts["config"] += 1
                    break
            else:
                # 检测测试文件
                for pattern in DEFAULT_CONFIG["file_types"]["test"]:
                    if pattern in filename:
                        type_counts["test"] += 1
                        break
                else:
                    # 检测文档文件
                    for ext in DEFAULT_CONFIG["file_types"]["doc"]:
                        if filename.endswith(ext):
                            type_counts["doc"] += 1
                            break

    # 返回数量最多的类型
    primary_type = max(type_counts.items(), key=lambda x: x[1])[0]
    logger.debug(f"主要文件类型: {primary_type}, 分布: {type_counts}")
    return primary_type


def classify_change_size(additions: int, deletions: int) -> str:
    """分类变更规模

    Args:
        additions: 新增行数
        deletions: 删除行数

    Returns:
        规模类别: "large", "medium", "small", "tiny"
    """
    total_changes = additions + deletions

    if total_changes > DEFAULT_CONFIG["change_sizes"]["large"]:
        return "large"
    elif total_changes > DEFAULT_CONFIG["change_sizes"]["medium"]:
        return "medium"
    elif total_changes > DEFAULT_CONFIG["change_sizes"]["small"]:
        return "small"
    else:
        return "tiny"


def calculate_importance_score(commit, repo_info: Optional[Dict] = None, config: Optional[Dict] = None) -> Dict:
    """计算提交重要性分数

    Args:
        commit: GitHub commit 对象
        repo_info: 仓库信息字典 (可选)
        config: 自定义配置 (可选)

    Returns:
        包含 score, level, details 的字典:
        {
            'score': int,           # 总分数
            'level': str,           # 'high' | 'medium' | 'low'
            'details': {            # 详细评分
                'type_weight': int,
                'size_weight': int,
                'file_type_weight': int,
                'scope_weight': int,
                'commit_type': str,
                'change_size': str,
                'primary_file_type': str,
            }
        }
    """
    # 使用自定义配置或默认配置
    cfg = config if config else DEFAULT_CONFIG
    thresholds = cfg.get("thresholds", DEFAULT_CONFIG["thresholds"])

    # 1. 提交类型权重
    commit_type = get_commit_type(commit.commit.message)
    type_weight = cfg["commit_types"].get(commit_type, 3)  # 默认中等权重

    # 2. 变更规模权重
    additions = commit.stats.additions if hasattr(commit, 'stats') else 0
    deletions = commit.stats.deletions if hasattr(commit, 'stats') else 0
    change_size = classify_change_size(additions, deletions)

    size_weights = {"large": 3, "medium": 2, "small": 1, "tiny": 0}
    size_weight = size_weights.get(change_size, 0)

    # 3. 文件类型权重
    files = commit.files if hasattr(commit, 'files') else []
    primary_file_type = get_primary_file_type(files)
    file_type_weights = {"core": 2, "config": 1, "test": 1, "doc": 0}
    file_type_weight = file_type_weights.get(primary_file_type, 0)

    # 4. 影响范围权重
    file_count = len(files)
    if file_count > cfg["scopes"]["wide"]:
        scope_weight = 2
    elif file_count >= cfg["scopes"]["medium"]:
        scope_weight = 1
    else:
        scope_weight = 0

    # 计算总分
    total_score = type_weight + size_weight + file_type_weight + scope_weight

    # 映射到重要等级
    if total_score >= thresholds["high"]:
        level = "high"
    elif total_score >= thresholds["medium"]:
        level = "medium"
    else:
        level = "low"

    result = {
        'score': total_score,
        'level': level,
        'details': {
            'type_weight': type_weight,
            'size_weight': size_weight,
            'file_type_weight': file_type_weight,
            'scope_weight': scope_weight,
            'commit_type': commit_type,
            'change_size': change_size,
            'primary_file_type': primary_file_type,
        }
    }

    logger.info(f"提交 {commit.sha[:7]} 重要性评分: {total_score} ({level})")
    logger.debug(f"详细信息: {result['details']}")

    return result


def get_importance_emoji(level: str) -> str:
    """获取重要等级对应的 emoji

    Args:
        level: 'high', 'medium', 或 'low'

    Returns:
        emoji 字符串
    """
    emojis = {
        "high": "🔴",
        "medium": "🟡",
        "low": "🟢"
    }
    return emojis.get(level, "⚪")


def get_importance_label(level: str) -> str:
    """获取重要等级的中文标签

    Args:
        level: 'high', 'medium', 或 'low'

    Returns:
        中文标签 ('高', '中', '低')
    """
    labels = {
        "high": "高",
        "medium": "中",
        "low": "低"
    }
    return labels.get(level, "未知")
