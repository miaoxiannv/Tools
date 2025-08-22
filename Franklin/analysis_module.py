import os
import json
import openai
from typing import Optional
from search_module import Paper, AnalysisResult

class AnalysisError(Exception):
    pass

ANALYSIS_PROMPT = """You are an expert biological research reviewer specializing in life sciences and biomedical research. Analyze this biological/biomedical paper and provide a comprehensive evaluation.

Title: "{title}"
Abstract: "{abstract}"

Evaluation Criteria (Biology-focused):
1. BIOLOGICAL CONTRIBUTION: What new biological knowledge, mechanism, or discovery does this work provide?
2. NOVELTY: How novel is this biological finding or approach? (1=known mechanism, 3=new application, 5=paradigm shift)
3. BIOLOGICAL IMPACT: What is the potential impact on biological understanding, human health, or disease treatment?
4. TECHNICAL INNOVATION: How innovative are the biological methods, techniques, or experimental approaches?

Scoring Guidelines:
- Novelty: 1=incremental improvement, 2=modest advance, 3=significant finding, 4=major breakthrough, 5=paradigm-shifting discovery
- Biological Impact: 1=limited scope, 2=field-specific, 3=broad biological relevance, 4=clinical potential, 5=transformative for medicine/biology
- Technical Innovation: 1=standard methods, 2=improved protocols, 3=novel techniques, 4=breakthrough methodology, 5=revolutionary approach

Focus on biological significance, clinical relevance, mechanistic insights, and potential therapeutic applications.

Return only this JSON structure:
{{
    "contribution": "Brief summary of core biological contribution and significance",
    "novelty": <1-5 integer>,
    "biological_impact": <1-5 integer>, 
    "technical_innovation": <1-5 integer>
}}"""

def _call_analysis_api(title: str, abstract: str, model: str, api_key: str) -> dict:
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.siliconflow.cn/v1"
    )
    
    prompt = ANALYSIS_PROMPT.format(title=title, abstract=abstract)
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.0,
        response_format={"type": "json_object"}
    )
    
    data = json.loads(response.choices[0].message.content)
    
    required_keys = ["contribution", "novelty", "biological_impact", "technical_innovation"]
    for key in required_keys:
        if key not in data:
            raise AnalysisError(f"缺少必需字段: {key}")
    
    return data

def analyze_paper(paper: Paper, 
                 lang: str = "en", 
                 model_name: str = "deepseek-ai/DeepSeek-R1") -> Paper:
    api_key = os.environ.get("SILICONFLOW_API_KEY")
    if not api_key:
        paper.status = 'ANALYSIS_FAILED'
        paper.error_message = "SILICONFLOW_API_KEY未设置"
        return paper
    
    if not paper.abstract or not paper.abstract.strip():
        paper.status = 'ANALYSIS_SKIPPED'
        paper.error_message = "论文无摘要"
        return paper
    
    paper.status = 'ANALYZING'
    
    try:
        data = _call_analysis_api(paper.title, paper.abstract, model_name, api_key)
        
        paper.analysis_result = AnalysisResult(
            contribution=str(data['contribution']),
            novelty=int(data['novelty']),
            biological_impact=int(data['biological_impact']),
            technical_innovation=int(data['technical_innovation'])
        )
        
        paper.status = 'ANALYZED'
        paper.error_message = None
        
    except Exception as e:
        paper.status = 'ANALYSIS_FAILED'
        paper.error_message = f"分析失败: {e}"
    
    return paper

def analyze_paper_legacy(paper: Paper, lang: str = "en", model_name: str = "deepseek/DeepSeek-R1") -> Paper:
    return analyze_paper(paper, lang, model_name)
