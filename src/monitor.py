#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
from datetime import datetime, timedelta
import pytz
from github import Github
from github.GithubException import GithubException

# 配置要监控的仓库
REPOSITORIES = [
    "vllm-project/vllm",
    "sgl-project/sglang"
]

TIME_ZONE = pytz.timezone('Asia/Shanghai')

def get_commits_lastday(repo):
    """获取最近一天的提交"""
    commits = []
    yesterday = datetime.now(TIME_ZONE) - timedelta(days=1)
    since = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    until = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
    print(f"==== 获取 {repo.full_name} 提交从 {since} 到 {until}")
    try:
        paged_commits = repo.get_commits(since=since, until=until)
        for commit in paged_commits:
            commits.append(commit)
    except GithubException as e:
        print(f"==== 获取 {repo.full_name} 提交失败: {e.status} {e.data.get('message')}")
    return commits

def create_issue_content(commits_data):
    """创建issue内容"""
    today = datetime.now(TIME_ZONE).strftime('%Y-%m-%d')
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
            message = commit.commit.message.split('\n')[0]
            # 处理表格中的竖线字符，避免格式错误
            message = message.replace('|', '\\|')
            content += f"| {commit.commit.author.date} | {commit.commit.author.name} | {message} |\n"
        
        content += "\n"
    
    return content

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='GitHub仓库更新监控工具')
    parser.add_argument('--token', help='GitHub个人访问令牌（PAT）')
    parser.add_argument('--repo', help='目标仓库（格式：owner/repo）')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    args = parser.parse_args()

    # 设置调试模式
    debug = args.debug
    if debug:
        print("调试模式已启用")
        print(f"当前环境变量 GITHUB_REPOSITORY: {os.getenv('GITHUB_REPOSITORY')}")
        print(f"当前环境变量 GITHUB_TOKEN: {'已设置' if os.getenv('GITHUB_TOKEN') else '未设置'}")

    # 初始化GitHub客户端
    try:
        if args.token:
            g = Github(args.token)
        elif os.getenv('GITHUB_TOKEN'):
            g = Github(os.getenv('GITHUB_TOKEN'))
        else:
            g = Github()
            
        # 测试API连接
        rate_limit = g.get_rate_limit()
        if debug:
            print(f"API速率限制: {rate_limit.core.limit}, 剩余: {rate_limit.core.remaining}")
    except Exception as e:
        print(f"初始化GitHub客户端失败: {str(e)}")
        return
    
    # 获取当前仓库
    try:
        if args.repo:
            current_repo = g.get_repo(args.repo)
        else:
            repo_name = os.getenv('GITHUB_REPOSITORY')
            if not repo_name:
                print("错误: 未指定仓库名称，请使用--repo参数或设置GITHUB_REPOSITORY环境变量")
                return
            current_repo = g.get_repo(repo_name)
    except GithubException as e:
        print(f"获取仓库失败: {e.status} {e.data.get('message')}")
        return
    except Exception as e:
        print(f"获取仓库出错: {str(e)}")
        return
    
    # 收集所有仓库的更新
    commits_data = {}
    for repo_name in REPOSITORIES:
        print(f"正在获取 {repo_name} 的提交...")
        try:
            repo = g.get_repo(repo_name)
            if debug:
                print(f"==== 仓库信息: {repo.full_name}, 星标: {repo.stargazers_count}")
            
            commits = get_commits_lastday(repo)
            commits_data[repo_name] = commits
            print(f"==== 成功获取 {repo_name} 的 {len(commits)} 个提交")
        except GithubException as e:
            print(f"==== 访问仓库 {repo_name} 失败: {e.status} {e.data.get('message')}")
            commits_data[repo_name] = []
        except Exception as e:
            print(f"==== 处理 {repo_name} 出错: {str(e)}")
            commits_data[repo_name] = []
    
    # 创建issue内容
    issue_content = create_issue_content(commits_data)
    
    if debug:
        print("\n生成的issue内容预览:")
        print(issue_content)
        return
    else:    
        # 创建issue
        try:
            # 获取昨天的日期并格式化
            yesterday_date = (datetime.now(TIME_ZONE) - timedelta(days=1)).strftime('%Y-%m-%d')
            issue = current_repo.create_issue(
                title=f"仓库更新报告 ({yesterday_date})",
                body=issue_content
            )
            print(f"成功创建issue: #{issue.number}")
        except GithubException as e:
            print(f"创建issue失败: {e.status} {e.data.get('message')}")
        except Exception as e:
            print(f"创建issue出错: {str(e)}")

if __name__ == "__main__":
    main() 