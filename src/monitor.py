#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
from datetime import datetime, timedelta
import logging

from github_utils import (
    init_github_client, 
    get_repository, 
    get_commits_lastday, 
    create_commit_report, 
    create_issue,
    TIME_ZONE
)

from llm import (
    analyze_commit,
)

# 配置要监控的仓库
REPOSITORIES = [
    "vllm-project/vllm",
    "sgl-project/sglang",
    "ai-dynamo/dynamo",
]

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='GitHub仓库更新监控工具')
    parser.add_argument('--github-token', help='GitHub个人访问令牌（PAT）')
    parser.add_argument('--repo', help='目标仓库（格式：owner/repo）')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    parser.add_argument('--enable-analysis', action='store_true', help='启用LLM分析模式')
    parser.add_argument('--llm-api-key', help='DeepSeek API密钥')
    parser.add_argument('--llm-model', help='DeepSeek 模型名称，例如: deepseek-chat')
    args = parser.parse_args()

    # 设置调试模式
    if args.debug:
       log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(level=log_level,
                        format="%(asctime)s - %(levelname)s - %(message)s",
                        handlers=[logging.StreamHandler()])
    logging.debug("调试模式已启用")

    # 初始化GitHub客户端
    github_client = init_github_client(token=args.github_token)
    if not github_client:
        logging.error("无法初始化GitHub客户端，程序终止")
        sys.exit(1)
    
    # 获取当前仓库（用于创建issue）
    current_repo = get_repository(github_client, args.repo)
    if not current_repo:
        logging.error("无法获取当前仓库，程序终止")
        sys.exit(1)
    
    issue_content = "# 每日更新报告（" + get_yesterday_date() + "）\n\n"
    for repo_name in REPOSITORIES:
        logging.info(f"正在获取 {repo_name} 的提交...")
        repo = get_repository(github_client, repo_name)
        if not repo:
            logging.error(f"跳过 {repo_name}")
            continue
        logging.info(f"仓库信息: {repo.full_name}, 星标: {repo.stargazers_count}")
        commits = get_commits_lastday(repo)
        logging.info(f"成功获取 {repo_name} 的 {len(commits)} 个提交")
        issue_content += f"## {repo_name}\n\n"
        issue_content += create_commit_report(commits)
        if args.enable_analysis:
            logging.info("正在使用LLM分析提交...")
            analysis_result = analyze_commit(commits, api_key=args.llm_api_key, model=args.llm_model)
            logging.debug("LLM分析结果:")
            logging.debug(analysis_result)
            issue_content += f"## {repo_name} 的LLM分析结果\n\n"
            issue_content += analysis_result
    
    if args.debug:
        logging.debug("\n生成的issue内容预览:") 
        logging.debug(issue_content)

    # 创建issue
    yesterday_date = get_yesterday_date()
    issue_title = f"仓库更新报告 ({yesterday_date})"
    create_issue(current_repo, issue_title, issue_content)

def get_yesterday_date():
    yesterday = datetime.now(TIME_ZONE) - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

if __name__ == "__main__":
    main() 