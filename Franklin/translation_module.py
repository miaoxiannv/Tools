# translation_module.py
"""
翻译模块 - Linus式设计

核心原则：简洁、直接、无废话
"好品味意味着让特殊情况消失"
"""

import os
import json
import openai
from typing import Optional
from search_module import Paper


class TranslationError(Exception):
    """翻译专用异常 - 统一错误处理"""
    pass


# 简洁的翻译提示词
TRANSLATION_PROMPT = """Translate this scientific abstract to Chinese. Keep technical terms accurate and maintain academic tone.

Abstract: "{text}"

Return only the Chinese translation, no explanations or additional text."""


def _call_translation_api(text: str, api_key: str, model: str = "deepseek/DeepSeek-R1") -> str:
    """核心翻译API调用 - 单一职责"""
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.siliconflow.cn/v1"
    )
    
    prompt = TRANSLATION_PROMPT.format(text=text)
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.0
    )
    
    translation = response.choices[0].message.content.strip()
    
    if not translation:
        raise TranslationError("翻译结果为空")
    
    return translation


def translate_abstract(paper: Paper, 
                      target_lang: str = "zh", 
                      model_name: str = "deepseek/DeepSeek-R1") -> Paper:
    """
    翻译论文摘要 - 主要接口
    
    Args:
        paper: 论文对象
        target_lang: 目标语言（保持兼容性，当前只支持中文）
        model_name: 翻译模型名称
        
    Returns:
        更新后的论文对象
    """
    # 快速失败验证
    api_key = os.environ.get("SILICONFLOW_API_KEY")
    if not api_key:
        paper.error_message = "SILICONFLOW_API_KEY未设置，无法翻译"
        return paper
    
    if not paper.abstract or not paper.abstract.strip():
        paper.error_message = "论文无摘要，无法翻译"
        return paper
    
    # 如果已经翻译过，直接返回
    if paper.translated_abstract:
        return paper
    
    # 执行翻译
    try:
        translated_text = _call_translation_api(paper.abstract, api_key, model_name)
        paper.translated_abstract = translated_text
        
        # 清除可能的错误信息
        if paper.error_message and "翻译" in paper.error_message:
            paper.error_message = None
            
    except Exception as e:
        error_msg = f"翻译失败: {e}"
        if paper.error_message:
            paper.error_message += f"; {error_msg}"
        else:
            paper.error_message = error_msg
    
    return paper


# 向后兼容接口
def translate_paper_abstract(paper: Paper, lang: str = "zh") -> Paper:
    """向后兼容的翻译接口"""
    return translate_abstract(paper, lang)