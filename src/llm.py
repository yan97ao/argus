import os
import json
import requests
import logging
from typing import List, Dict, Any, Optional

def analyze_commit(commits, api_key=None, model=None):
    """分析提交内容，使用LLM提供洞察
    
    Args:
        commits: GitHub提交对象列表
        api_key: API密钥，优先使用参数传入的值
        model: 模型名称，优先使用参数传入的值
        
    Returns:
        str: LLM分析结果
    """
    if not commits:
        return "没有提交可供分析"
    
    if api_key is None:
        error_msg = "未提供大模型API密钥，请通过--llm-api-key参数或LLM_API_KEY环境变量设置"
        logging.error(error_msg)
        return error_msg

    if model is None:
        logging.warning("未提供大模型名称，使用默认模型: deepseek-chat")
        model = "deepseek-chat"

    result = ""
    for commit in commits:
        logging.info(f"分析提交: {commit.sha}")
        system_prompt = build_system_prompt()
        user_prompt = build_user_prompt(commit)
    
        # 调用LLM进行分析
        try:
            output = call_llm(system_prompt, user_prompt, api_key=api_key, model=model)
            logging.debug("LLM分析结果:")
            logging.debug(output)
            result += "### " + commit.sha + "\n"
            result += commit.html_url + "\n"
            result += commit.commit.message + "\n"
            result += output + "\n\n"
        except Exception as e:
            error_msg = f"LLM分析失败: {str(e)}"
            logging.error(error_msg)

    return result

def build_system_prompt():
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

**🎯 变更类型**：[功能增强/Bug修复/性能优化/重构/文档/测试/配置/依赖更新/其他]
**⚡ 重要程度**：[🔴高/🟡中/🟢低]
**📋 变更摘要**：[用2-3句话概括这次变更的核心内容、目标和预期效果]
**🎯 影响范围**：[列出受影响的主要模块或组件]
**🔍 技术洞察**：
- 架构影响：[对系统架构的影响，如模块关系、设计模式等]
- 性能影响：[对性能的潜在影响，包括时间和空间复杂度]
- 安全考虑：[是否涉及安全相关变更或引入新的安全风险]
**⚠️ 潜在风险**：[识别可能的风险点，如破坏性变更、性能回归、兼容性问题等]
**💡 关注建议**：[给开发者和用户的具体建议，如需要额外测试的场景、升级注意事项等]

## 回答要求
- 使用中文回答
- 保持简洁但信息丰富
- 如果某个维度不适用，请明确标注"无"或"不适用"
- 避免重复信息，每个部分应有独特价值"""

def build_user_prompt(commit):
    prompt = "待分析的提交信息如下:\n\n"
    prompt += f"- 提交: {commit.sha}\n"
    prompt += f"- 作者: {commit.commit.author.name}\n"
    prompt += f"- 消息: {commit.commit.message}\n"
    prompt += "- 修改文件:\n"
    
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
            
            if hasattr(file, 'patch') and file.patch:
                if len(file.patch) > 100000: # 100K
                    prompt += f"```diff\n{file.patch[:10000]}\n```\n"
                else:
                    prompt += f"```diff\n{file.patch}\n```\n"
    except Exception as e:
        prompt += f"  * 无法获取文件详情: {str(e)}\n"
        
    prompt += "\n---\n\n"

    logging.debug("=" * 40)
    logging.debug("LLM提示词:")
    logging.debug(prompt)
    logging.debug("-" * 40)
    return prompt

def call_llm(system_prompt: str, user_prompt: str, api_key: str = None, model: str = None) -> str:
    """调用LLM API获取LLM回复
    
    Args:
        prompt: 提示词
        api_key: API密钥，优先使用参数传入的值
        model: 模型名称，优先使用参数传入的值
        
    Returns:
        str: LLM回复内容
    """    
    # LLM API端点
    api_url = "https://api.deepseek.com/chat/completions"
    
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
        # 发送请求
        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        logging.info("call LLM with %s bytes and got %s bytes", len(response.request.body), len(response.content))
        response.raise_for_status()  # 检查HTTP错误
        
        # 解析响应
        result = response.json()
        
        # 提取回复内容
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            raise ValueError(f"无效的API响应: {json.dumps(result)}")
            
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API请求失败: {str(e)}")
    except json.JSONDecodeError:
        raise ValueError(f"无法解析API响应: {response.text}")
    except Exception as e:
        raise RuntimeError(f"调用LLM时出错: {str(e)}")
