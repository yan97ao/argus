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
        commit_time = parse(commit.commit.author.date)
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
            content += f"| {commit['date']} | {commit['author']} | {commit['message'].split('\n')[0]} |\n"
        
        content += "\n"
    
    return content

def main():
    # 使用默认的GITHUB_TOKEN
    g = Github()
    
    # 获取当前仓库
    current_repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
    
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

if __name__ == "__main__":
    main() 