import os
import json
import requests
import logging
from typing import List, Dict, Any, Optional

def analyze_commit(commits, api_key=None, model=None):
    """分析提交内容，使用LLM提供洞察
    
    Args:
        commits: GitHub提交对象列表
        api_key: OpenRouter API密钥，优先使用参数传入的值
        model: 模型名称，优先使用参数传入的值
        
    Returns:
        str: LLM分析结果
    """
    if not commits:
        return "没有提交可供分析"
    
    if api_key is None:
        error_msg = "未提供OpenRouter API密钥，请通过--api-key参数或OPENROUTER_API_KEY环境变量设置"
        logging.error(error_msg)
        return error_msg

    if model is None:
        logging.warning("未提供OpenRouter模型，使用默认模型: deepseek/deepseek-chat-v3-0324")
        model = "deepseek/deepseek-chat-v3-0324"

    result = ""    
    for commit in commits:
        logging.info(f"分析提交: {commit.sha}")
        prompt = "请分析以下Git提交，总结主要变更，识别关键功能修改，并指出潜在的重要更新：\n\n"
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
    
        # 添加分析要求
        prompt += """请提供以下分析：
此次更新的重要程度（低/中/高）以及200字以内的内容总结

请用中文回答，格式清晰。"""
        logging.debug("=" * 40)
        logging.debug("LLM提示词:")
        logging.debug(prompt)
        logging.debug("-" * 40)
    
        # 调用LLM进行分析
        try:
            output = call_openrouter(prompt, api_key=api_key, model=model)
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

def call_openrouter(prompt: str, api_key: str = None, model: str = None) -> str:
    """调用OpenRouter API获取LLM回复
    
    Args:
        prompt: 提示词
        api_key: OpenRouter API密钥，优先使用参数传入的值
        model: 模型名称，优先使用参数传入的值
        
    Returns:
        str: LLM回复内容
    """    
    # OpenRouter API端点
    api_url = "https://openrouter.ai/api/v1/chat/completions"
    
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
            {"role": "system", "content": "你是一位专业的代码审查专家和Git提交分析师。你擅长分析代码变更，提取关键信息，并提供简洁明了的总结。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 1.0,  # 较低的温度使输出更确定性
        "max_tokens": 1000   # 限制回复长度
    }
    
    try:
        # 发送请求
        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        logging.info("call openrouter with %s bytes and got %s bytes", len(response.request.body), len(response.content))
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
        raise RuntimeError(f"调用OpenRouter时出错: {str(e)}")
