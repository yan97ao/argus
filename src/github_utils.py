#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pytz
from github import Github
from github.Commit import Commit
from github.GithubException import GithubException

TIME_ZONE = pytz.timezone('Asia/Shanghai')

# 存储已使用的锚点，用于检测重复
_used_anchors: Dict[str, List[str]] = {}

def init_github_client(token=None):
    """初始化GitHub客户端
    
    Args:
        token: GitHub个人访问令牌
        
    Returns:
        Github: GitHub客户端实例
    """
    try:
        # 优先使用传入的token
        if token:
            g = Github(token)
        # 其次使用环境变量中的token
        elif os.getenv('GITHUB_TOKEN'):
            g = Github(os.getenv('GITHUB_TOKEN'))
        # 最后使用无认证方式
        else:
            g = Github()
            
        # 测试API连接
        rate_limit = g.get_rate_limit()
        logging.debug(f"API速率限制: {rate_limit.core.limit}, 剩余: {rate_limit.core.remaining}")
        return g
    except Exception as e:
        logging.error(f"初始化GitHub客户端失败: {str(e)}")
        return None

def get_repository(github_client, repo_name=None):
    """获取GitHub仓库
    
    Args:
        github_client: GitHub客户端实例
        repo_name: 仓库名称，格式为"owner/repo"
        
    Returns:
        Repository: GitHub仓库实例
    """
    try:
        if repo_name:
            return github_client.get_repo(repo_name)
        else:
            # 优先使用 Action 传入的环境变量
            repo_name = os.getenv('GITHUB_REPOSITORY_NAME') or os.getenv('GITHUB_REPOSITORY')
            if not repo_name:
                logging.error("错误: 未指定仓库名称，请使用参数或确保在 GitHub Actions 环境中运行")
                return None
            return github_client.get_repo(repo_name)
    except GithubException as e:
        logging.error(f"获取仓库失败: {e.status} {e.data.get('message')}")
        return None
    except Exception as e:
        logging.error(f"获取仓库出错: {str(e)}")
        return None

def get_commits_lastday(repo):
    """获取最近一天的提交
    
    Args:
        repo: GitHub仓库实例
        
    Returns:
        list: 提交对象列表
    """
    # 获取北京时间的昨天日期
    yesterday = datetime.now(TIME_ZONE) - timedelta(days=1)
    
    # 计算北京时间的开始和结束
    since = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    until = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    # 将时间转换为UTC
    since_utc = since.astimezone(pytz.UTC)
    until_utc = until.astimezone(pytz.UTC)
    
    logging.info(f"获取 {repo.full_name} 提交从 {since_utc} (UTC) 到 {until_utc} (UTC)")
    try:
        paged_commits = repo.get_commits(since=since_utc, until=until_utc)
        commits = [c for c in paged_commits]
        return commits
    except GithubException as e:
        logging.error(f"获取 {repo.full_name} 提交失败: {e.status} {e.data.get('message')}")
    except Exception as e:
        logging.error(f"获取 {repo.full_name} 提交出错: {str(e)}")
    return []

def format_commit_time(commit_time):
    """格式化提交时间为北京时间
    
    Args:
        commit_time: 提交时间
        
    Returns:
        str: 格式化后的时间字符串
    """
    if commit_time.tzinfo is None:
        # 如果时间没有时区信息，假设是UTC时间
        commit_time = commit_time.replace(tzinfo=pytz.UTC)
    # 转换为北京时间
    beijing_time = commit_time.astimezone(TIME_ZONE)
    return beijing_time.strftime('%Y-%m-%d %H:%M:%S')

def format_commit_message(message):
    """格式化提交信息，处理多行和特殊字符
    
    Args:
        message: 原始提交信息
        
    Returns:
        str: 格式化后的提交信息
    """
    # 过滤掉空行，转义表格分隔符
    filtered_lines = []
    for line in message.split('\n'):
        if line.strip():
            # 过滤掉签名和共同作者行
            if line.startswith('Signed-off-by') or line.startswith('Co-authored-by'):
                continue
            # 转义竖线以避免破坏表格结构
            filtered_lines.append(line.replace('|', '\\|'))
    
    # 使用HTML的<br>标签连接多行
    return "<br>".join(filtered_lines)

def create_commit_report(commits):
    """创建提交报告
    
    Args:
        commits_data: 字典，键为仓库名，值为提交列表
        
    Returns:
        str: Markdown格式的提交报告
    """
    content = ""
    content += "| 提交时间 | 作者 | 提交信息 |\n"
    content += "|----------|------|----------|\n"
    
    for commit in commits:
        commit_time = format_commit_time(commit.commit.author.date)
        author_name = commit.commit.author.name
        formatted_message = format_commit_message(commit.commit.message)
        content += f"| {commit_time} | {author_name} | {formatted_message} |\n"
    
    content += "\n"
    
    return content

def get_report_file_path(repo_name, date):
    """生成报告文件路径

    Args:
        repo_name: 仓库名称，格式为"owner/repo"，将提取最后一部分作为目录名
        date: 日期字符串，格式为"YYYY-MM-DD"

    Returns:
        str: 报告文件路径，格式为"reports/YYYY/repo-name/YYYY-MM-DD.md"
    """
    # 提取仓库名称的最后一部分（如 "vllm-project/vllm" -> "vllm"）
    repo_short_name = repo_name.split('/')[-1]

    # 从日期字符串中提取年份
    year = date.split('-')[0]

    # 构建文件路径
    file_path = f"reports/{year}/{repo_short_name}/{date}.md"
    return file_path


def create_report_file(repo, file_path, content):
    """创建报告文件并提交到仓库

    Args:
        repo: GitHub仓库实例
        file_path: 文件路径，格式为"reports/YYYY/repo-name/YYYY-MM-DD.md"
        content: 文件内容（Markdown格式）

    Returns:
        bool: 成功返回True，失败返回False
    """
    try:
        # 提取日期和仓库名用于 commit 消息
        parts = file_path.split('/')
        date = parts[-1].replace('.md', '')
        repo_name = parts[-2]

        commit_message = f"Report: {repo_name} - {date}"

        # 创建文件并提交
        repo.create_file(
            path=file_path,
            message=commit_message,
            content=content,
            branch="master"
        )
        logging.info(f"成功创建报告文件: {file_path}")
        return True
    except GithubException as e:
        error_msg = f"创建报告文件失败: {e.status}"
        if hasattr(e, 'data') and e.data:
            if isinstance(e.data, dict):
                error_msg += f" {e.data.get('message', '')}"
                if 'errors' in e.data:
                    for error in e.data['errors']:
                        if isinstance(error, dict):
                            error_msg += f"\n  - {error.get('field', 'unknown')}: {error.get('message', error.get('code', 'unknown error'))}"
                        else:
                            error_msg += f"\n  - {error}"
            else:
                error_msg += f" {e.data}"
        logging.error(error_msg)
    except Exception as e:
        logging.error(f"创建报告文件出错: {str(e)}")
    return False


def create_issue(repo, title, body):
    """创建issue

    Args:
        repo: GitHub仓库实例
        title: issue标题
        body: issue内容

    Returns:
        Issue: 创建的issue实例，如果失败则返回None
    """
    try:
        issue = repo.create_issue(title=title, body=body)
        logging.info(f"成功创建issue: #{issue.number}")
        return issue
    except GithubException as e:
        error_msg = f"创建issue失败: {e.status}"
        if hasattr(e, 'data') and e.data:
            if isinstance(e.data, dict):
                error_msg += f" {e.data.get('message', '')}"
                if 'errors' in e.data:
                    for error in e.data['errors']:
                        if isinstance(error, dict):
                            error_msg += f"\n  - {error.get('field', 'unknown')}: {error.get('message', error.get('code', 'unknown error'))}"
                        else:
                            error_msg += f"\n  - {error}"
            else:
                error_msg += f" {e.data}"
        logging.error(error_msg)
    except Exception as e:
        logging.error(f"创建issue出错: {str(e)}")
    return None


# ============================================================================
# 报告格式增强函数
# ============================================================================

def sanitize_commit_title(message: str, sha: str = "") -> Tuple[str, str]:
    """清理 commit message 标题以用作 Markdown 锚点

    Args:
        message: 完整的 commit message
        sha: commit SHA（用于生成唯一锚点）

    Returns:
        (sanitized_title, anchor_id): 清理后的标题和锚点ID
    """
    if not message:
        message = "无标题提交"

    # 提取第一行作为标题
    title = message.split('\n')[0].strip()

    # 限制最大长度（80字符）
    if len(title) > 80:
        title = title[:77] + "..."

    # 清理特殊字符
    # 移除或替换：# @ [ ] ( ) 等特殊字符
    # 保留：字母、数字、常见标点（. , - _ : 等）
    sanitized = re.sub(r'[#@()[\]{}]', '', title)
    sanitized = re.sub(r'\s+', '-', sanitized)  # 空格替换为连字符

    # 生成锚点ID（转换为小写，移除特殊字符）
    anchor_id = re.sub(r'[^\w\u4e00-\u9fff-]', '-', sanitized.lower())
    anchor_id = re.sub(r'-+', '-', anchor_id).strip('-')

    # 如果锚点为空或太短，使用SHA
    if not anchor_id or len(anchor_id) < 3:
        anchor_id = sha[:7] if sha else "commit"

    # 确保锚点唯一（简单处理：如果重复，添加SHA后缀）
    # 注意：这里使用全局变量跟踪，实际使用时需要在外部管理
    global _used_anchors
    if anchor_id not in _used_anchors:
        _used_anchors[anchor_id] = []
    _used_anchors[anchor_id].append(sha[:7])

    if len(_used_anchors[anchor_id]) > 1:
        anchor_id = f"{anchor_id}-{sha[:7]}"

    logging.debug(f"标题清理: '{title}' -> '{sanitized}' (锚点: #{anchor_id})")
    return sanitized, anchor_id


def format_commit_header(commit, analysis_result: Optional[Dict] = None) -> str:
    """格式化提交标题（使用 commit message 标题 + SHA 副标题）

    Args:
        commit: GitHub commit 对象
        analysis_result: LLM 分析结果（可选）

    Returns:
        str: 格式化后的提交标题
    """
    message = commit.commit.message
    sha = commit.sha[:7]
    url = commit.html_url

    # 清理标题
    sanitized_title, anchor_id = sanitize_commit_title(message, sha)

    # 生成标题
    header = f"### {sanitized_title}\n"
    header += f"**SHA**: `{sha}` | 🔗 [查看提交]({url})\n"

    # 如果有分析错误，添加错误提示
    if analysis_result and 'error' in analysis_result:
        header += f"\n⚠️ {analysis_result['error']}\n"

    return header


def calculate_stats(commits_with_analysis: List[Dict]) -> Dict:
    """计算统计信息

    Args:
        commits_with_analysis: 包含 commit 和 importance_info 的字典列表

    Returns:
        dict: 统计结果
        {
            'total': int,           # 总提交数
            'high': int,            # 高重要度数量
            'medium': int,          # 中重要度数量
            'low': int,             # 低重要度数量
        }
    """
    stats = {
        'total': len(commits_with_analysis),
        'high': 0,
        'medium': 0,
        'low': 0
    }

    for item in commits_with_analysis:
        importance_info = item.get('importance_info', {})
        level = importance_info.get('level', 'low')

        if level == 'high':
            stats['high'] += 1
        elif level == 'medium':
            stats['medium'] += 1
        else:
            stats['low'] += 1

    return stats


def create_stats_summary(stats: Dict) -> str:
    """创建统计摘要 Markdown

    Args:
        stats: 统计信息字典

    Returns:
        str: Markdown 格式的统计摘要
    """
    return f"### 📊 统计摘要\n> 本日共 {stats['total']} 个提交 | 🔴高 {stats['high']} | 🟡中 {stats['medium']} | 🟢低 {stats['low']}\n"


def group_by_importance(commits_with_analysis: List[Dict]) -> Dict:
    """按重要程度分组

    Args:
        commits_with_analysis: 包含 commit 和 importance_info 的字典列表

    Returns:
        dict: 分组结果
        {
            'high': [...],      # 高重要度提交列表
            'medium': [...],    # 中重要度提交列表
            'low': [...],       # 低重要度提交列表
        }
    """
    groups = {
        'high': [],
        'medium': [],
        'low': []
    }

    for item in commits_with_analysis:
        importance_info = item.get('importance_info', {})
        level = importance_info.get('level', 'low')
        groups[level].append(item)

    return groups


def format_grouped_analysis(groups: Dict) -> str:
    """格式化分组后的分析结果

    Args:
        groups: 按重要程度分组的提交

    Returns:
        str: Markdown 格式的分组分析
    """
    result = ""

    # 定义等级顺序和对应的emoji
    levels = [
        ('high', '🔴', '高'),
        ('medium', '🟡', '中'),
        ('low', '🟢', '低')
    ]

    for level_key, emoji, label_cn in levels:
        items = groups.get(level_key, [])

        if not items:
            continue

        result += f"#### {emoji} {label_cn}重要度变更 ({len(items)})\n\n"

        for item in items:
            commit = item['commit']
            analysis = item.get('analysis')

            # 添加提交标题
            result += format_commit_header(commit, item)

            # 添加分析结果
            if analysis:
                result += f"\n{analysis}\n"
            else:
                result += "\n*暂无分析*\n"

            result += "\n---\n\n"

    return result


def create_toc(commits_with_analysis: List[Dict], repo_name: str) -> str:
    """生成目录 (TOC)

    Args:
        commits_with_analysis: 包含 commit 和 importance_info 的字典列表
        repo_name: 仓库名称

    Returns:
        str: Markdown 格式的目录
    """
    toc = "## 📋 目录\n\n"
    toc += f"- [{repo_name}](#{repo_name.lower().replace('/', '-')})\n"

    # 添加统计摘要链接
    toc += "  - [📊 统计摘要](#-统计摘要)\n"

    # 按重要程度分组生成目录
    groups = group_by_importance(commits_with_analysis)
    level_names = {
        'high': ('🔴', '高'),
        'medium': ('🟡', '中'),
        'low': ('🟢', '低')
    }

    for level_key in ['high', 'medium', 'low']:
        items = groups.get(level_key, [])
        if items:
            emoji, label_cn = level_names[level_key]
            toc += f"  - [{emoji} {label_cn}重要度变更 ({len(items)})](#-{emoji}-{label_cn}重要度变更-{len(items)})\n"

            # 添加该组内的提交链接
            for item in items:
                commit = item['commit']
                message = commit.commit.message
                sha = commit.sha[:7]

                # 清理标题生成锚点
                _, anchor_id = sanitize_commit_title(message, sha)
                title = message.split('\n')[0].strip()
                if len(title) > 50:
                    title = title[:47] + "..."

                toc += f"    - [{title}](#{anchor_id})\n"

    return toc
