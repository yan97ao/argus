#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""配置管理模块 - 加载和验证 Argus 配置文件

该模块负责从 config.yaml 加载配置，如果配置文件不存在则使用默认值。
"""

import os
import logging
from typing import Dict, Any, Optional

try:
    import yaml
except ImportError:
    yaml = None

logger = logging.getLogger(__name__)

# 默认配置
DEFAULT_CONFIG = {
    "importance": {
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
            "other": 3,
        },
        "change_sizes": {
            "large": 500,
            "medium": 100,
            "small": 50,
        },
        "file_types": {
            "core": 2,
            "config": 1,
            "test": 1,
            "doc": 0,
        },
        "scopes": {
            "wide": 5,
            "medium": 3,
        },
        "thresholds": {
            "high": 10,
            "medium": 6,
        },
    },
    "rate_limit": {
        "delays": {
            "fast": 5,
            "normal": 10,
            "slow": 15,
        },
        "backoff": {
            "initial": 10,
            "max": 30,
            "multiplier": 1,
        },
        "retry": {
            "max_attempts": 3,
        },
    },
    "format": {
        "enable_toc": True,
        "enable_grouping": True,
        "enable_stats": True,
        "diff": {
            "truncate_threshold": 50000,
            "truncate_to": 50000,
        },
    },
    "llm": {
        "force_level": None,
        "timeout": 30,
        "max_tokens": 2048,
    },
}


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """加载配置文件

    Args:
        config_path: 配置文件路径，默认为项目根目录的 config.yaml

    Returns:
        dict: 配置字典，如果配置文件不存在或加载失败则返回默认配置
    """
    # 确定配置文件路径
    if config_path is None:
        # 从当前文件位置推导项目根目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        config_path = os.path.join(project_root, "config.yaml")

    # 检查文件是否存在
    if not os.path.exists(config_path):
        logger.info(f"配置文件不存在: {config_path}，使用默认配置")
        return DEFAULT_CONFIG.copy()

    # 检查 yaml 模块是否可用
    if yaml is None:
        logger.warning("PyYAML 未安装，无法加载配置文件，使用默认配置")
        logger.warning("安装命令: pip install pyyaml")
        return DEFAULT_CONFIG.copy()

    # 加载配置文件
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            user_config = yaml.safe_load(f)

        if user_config is None:
            logger.warning(f"配置文件为空: {config_path}，使用默认配置")
            return DEFAULT_CONFIG.copy()

        # 合并配置（用户配置覆盖默认配置）
        config = _merge_config(DEFAULT_CONFIG, user_config)

        # 验证配置
        config = _validate_config(config)

        logger.info(f"成功加载配置文件: {config_path}")
        return config

    except Exception as e:
        logger.error(f"加载配置文件失败: {e}，使用默认配置")
        return DEFAULT_CONFIG.copy()


def _merge_config(default: Dict, user: Dict) -> Dict:
    """递归合并配置（用户配置覆盖默认配置）

    Args:
        default: 默认配置
        user: 用户配置

    Returns:
        dict: 合并后的配置
    """
    result = default.copy()

    for key, value in user.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # 递归合并嵌套字典
            result[key] = _merge_config(result[key], value)
        else:
            # 用户配置覆盖默认配置
            result[key] = value

    return result


def _validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """验证配置的有效性

    Args:
        config: 配置字典

    Returns:
        dict: 验证后的配置（修正无效值）
    """
    # 验证 importance 配置
    if "importance" in config:
        importance = config["importance"]

        # 确保所有必需的键都存在
        if "commit_types" not in importance:
            importance["commit_types"] = DEFAULT_CONFIG["importance"]["commit_types"]
        if "thresholds" not in importance:
            importance["thresholds"] = DEFAULT_CONFIG["importance"]["thresholds"]

        # 验证阈值合理性
        thresholds = importance["thresholds"]
        if thresholds["high"] <= thresholds["medium"]:
            logger.warning("配置警告: high 阈值应大于 medium 阈值")

    # 验证 rate_limit 配置
    if "rate_limit" in config:
        rate_limit = config["rate_limit"]

        # 确保延迟值为正数
        if "delays" in rate_limit:
            for key in ["fast", "normal", "slow"]:
                if rate_limit["delays"].get(key, 0) < 0:
                    rate_limit["delays"][key] = DEFAULT_CONFIG["rate_limit"]["delays"][key]
                    logger.warning(f"配置警告: rate_limit.delays.{key} 必须为正数，已使用默认值")

        # 验证重试次数
        if "retry" in rate_limit:
            max_attempts = rate_limit["retry"].get("max_attempts", 3)
            if max_attempts < 1:
                rate_limit["retry"]["max_attempts"] = 1
                logger.warning("配置警告: max_attempts 必须 >= 1")

    # 验证 format 配置
    if "format" in config:
        fmt = config["format"]

        # 确保布尔值正确
        for key in ["enable_toc", "enable_grouping", "enable_stats"]:
            if key in fmt and not isinstance(fmt[key], bool):
                logger.warning(f"配置警告: format.{key} 必须为布尔值，已设置为 True")
                fmt[key] = True

    # 验证 llm 配置
    if "llm" in config:
        llm_cfg = config["llm"]

        # 验证 force_level
        if "force_level" in llm_cfg:
            valid_levels = [None, "low", "medium", "high"]
            if llm_cfg["force_level"] not in valid_levels:
                logger.warning(f"配置警告: llm.force_level 必须为 low/medium/high 或 null")
                llm_cfg["force_level"] = None

    return config


def get_importance_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """获取重要性评分相关配置

    Args:
        config: 完整配置字典

    Returns:
        dict: 重要性评分配置
    """
    return config.get("importance", DEFAULT_CONFIG["importance"])


def get_rate_limit_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """获取速率限制相关配置

    Args:
        config: 完整配置字典

    Returns:
        dict: 速率限制配置
    """
    return config.get("rate_limit", DEFAULT_CONFIG["rate_limit"])


def get_format_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """获取格式化相关配置

    Args:
        config: 完整配置字典

    Returns:
        dict: 格式化配置
    """
    return config.get("format", DEFAULT_CONFIG["format"])


def get_llm_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """获取 LLM 相关配置

    Args:
        config: 完整配置字典

    Returns:
        dict: LLM 配置
    """
    return config.get("llm", DEFAULT_CONFIG["llm"])
