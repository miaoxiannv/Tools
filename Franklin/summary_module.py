# summary_module.py
"""
总结模块 - Linus式设计

核心原则：简洁、直接、无废话
"好品味意味着让特殊情况消失"
"""

import os
import json
import openai
from typing import List, Optional
from search_module import Paper


class SummaryError(Exception):
    """总结专用异常 - 统一错误处理"""
    pass


# 生物学专业总结提示词模板
SUMMARY_PROMPT = """You are an expert biological research analyst. Based on the analyzed papers below, write a comprehensive summary explaining why these papers were selected and their collective significance in biological research.

Query: "{query}"
Keywords used: {keywords}

Papers analyzed:
{papers_info}

Please provide a summary that includes:
1. Why these specific papers were selected based on the query
2. Common themes and research directions across the papers
3. Biological significance and potential impact
4. How these papers contribute to the field
5. Any emerging trends or patterns observed

Write in Chinese, be professional and insightful. Focus on biological and biomedical relevance.

Return only the summary text, no additional formatting."""


def _format_papers_for_summary(papers: List[Paper]) -> str:
    """格式化论文信息用于总结"""
    papers_info = []
    
    for i, paper in enumerate(papers, 1):
        info = f"论文 {i}:\n"
        info += f"标题: {paper.title}\n"
        info += f"DOI: {paper.doi}\n"
        
        if paper.analysis_result:
            result = paper.analysis_result
            info += f"核心贡献: {result.contribution}\n"
            info += f"新颖性: {result.novelty}/5\n"
            info += f"生物影响: {result.biological_impact}/5\n"
            info += f"技术创新: {result.technical_innovation}/5\n"
        
        if paper.translated_abstract:
            info += f"中文摘要: {paper.translated_abstract[:200]}...\n"
        
        papers_info.append(info)
    
    return "\n".join(papers_info)


def _call_summary_api(query: str, keywords: List[str], papers: List[Paper], 
                     model: str, api_key: str) -> str:
    """核心总结API调用 - 单一职责"""
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.siliconflow.cn/v1"
    )
    
    papers_info = _format_papers_for_summary(papers)
    keywords_str = ", ".join(keywords)
    
    prompt = SUMMARY_PROMPT.format(
        query=query,
        keywords=keywords_str,
        papers_info=papers_info
    )
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10240,
        temperature=0.3
    )
    
    summary = response.choices[0].message.content.strip()
    
    if not summary:
        raise SummaryError("总结结果为空")
    
    return summary


def generate_summary(query: str, keywords: List[str], papers: List[Paper],
                    model_name: str = "deepseek/DeepSeek-R1") -> str:
    """
    生成论文总结 - 主要接口
    
    Args:
        query: 原始查询
        keywords: 提取的关键词
        papers: 分析后的论文列表
        model_name: 模型名称
        
    Returns:
        总结文本
        
    Raises:
        SummaryError: 总结失败
    """
    # 快速失败验证
    api_key = os.environ.get("SILICONFLOW_API_KEY")
    if not api_key:
        raise SummaryError("SILICONFLOW_API_KEY未设置")
    
    if not papers:
        raise SummaryError("没有论文可总结")
    
    if not keywords:
        keywords = ["生物学研究"]  # 默认关键词
    
    # 执行总结
    try:
        summary = _call_summary_api(query, keywords, papers, model_name, api_key)
        return summary
        
    except Exception as e:
        raise SummaryError(f"总结失败: {e}")