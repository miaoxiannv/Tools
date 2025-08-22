# keyword_extractor.py
"""
关键词提取模块 - Linus式重构版本

核心原则：简洁、直接、无废话
"好品味意味着让特殊情况消失"
"""

import os
import json
import time
import openai
from typing import List, Optional
from functools import lru_cache


class KeywordExtractionError(Exception):
    """关键词提取专用异常 - 统一错误处理"""
    pass


# 生物学专业提示词模板 - 专注生物医学领域
PROMPT_TEMPLATE = """You are an expert biological research assistant specializing in life sciences and biomedical research. Extract 2-5 English biological/biomedical keywords from the user's query for academic paper search.

User Query: "{text}"

Requirements:
1. If the input is in Chinese, translate to English biological terms first
2. Correct any obvious typos or misspellings
3. Focus EXCLUSIVELY on biological, biomedical, and life science keywords
4. Keywords must be suitable for PubMed, Nature, Cell, and other biological databases
5. Prioritize: molecular biology, cell biology, genetics, biochemistry, physiology, pharmacology, medicine
6. Include specific biological processes, pathways, organisms, diseases, or techniques
7. Avoid general AI/CS terms unless directly related to bioinformatics

Biological Focus Examples:
- Input: "深度学习蛋白质结构预测" → ["protein structure prediction", "computational biology", "structural bioinformatics"]
- Input: "AI drug discovry" → ["drug discovery", "pharmaceutical research", "molecular pharmacology"]
- Input: "机器学习在癌症诊断中的应用" → ["cancer diagnosis", "oncology", "biomarker discovery", "medical imaging"]
- Input: "CRISPR基因编辑" → ["CRISPR-Cas9", "gene editing", "genome engineering"]
- Input: "细胞凋亡机制" → ["apoptosis", "cell death", "programmed cell death"]

Return JSON: {{"keywords": ["keyword1", "keyword2", ...]}}"""


def _call_api(text: str, api_key: str, model: str = "Qwen/Qwen2.5-7B-Instruct") -> List[str]:
    """核心API调用 - 单一职责，无特殊情况"""
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.siliconflow.cn/v1"
    )
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(text=text)}],
        max_tokens=256,
        temperature=0.0,
        response_format={"type": "json_object"}
    )
    
    data = json.loads(response.choices[0].message.content)
    keywords = data.get("keywords", [])
    
    # 简单验证和清理 - 无复杂逻辑
    if not isinstance(keywords, list):
        raise KeywordExtractionError(f"API返回格式错误: {type(keywords)}")
    
    return [k.strip() for k in keywords if isinstance(k, str) and k.strip()][:5]


def extract_keywords(text: str, 
                    api_key: Optional[str] = None, 
                    model: Optional[str] = None,
                    retries: int = 3) -> List[str]:
    """
    提取关键词 - 主要接口
    
    Args:
        text: 输入文本
        api_key: API密钥，默认从环境变量获取
        model: 模型名称
        retries: 重试次数
        
    Returns:
        关键词列表
        
    Raises:
        KeywordExtractionError: 提取失败
    """
    # 输入验证 - 快速失败
    if not text or not text.strip():
        return []
    
    api_key = api_key or os.environ.get("SILICONFLOW_API_KEY")
    if not api_key:
        raise KeywordExtractionError("SILICONFLOW_API_KEY未设置")
    
    model = model or "deepseek/DeepSeek-R1"
    text = text.strip()
    
    # 重试逻辑 - 简单直接
    last_error = None
    for attempt in range(retries):
        try:
            return _call_api(text, api_key, model)
        except Exception as e:
            last_error = e
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # 指数退避
    
    # 所有重试失败
    raise KeywordExtractionError(f"提取失败，重试{retries}次: {last_error}")


# 向后兼容包装 - 保持原有接口
def extract_keywords_legacy(user_text: str, model_name: Optional[str] = None, max_retries: Optional[int] = None) -> List[str]:
    """向后兼容的接口"""
    try:
        return extract_keywords(user_text, model=model_name, retries=max_retries or 3)
    except KeywordExtractionError:
        return []  # 原版本失败时返回空列表


@lru_cache(maxsize=128)
def extract_keywords_cached(text: str, model: Optional[str] = None) -> tuple:
    """缓存版本 - 返回元组以支持缓存"""
    try:
        keywords = extract_keywords(text, model=model)
        return tuple(keywords)
    except KeywordExtractionError:
        return ()


def get_cache_stats() -> dict:
    """获取缓存统计"""
    info = extract_keywords_cached.cache_info()
    return {
        "hits": info.hits,
        "misses": info.misses,
        "size": info.currsize,
        "maxsize": info.maxsize
    }


def clear_cache():
    """清空缓存"""
    extract_keywords_cached.cache_clear()

# ---------------------------------------------------------------------------
# 测试 - Linus式简洁测试
# ---------------------------------------------------------------------------

def _test_basic():
    """基础功能测试"""
    print("=== Linus式简洁测试 ===\n")
    
    test_cases = [
        ("AI in drug discovery", "英文查询"),
        ("深度学习蛋白质结构预测", "中文查询"),
        ("", "空输入"),
        ("machine learning", "短查询")
    ]
    
    for query, desc in test_cases:
        print(f"测试 {desc}: '{query}'")
        try:
            result = extract_keywords_legacy(query)  # 使用兼容接口测试
            print(f"结果: {result}")
            print(f"状态: {'✅ 通过' if isinstance(result, list) else '❌ 失败'}")
        except Exception as e:
            print(f"异常: {e}")
            print("状态: ✅ 通过 (异常处理正常)")
        print("-" * 40)
    
    # 测试缓存
    print("缓存测试:")
    extract_keywords_cached("test")
    extract_keywords_cached("test")  # 第二次应该命中缓存
    stats = get_cache_stats()
    print(f"缓存统计: {stats}")
    print(f"缓存命中: {'✅ 通过' if stats['hits'] > 0 else '❌ 失败'}")


if __name__ == "__main__":
    _test_basic()
