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
        issue = repo.create_issue(title=title, body=body)
        logging.info(f"成功创建issue: #{issue.number}")
        return issue
    except GithubException as e:
        logging.error(f"创建issue失败: {e.status} {e.data.get('message')}")
    except Exception as e:
        logging.error(f"创建issue出错: {str(e)}")
    return None

def get_old_open_issues(repo, days_threshold=30):
    """获取超过指定天数的开放issue
    
    Args:
        repo: GitHub仓库实例
        days_threshold: 天数阈值，默认30天
        
    Returns:
        list: 超过阈值天数的开放issue列表
    """
    try:
        # 计算阈值日期
        threshold_date = datetime.now(TIME_ZONE) - timedelta(days=days_threshold)
        threshold_utc = threshold_date.astimezone(pytz.UTC)
        
        logging.info(f"扫描 {repo.full_name} 中超过 {days_threshold} 天的开放issue...")
        
        # 获取所有开放的issue
        open_issues = repo.get_issues(state='open')
        old_issues = []
        
        for issue in open_issues:
            # 检查创建时间是否超过阈值
            if issue.created_at < threshold_utc:
                old_issues.append(issue)
                logging.debug(f"发现旧issue: #{issue.number} - {issue.title} (创建于: {issue.created_at})")
        
        logging.info(f"发现 {len(old_issues)} 个超过 {days_threshold} 天的开放issue")
        return old_issues
        
    except GithubException as e:
        logging.error(f"获取 {repo.full_name} 旧issue失败: {e.status} {e.data.get('message')}")
    except Exception as e:
        logging.error(f"获取 {repo.full_name} 旧issue出错: {str(e)}")
    return []

def close_old_issues(repo, days_threshold=30):
    """关闭超过指定天数的开放issue
    
    Args:
        repo: GitHub仓库实例
        days_threshold: 天数阈值，默认30天
        
    Returns:
        int: 成功关闭的issue数量
    """
    old_issues = get_old_open_issues(repo, days_threshold)
    closed_count = 0
    
    for issue in old_issues:
        try:
            # 添加关闭评论
            close_comment = f"此历史记录issue已存在{days_threshold}天，作为展示记录已完成使命，现自动关闭以保持仓库整洁。"
            issue.create_comment(close_comment)
            
            # 关闭issue
            issue.edit(state='closed')
            logging.info(f"成功关闭旧issue: #{issue.number} - {issue.title}")
            closed_count += 1
            
        except GithubException as e:
            logging.error(f"关闭issue #{issue.number} 失败: {e.status} {e.data.get('message')}")
        except Exception as e:
            logging.error(f"关闭issue #{issue.number} 出错: {str(e)}")
    
    logging.info(f"成功关闭 {closed_count} 个旧issue")
    return closed_count
