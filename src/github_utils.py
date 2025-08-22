#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime, timedelta
import pytz
from github import Github
from github.Commit import Commit
from github.GithubException import GithubException

TIME_ZONE = pytz.timezone('Asia/Shanghai')

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

def validate_and_truncate_content(title, body, max_title_length=256, max_body_length=65536):
    """验证并截断issue内容以符合GitHub限制
    
    Args:
        title: issue标题
        body: issue内容  
        max_title_length: 标题最大长度，GitHub限制为256字符
        max_body_length: 内容最大长度，GitHub限制为65536字符
        
    Returns:
        tuple: (截断后的标题, 截断后的内容, 是否被截断)
    """
    truncated = False
    
    # 截断标题
    if len(title) > max_title_length:
        title = title[:max_title_length-3] + "..."
        truncated = True
        logging.warning(f"标题过长，已截断至 {max_title_length} 字符")
    
    # 截断内容
    if len(body) > max_body_length:
        # 在合适的位置截断，尽量保持markdown结构
        truncate_pos = max_body_length - 200  # 留出空间添加截断说明
        
        # 尝试在段落边界截断
        newline_pos = body.rfind('\n\n', 0, truncate_pos)
        if newline_pos > max_body_length // 2:  # 确保不会截断太多内容
            truncate_pos = newline_pos
        
        truncated_body = body[:truncate_pos]
        truncated_body += "\n\n---\n\n**⚠️ 内容过长已截断**\n\n"
        truncated_body += f"原始内容长度: {len(body)} 字符\n"
        truncated_body += f"截断后长度: {len(truncated_body)} 字符\n\n"
        truncated_body += "完整内容请查看 GitHub Actions 运行日志。"
        
        original_length = len(body)
        body = truncated_body
        truncated = True
        logging.warning(f"内容过长，已从 {original_length} 字符截断至 {len(body)} 字符")
    
    return title, body, truncated

def create_issue(repo, title, body, debug=False):
    """创建issue
    
    Args:
        repo: GitHub仓库实例
        title: issue标题
        body: issue内容
        debug: 是否开启调试模式
        
    Returns:
        Issue: 创建的issue实例，如果失败则返回None
    """
    try:
        # 验证并截断内容
        validated_title, validated_body, was_truncated = validate_and_truncate_content(title, body)
        
        # 记录内容长度用于调试
        logging.debug(f"Issue标题长度: {len(validated_title)}")
        logging.debug(f"Issue内容长度: {len(validated_body)}")
        if was_truncated:
            logging.info("内容已截断以符合GitHub限制")
        
        issue = repo.create_issue(title=validated_title, body=validated_body)
        logging.info(f"成功创建issue: #{issue.number}")
        return issue
    except GithubException as e:
        # 详细记录GitHub API错误信息
        error_msg = f"创建issue失败: {e.status}"
        if hasattr(e, 'data') and e.data:
            if isinstance(e.data, dict):
                error_msg += f" {e.data.get('message', '')}"
                # 记录详细的验证错误
                if 'errors' in e.data:
                    for error in e.data['errors']:
                        if isinstance(error, dict):
                            error_msg += f"\n  - {error.get('field', 'unknown')}: {error.get('message', error.get('code', 'unknown error'))}"
                        else:
                            error_msg += f"\n  - {error}"
            else:
                error_msg += f" {e.data}"
        logging.error(error_msg)
        
        # 如果是内容过长错误，提供额外信息
        if e.status == 422:
            logging.error(f"可能原因: 内容长度超限 (标题: {len(validated_title)} 字符, 内容: {len(validated_body)} 字符)")
            
    except Exception as e:
        logging.error(f"创建issue出错: {str(e)}")
    return None
