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
    create_report_file,
    get_report_file_path,
    TIME_ZONE,
    create_toc,
    calculate_stats,
    create_stats_summary,
    group_by_importance,
    format_grouped_analysis,
)

from llm import (
    analyze_commit,
)

from config import (
    load_config,
    get_importance_config,
    get_rate_limit_config,
    get_format_config,
)

# 配置要监控的仓库
REPOSITORIES = [
    "vllm-project/vllm",
    "sgl-project/sglang",
    "ai-dynamo/dynamo",
]

# 必需的环境变量列表
# GITHUB_TOKEN 在 GitHub Actions 中自动提供，不需要用户配置
# TOKEN 可选用于本地开发环境
REQUIRED_ENV_VARS = ["REPOSITORY", "LLM_API_KEY", "LLM_MODEL", "LLM_BASE_URL"]


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
    parser.add_argument('--config', type=str, default=None, help='配置文件路径（默认为项目根目录的 config.yaml）')
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

    # 加载配置文件
    config = load_config(args.config)
    logging.debug(f"配置已加载: {args.config or '默认配置'}")

    # 从环境变量读取配置
    repository = os.getenv("REPOSITORY")

    # 初始化GitHub客户端
    # GITHUB_TOKEN 由 GitHub Actions 自动提供，或从 TOKEN 环境变量读取（本地开发）
    github_client = init_github_client()
    if not github_client:
        logging.error("无法初始化GitHub客户端，程序终止")
        sys.exit(1)

    # 获取当前仓库（用于提交报告文件）
    current_repo = get_repository(github_client, repository)
    if not current_repo:
        logging.error("无法获取当前仓库，程序终止")
        sys.exit(1)

    for repo_name in REPOSITORIES:
        report_content = "# 每日更新报告（" + get_yesterday_date() + "）\n\n"
        logging.info(f"正在获取 {repo_name} 的提交...")
        repo = get_repository(github_client, repo_name)
        if not repo:
            logging.error(f"跳过 {repo_name}")
            continue
        logging.info(f"仓库信息: {repo.full_name}, 星标: {repo.stargazers_count}")
        commits = get_commits_lastday(repo)
        logging.info(f"成功获取 {repo_name} 的 {len(commits)} 个提交")
        report_content += f"## {repo_name}\n\n"
        report_content += create_commit_report(commits)
        if args.enable_analysis:
            logging.info("正在使用LLM分析提交...")
            # 从环境变量读取 LLM 配置
            llm_api_key = os.getenv("LLM_API_KEY")
            llm_model = os.getenv("LLM_MODEL")

            # 构建仓库上下文信息
            repo_context = {
                'name': repo.full_name,
                'language': repo.language or 'Unknown',
                'stars': repo.stargazers_count,
            }

            # 调用新版 analyze_commit，返回字典列表
            # 提取重要性评分配置
            importance_config = get_importance_config(config)

            commits_with_analysis = analyze_commit(
                commits,
                repo_context=repo_context,
                api_key=llm_api_key,
                model=llm_model,
                config=importance_config
            )

            # 生成增强的报告格式
            if commits_with_analysis:
                # 统计摘要
                stats = calculate_stats(commits_with_analysis)
                report_content += create_stats_summary(stats)

                # 目录 (TOC)
                report_content += create_toc(commits_with_analysis, repo_name)

                # 按重要程度分组并格式化
                groups = group_by_importance(commits_with_analysis)
                report_content += format_grouped_analysis(groups)

                logging.debug(f"LLM分析完成: 总计 {stats['total']} 个提交")
                logging.debug(f"  - 🔴 高重要度: {stats['high']}")
                logging.debug(f"  - 🟡 中重要度: {stats['medium']}")
                logging.debug(f"  - 🟢 低重要度: {stats['low']}")
        if args.debug:
            logging.debug("\n生成的报告内容预览:")
            logging.debug(report_content)

        # 准备报告文件路径
        yesterday_date = get_yesterday_date()
        report_file_path = get_report_file_path(repo_name, yesterday_date)

        # dry-run模式：输出到控制台，不创建文件
        if args.dry_run:
            logging.info("=" * 60)
            logging.info(f"DRY-RUN模式: {repo_name} 报告内容")
            logging.info("=" * 60)
            print(report_content)
            print("=" * 60)
            logging.info(f"DRY-RUN模式: 跳过创建报告文件 '{report_file_path}'")
        else:
            # 创建报告文件
            create_report_file(current_repo, report_file_path, report_content)

def get_yesterday_date():
    yesterday = datetime.now(TIME_ZONE) - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

if __name__ == "__main__":
    main() 