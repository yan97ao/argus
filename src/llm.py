import os
import json
from time import sleep, time
import requests
import logging
from typing import List, Dict, Any, Optional, Tuple

from importance_scorer import calculate_importance_score, get_importance_emoji

# 存储已使用的锚点，用于检测重复
_used_anchors: Dict[str, List[str]] = {}

def analyze_commit(commits, repo_context=None, api_key=None, model=None, config=None):
    """分析提交内容，使用LLM提供洞察

    Args:
        commits: GitHub提交对象列表
        repo_context: 仓库上下文信息 (可选)
        api_key: API密钥（如果为None，从LLM_API_KEY环境变量读取）
        model: 模型名称（如果为None，从LLM_MODEL环境变量读取）
        config: 配置字典 (可选)

    Returns:
        list: LLM分析结果列表，每个元素包含 (commit, analysis, importance_info)
    """
    if not commits:
        return []

    # 从环境变量读取配置（如果参数未提供）
    if api_key is None:
        api_key = os.getenv("LLM_API_KEY")
    if model is None:
        model = os.getenv("LLM_MODEL")

    results = []
    for commit in commits:
        logging.info(f"分析提交: {commit.sha}")

        # 计算重要性评分（传递配置）
        importance_info = calculate_importance_score(commit, repo_context, config)
        importance_level = importance_info['level']

        # 构建提示词
        system_prompt = build_system_prompt(importance_level)
        user_prompt = build_user_prompt_enhanced(commit, repo_context, importance_info)

        # 调用LLM进行分析（带重试）
        max_retries = 3
        for attempt in range(max_retries):
            try:
                output, response_time = call_llm(
                    system_prompt, user_prompt,
                    api_key=api_key, model=model,
                    return_response_time=True
                )
                logging.debug("LLM分析结果:")
                logging.debug(output)

                results.append({
                    'commit': commit,
                    'analysis': output,
                    'importance_info': importance_info
                })
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    # 检查是否是限流错误
                    is_rate_limited = "429" in str(e) or "rate limit" in str(e).lower()
                    delay = smart_rate_limit(response_time if 'response_time' in locals() else None,
                                             is_rate_limited,
                                             attempt + 1)
                    logging.warning(f"LLM调用失败（第{attempt + 1}次尝试）: {str(e)}, {delay}秒后重试...")
                    sleep(delay)
                else:
                    error_msg = f"LLM分析失败（已重试{max_retries}次）: {str(e)}"
                    logging.error(error_msg)
                    results.append({
                        'commit': commit,
                        'analysis': None,
                        'importance_info': importance_info,
                        'error': error_msg
                    })
                    break
        else:
            # 智能速率控制延迟（正常情况）
            delay = smart_rate_limit(None, False, 0)
            if delay > 0:
                sleep(delay)

    return results


def build_system_prompt(importance_level: str = "medium") -> str:
    """根据重要程度生成分级 system prompt

    Args:
        importance_level: 'low', 'medium', 或 'high'

    Returns:
        str: system prompt 内容
    """
    if importance_level == "low":
        # 🟢 低重要度：简化版（3 字段）
        return """你是一位代码审查专家。请为这次变更提供简洁的分析。

**🎯 变更类型**：[从以下选择: 文档更新/配置调整/测试修改/代码重构/其他]
**⚡ 重要程度**：🟢低
**📋 摘要**：[1-2句话概括变更内容]

要求: 简洁明了,不超过100字。"""

    elif importance_level == "medium":
        # 🟡 中重要度：标准版（5 字段）
        return """你是一位代码审查专家。请为这次变更提供中等深度的分析。

**🎯 变更类型**：[功能增强/Bug修复/性能优化/重构/其他]
**⚡ 重要程度**：🟡中
**📋 变更摘要**：[2-3句话概括变更内容和目标]
**🎯 影响范围**：[列出受影响的主要模块]
**💡 关注建议**：[给开发者和用户的具体建议]

要求: 关注核心变更,提供可操作的建议,200字左右。"""

    else:
        # 🔴 高重要度：完整版（7 字段，当前格式）
        return """你是一位资深的软件工程师和代码审查专家，专门分析开源项目的代码变更。

## 你的专长
- 识别代码变更的技术影响和业务价值
- 评估变更的风险等级和影响范围
- 从架构、性能、安全、可维护性等多个维度分析
- 为开发者提供简洁而有价值的技术洞察

## 分析原则
1. 关注变更的实际影响，而非表面现象
2. 识别潜在的风险和机会
3. 提供可操作的建议和洞察
4. 保持客观和专业的分析态度

## 输出格式要求
请严格按照以下格式提供分析，每个部分都必须填写：

**🎯 变更类型**：[功能增强/Bug修复/性能优化/重构/架构变更/安全修复]
**⚡ 重要程度**：🔴高
**📋 变更摘要**：[2-3句话概括变更内容、目标和预期效果]
**🎯 影响范围**：[列出受影响的主要模块或组件]
**🔍 技术洞察**：
- 架构影响：[对系统架构的影响]
- 性能影响：[对性能的潜在影响]
- 安全考虑：[是否涉及安全相关变更]
**⚠️ 潜在风险**：[识别可能的风险点]
**💡 关注建议**：[给开发者和用户的具体建议]

## 回答要求
- 使用中文回答
- 保持简洁但信息丰富
- 避免重复信息，每个部分应有独特价值"""


def build_user_prompt_enhanced(commit, repo_context: Optional[Dict] = None, importance_info: Optional[Dict] = None) -> str:
    """生成增强的 user prompt，包含上下文信息

    Args:
        commit: GitHub commit 对象
        repo_context: 仓库上下文信息 (可选)
        importance_info: 重要性评分信息 (可选)

    Returns:
        str: user prompt 内容
    """
    prompt = "## 仓库上下文\n"
    if repo_context:
        prompt += f"- 项目: {repo_context.get('name', 'Unknown')}\n"
        prompt += f"- 主要语言: {repo_context.get('language', 'Unknown')}\n"
        if 'stars' in repo_context:
            prompt += f"- 星标: {repo_context['stars']}\n"
    prompt += "\n"

    prompt += "## 提交信息\n"
    prompt += f"- SHA: {commit.sha}\n"
    prompt += f"- 作者: {commit.commit.author.name}\n"
    prompt += f"- 消息: {commit.commit.message}\n"

    # 添加重要性相关信息
    if importance_info:
        details = importance_info.get('details', {})
        prompt += f"- 类型: {details.get('commit_type', 'unknown')}\n"
        prompt += f"- 变更规模: {commit.stats.additions if hasattr(commit, 'stats') else 0}+ / {commit.stats.deletions if hasattr(commit, 'stats') else 0}-\n"
        prompt += f"- 主要文件类型: {details.get('primary_file_type', 'unknown')}\n"

    prompt += "\n## 修改文件\n"

    # 获取文件变更详情
    try:
        for file in commit.files:
            status_desc = {
                'added': '新增',
                'modified': '修改',
                'removed': '删除',
                'renamed': '重命名',
                'changed': '变更'
            }.get(file.status, file.status)

            prompt += f"  * {status_desc}: {file.filename} (+{file.additions}/-{file.deletions})\n"

            # 优化差异截断：>50KB 截断到 50KB
            if hasattr(file, 'patch') and file.patch:
                if len(file.patch) > 50000:  # 50KB
                    prompt += f"```diff\n{file.patch[:50000]}\n```\n"
                    prompt += f"(差异过大，已截断到前50KB)\n"
                else:
                    prompt += f"```diff\n{file.patch}\n```\n"
    except Exception as e:
        prompt += f"  * 无法获取文件详情: {str(e)}\n"

    # 添加分析深度要求
    prompt += "\n## 分析要求\n"
    if importance_info:
        level = importance_info.get('level', 'medium')
        if level == 'high':
            prompt += "- 请提供全面深入的技术分析\n"
            prompt += "- 关注架构、性能、安全等多维度影响\n"
        elif level == 'medium':
            prompt += "- 请提供中等深度的分析\n"
            prompt += "- 关注核心变更和影响范围\n"
        else:  # low
            prompt += "- 请提供简洁的摘要即可\n"

    prompt += "\n---\n\n"

    logging.debug("=" * 40)
    logging.debug("LLM提示词:")
    logging.debug(prompt)
    logging.debug("-" * 40)
    return prompt


def smart_rate_limit(response_time: Optional[float], is_rate_limited: bool, attempt_num: int) -> int:
    """智能速率控制

    Args:
        response_time: 上次API响应时间（秒）
        is_rate_limited: 是否被限流
        attempt_num: 当前重试次数

    Returns:
        int: 需要等待的秒数
    """
    if is_rate_limited:
        # 指数退避：10s, 20s, 30s
        backoff = min(10 * attempt_num, 30)
        logging.warning(f"检测到限流，使用指数退避: {backoff}秒")
        return backoff
    elif response_time is not None:
        if response_time < 1.0:
            # 响应快，加速到5秒
            return 5
        elif response_time > 5.0:
            # 响应慢，减速到15秒
            return 15

    # 默认延迟
    return 10


def call_llm(system_prompt: str, user_prompt: str, api_key: str = None, model: str = None,
            return_response_time: bool = False) -> Tuple[str, Optional[float]]:
    """调用LLM API获取LLM回复

    Args:
        system_prompt: 系统提示词
        user_prompt: 用户提示词
        api_key: API密钥（如果为None，从LLM_API_KEY环境变量读取）
        model: 模型名称（如果为None，从LLM_MODEL环境变量读取）
        return_response_time: 是否返回响应时间

    Returns:
        (str, Optional[float]): LLM回复内容和响应时间（秒）
    """
    # 从环境变量读取配置（如果参数未提供）
    if api_key is None:
        api_key = os.getenv("LLM_API_KEY")
    if model is None:
        model = os.getenv("LLM_MODEL")

    # LLM API端点（从环境变量读取）
    api_url = os.getenv("LLM_BASE_URL")

    # 请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-Title": "Argus Git Commit Analyzer"  # 应用名称
    }

    # 请求体
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 1.0,  # https://api-docs.deepseek.com/zh-cn/quick_start/parameter_settings
        "max_tokens": 2048   # 限制回复长度
    }

    try:
        # 记录开始时间
        start_time = time()

        # 发送请求
        response = requests.post(api_url, headers=headers, json=data, timeout=30)

        # 计算响应时间
        response_time = time() - start_time

        logging.info("call LLM with %s bytes and got %s bytes in %.2fs",
                    len(response.request.body), len(response.content), response_time)
        response.raise_for_status()  # 检查HTTP错误

        # 解析响应
        result = response.json()

        # 提取回复内容
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            if return_response_time:
                return content, response_time
            return content
        else:
            raise ValueError(f"无效的API响应: {json.dumps(result)}")

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API请求失败: {str(e)}")
    except json.JSONDecodeError:
        raise ValueError(f"无法解析API响应: {response.text}")
    except Exception as e:
        raise RuntimeError(f"调用LLM时出错: {str(e)}")
