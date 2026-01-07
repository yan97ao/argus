#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
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

# 必需的环境变量列表
REQUIRED_ENV_VARS = ["TOKEN", "REPOSITORY", "LLM_API_KEY", "LLM_MODEL", "LLM_BASE_URL"]


def check_required_env_vars():
    """检查所有必需的环境变量是否已设置

    Returns:
        bool: 如果所有变量都已设置则返回 True，否则返回 False
    """
    missing_vars = []
    set_vars = []

    for var in REQUIRED_ENV_VARS:
        value = os.getenv(var)
        if value is None or value.strip() == "":
            missing_vars.append(var)
        else:
            set_vars.append(var)

    if missing_vars:
        print("=" * 60, file=sys.stderr)
        print("错误：缺少必需的环境变量", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print("\n以下环境变量必须设置：", file=sys.stderr)
        for var in REQUIRED_ENV_VARS:
            if var in missing_vars:
                print(f"  ✗ {var}", file=sys.stderr)
            else:
                print(f"  ✓ {var}", file=sys.stderr)
        print("\n请设置这些环境变量后重试。", file=sys.stderr)
        print("参考 .env.example 文件或使用：source .env\n", file=sys.stderr)
        return False

    return True


def main():
    # 首先检查必需的环境变量
    if not check_required_env_vars():
        sys.exit(1)

    # 解析命令行参数（仅保留行为控制参数）
    parser = argparse.ArgumentParser(description='GitHub仓库更新监控工具')
    parser.add_argument('--debug', action='store_true', help='启用详细日志输出')
    parser.add_argument('--dry-run', action='store_true', help='dry-run模式：只输出报告内容，不创建GitHub Issue')
    parser.add_argument('--enable-analysis', action='store_true', help='启用LLM分析模式')
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

    # 从环境变量读取配置
    token = os.getenv("TOKEN")
    repository = os.getenv("REPOSITORY")

    # 初始化GitHub客户端
    github_client = init_github_client(token=token)
    if not github_client:
        logging.error("无法初始化GitHub客户端，程序终止")
        sys.exit(1)

    # 获取当前仓库（用于创建issue）
    current_repo = get_repository(github_client, repository)
    if not current_repo:
        logging.error("无法获取当前仓库，程序终止")
        sys.exit(1)
    
    for repo_name in REPOSITORIES:
        issue_content = "# 每日更新报告（" + get_yesterday_date() + "）\n\n"
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
            # 从环境变量读取 LLM 配置
            llm_api_key = os.getenv("LLM_API_KEY")
            llm_model = os.getenv("LLM_MODEL")
            analysis_result = analyze_commit(commits, api_key=llm_api_key, model=llm_model)
            logging.debug("LLM分析结果:")
            logging.debug(analysis_result)
            issue_content += f"## {repo_name} 的LLM分析结果\n\n"
            issue_content += analysis_result
        if args.debug:
            logging.debug("\n生成的issue内容预览:")
            logging.debug(issue_content)

        # 准备issue标题（dry-run和创建issue都需要）
        yesterday_date = get_yesterday_date()
        issue_title = f"{yesterday_date}: {repo_name} 仓库更新报告"

        # dry-run模式：输出到控制台，不创建issue
        if args.dry_run:
            logging.info("=" * 60)
            logging.info(f"DRY-RUN模式: {repo_name} 报告内容")
            logging.info("=" * 60)
            print(issue_content)
            print("=" * 60)
            logging.info(f"DRY-RUN模式: 跳过创建 Issue '{issue_title}'")
        else:
            # 创建issue
            create_issue(current_repo, issue_title, issue_content)

def get_yesterday_date():
    yesterday = datetime.now(TIME_ZONE) - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

if __name__ == "__main__":
    main() 