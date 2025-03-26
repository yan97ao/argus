#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
import pytz
from github import Github
from dateutil.parser import parse

# 配置要监控的仓库
REPOSITORIES = [
    "vllm-project/vllm",
    "sgl-project/sglang"
]

def get_commits_since_last_check(repo, last_check_time):
    """获取指定时间后的所有提交"""
    commits = []
    for commit in repo.get_commits():
        # 直接使用commit.commit.author.date，它已经是datetime对象
        commit_time = commit.commit.author.date
        if commit_time <= last_check_time:
            break
        commits.append({
            'sha': commit.sha[:7],
            'message': commit.commit.message,
            'author': commit.commit.author.name,
            'date': commit_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    return commits

def create_issue_content(commits_data):
    """创建issue内容"""
    today = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')
    content = f"# 仓库更新报告 ({today})\n\n"
    
    for repo_name, commits in commits_data.items():
        if not commits:
            content += f"## {repo_name}\n\n"
            content += "今日无更新\n\n"
            continue
            
        content += f"## {repo_name}\n\n"
        content += "| 提交时间 | 作者 | 提交信息 |\n"
        content += "|----------|------|----------|\n"
        
        for commit in commits:
            # 获取提交信息的第一行，移除换行符
            message = commit['message'].split('\n')[0]
            content += f"| {commit['date']} | {commit['author']} | {message} |\n"
        
        content += "\n"
    
    return content

def main():
    # 使用默认的GITHUB_TOKEN
    g = Github()
    
    # 获取当前仓库
    try:
        current_repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
    except Exception as e:
        print(f"Error getting current repository: {str(e)}")
        return
    
    # 获取昨天的日期（CST时区）
    cst = pytz.timezone('Asia/Shanghai')
    yesterday = datetime.now(cst).replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 收集所有仓库的更新
    commits_data = {}
    for repo_name in REPOSITORIES:
        try:
            repo = g.get_repo(repo_name)
            commits = get_commits_since_last_check(repo, yesterday)
            commits_data[repo_name] = commits
        except Exception as e:
            print(f"Error processing {repo_name}: {str(e)}")
            commits_data[repo_name] = []
    
    # 创建issue内容
    issue_content = create_issue_content(commits_data)
    
    # 创建issue
    try:
        current_repo.create_issue(
            title=f"仓库更新报告 ({datetime.now(cst).strftime('%Y-%m-%d')})",
            body=issue_content
        )
        print("Successfully created issue")
    except Exception as e:
        print(f"Error creating issue: {str(e)}")
        # 打印更详细的错误信息
        if hasattr(e, 'data'):
            print(f"Error details: {e.data}")

if __name__ == "__main__":
    main() 