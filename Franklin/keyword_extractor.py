import os
import json
import time
import openai
from typing import List, Optional
from functools import lru_cache

class KeywordExtractionError(Exception):
    pass

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
    
    if not isinstance(keywords, list):
        raise KeywordExtractionError(f"API返回格式错误: {type(keywords)}")
    
    return [k.strip() for k in keywords if isinstance(k, str) and k.strip()][:5]

def extract_keywords(text: str, 
                    api_key: Optional[str] = None, 
                    model: Optional[str] = None,
                    retries: int = 3) -> List[str]:
    if not text or not text.strip():
        return []
    
    api_key = api_key or os.environ.get("SILICONFLOW_API_KEY")
    if not api_key:
        raise KeywordExtractionError("SILICONFLOW_API_KEY未设置")
    
    model = model or "deepseek/DeepSeek-R1"
    text = text.strip()
    
    last_error = None
    for attempt in range(retries):
        try:
            return _call_api(text, api_key, model)
        except Exception as e:
            last_error = e
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    
    raise KeywordExtractionError(f"提取失败，重试{retries}次: {last_error}")

def extract_keywords_legacy(user_text: str, model_name: Optional[str] = None, max_retries: Optional[int] = None) -> List[str]:
    try:
        return extract_keywords(user_text, model=model_name, retries=max_retries or 3)
    except KeywordExtractionError:
        return []

@lru_cache(maxsize=128)
def extract_keywords_cached(text: str, model: Optional[str] = None) -> tuple:
    try:
        keywords = extract_keywords(text, model=model)
        return tuple(keywords)
    except KeywordExtractionError:
        return ()

def get_cache_stats() -> dict:
    info = extract_keywords_cached.cache_info()
    return {
        "hits": info.hits,
        "misses": info.misses,
        "size": info.currsize,
        "maxsize": info.maxsize
    }

def clear_cache():
    extract_keywords_cached.cache_clear()
