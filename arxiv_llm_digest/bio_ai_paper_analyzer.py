import os
import json
import argparse
import re
from habanero import Crossref
import openai
from datetime import datetime, timedelta, timezone

# --- Language & Template Configuration ---

PROMPTS = {
    "en": {
        "system_message": "You are an expert interdisciplinary research analyst specializing in computational biology, bioinformatics, and deep learning applications in biological sciences. You have deep expertise in both biological systems and machine learning methodologies.",
        "template": """
You are a senior interdisciplinary researcher with expertise in computational biology, bioinformatics, and deep learning applications in life sciences.

**Paper Title:** {title}
**Paper Abstract:** {abstract}

**Analysis Framework:**
Please analyze this paper through the lens of biological and deep learning integration. Consider:

**Biological Context:**
- Biological systems, processes, or phenomena addressed
- Clinical/medical relevance and translational potential
- Biological data types (genomics, proteomics, imaging, etc.)
- Experimental validation and biological significance

**Deep Learning/AI Methodology:**
- Novel architectures, algorithms, or computational approaches
- Data representation and feature engineering innovations
- Model interpretability and biological insight generation
- Scalability and computational efficiency

**Interdisciplinary Impact:**
- Cross-domain knowledge transfer and methodological innovation
- Potential to advance both biological understanding and AI capabilities
- Reproducibility and generalizability across biological systems

**Tasks:**
1. **Summarize the core contribution** focusing on the intersection of biology and deep learning
2. **Rate novelty** (1-5): 1=Incremental improvement, 3=Significant advance, 5=Paradigm-shifting breakthrough
3. **Assess biological impact** (1-5): Potential to advance biological knowledge or clinical applications
4. **Evaluate technical innovation** (1-5): Novel computational/AI methodological contributions

Provide response in JSON format:
{{"contribution": "...", "novelty": ..., "biological_impact": ..., "technical_innovation": ...}}
"""
    },
    "zh": {
        "system_message": "你是一位跨学科研究分析专家，专精于计算生物学、生物信息学以及深度学习在生物科学中的应用。你在生物系统和机器学习方法论方面都有深厚的专业知识。",
        "template": """
你是一位资深的跨学科研究员，在计算生物学、生物信息学以及深度学习在生命科学中的应用方面具有专业知识。

**论文标题:** {title}
**论文摘要:** {abstract}

**分析框架:**
请从生物学与深度学习融合的角度分析这篇论文。考虑以下方面：

**生物学背景:**
- 涉及的生物系统、过程或现象
- 临床/医学相关性和转化潜力
- 生物数据类型（基因组学、蛋白质组学、成像等）
- 实验验证和生物学意义

**深度学习/AI方法论:**
- 新颖的架构、算法或计算方法
- 数据表示和特征工程创新
- 模型可解释性和生物学洞察生成
- 可扩展性和计算效率

**跨学科影响:**
- 跨领域知识转移和方法论创新
- 推进生物学理解和AI能力的潜力
- 在生物系统中的可重现性和泛化能力

**任务:**
1. **总结核心贡献**: 重点关注生物学与深度学习的交叉点
2. **评定新颖性** (1-5): 1=渐进式改进, 3=重要进展, 5=范式转换突破
3. **评估生物学影响** (1-5): 推进生物学知识或临床应用的潜力
4. **评价技术创新** (1-5): 新颖的计算/AI方法论贡献

请以JSON格式提供回答：
{{"contribution": "...", "novelty": ..., "biological_impact": ..., "technical_innovation": ...}}
"""
    }
}

REPORT_TEMPLATES = {
    "en": {
        "title": "# Daily Crossref Research Digest - {report_date}",
        "summary_by": "Your daily summary of new papers, analyzed by **{provider}**.",
        "top_recommendation": "## 🔥 Today's Top Recommendation",
        "authors": "- **Authors**: {authors}",
        "journal": "- **Journal**: {journal}",
        "year": "- **Year**: {year}",
        "doi": "- **DOI**: {doi}",
        "url": "- **URL**: {url}",
        "keywords": "- **Keywords**: {keywords}",
        "novelty_score": "- **Novelty Score**: `{novelty}/5`",
        "contribution": "- **Contribution**: {contribution}",
        "abstract": "**Abstract**: *{abstract}*",
        "other_papers": "---\n\n## 📚 Other Papers Today",
        "other_paper_info": "- **Journal**: `{journal}` | **Year**: `{year}` | **Novelty**: `{novelty}/5`",
        "no_papers_found": "# Daily Crossref Research Digest\n\nNo new papers found today."
    },
    "zh": {
        "title": "# Crossref 研究论文每日摘要 - {report_date}",
        "summary_by": "您的研究论文每日摘要，由 **{provider}** 分析。",
        "top_recommendation": "## 🔥 今日最佳推荐",
        "authors": "- **作者**: {authors}",
        "journal": "- **期刊**: {journal}",
        "year": "- **年份**: {year}",
        "doi": "- **DOI**: {doi}",
        "url": "- **链接**: {url}",
        "keywords": "- **关键字**: {keywords}",
        "novelty_score": "- **新颖性评分**: `{novelty}/5`",
        "contribution": "- **核心贡献**: {contribution}",
        "abstract": "**摘要**: *{abstract}*",
        "other_papers": "---\n\n## 📚 今日其他论文",
        "other_paper_info": "- **期刊**: `{journal}` | **年份**: `{year}` | **新颖性**: `{novelty}/5`",
        "no_papers_found": "# Crossref 研究论文每日摘要\n\n今日未发现新论文.",
        "translation_template": "请将以下英文摘要翻译成简洁的学术中文，只返回翻译结果，不要包含任何说明或解释：\n\n{text}"
    }
}


# --- 核心功能 (Core Functions) ---

def clean_html(raw_html):
    """一个简单的函数，用于移除HTML/XML标签。"""
    if not raw_html:
        return ""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def fetch_recent_papers(search_query, max_results, days, other_filters=None):
    """从 Crossref 获取论文 - 支持时间范围搜索"""
    print(f"🚀 正在搜索关于 '{search_query}' 且必须包含摘要的文章...")
    
    # 1. 准备过滤器
    filter_params = other_filters.copy() if other_filters else {}
    filter_params['has-abstract'] = True
    
    # 2. 如果指定了天数，添加时间过滤器
    if days > 0:
        start_date = datetime.now() - timedelta(days=days)
        filter_params['from-pub-date'] = start_date.strftime('%Y-%m-%d')
        print(f"搜索最近 {days} 天的论文（从 {start_date.strftime('%Y-%m-%d')} 开始）...")
    else:
        print("搜索所有时期的论文...")
    
    try:
        # 3. 初始化 Crossref 客户端
        cr = Crossref()

        # 4. 执行 .works() 查询
        results = cr.works(query=search_query, limit=max_results, filter=filter_params)

        # 5. 检查返回结果
        if results['status'] == 'ok' and results['message']['items']:
            items = results['message']['items']
            print(f"✅ 成功找到 {len(items)} 篇包含摘要的文章")
            
            # 6. 转换为统一格式
            papers = []
            for item in items:
                paper = {
                    'title': item.get('title', ['无标题'])[0],
                    'authors': [f"{author.get('given', '')} {author.get('family', '')}".strip() 
                               for author in item.get('author', [])],
                    'abstract': clean_html(item.get('abstract', '')),
                    'doi': item.get('DOI', 'N/A'),
                    'url': item.get('URL', 'N/A'),
                    'journal': item.get('container-title', ['未知期刊'])[0],
                    'keywords': item.get('subject', []),
                    'published_date': item.get('published-print', item.get('published-online', {})),
                    'raw_item': item  # 保存原始数据以备后用
                }
                
                # 处理发布日期
                published_info = paper['published_date']
                date_parts = published_info.get('date-parts', [[None]])
                paper['year'] = date_parts[0][0] if date_parts and date_parts[0][0] else 'N/A'
                
                papers.append(paper)
            
            return papers
        else:
            print(f"❌ 未能找到关于 '{search_query}' 且包含摘要的文章。请尝试其他关键词。")
            return []

    except Exception as e:
        print(f"发生严重错误: {e}")
        return []

def analyze_paper(client, model_name, paper, lang):
    """Analyze paper using SiliconFlow API"""
    print(f"  Analyzing with SiliconFlow: {paper['title'][:60]}...")
    try:
        prompt = PROMPTS[lang]["template"].format(title=paper['title'], abstract=paper['abstract'])
        system_message = PROMPTS[lang]["system_message"]
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse JSON response
        analysis = json.loads(response.choices[0].message.content)
        
        # Ensure analysis is a dictionary and has required fields
        if not isinstance(analysis, dict):
            print(f"    [!] Warning: Analysis result is not a dictionary, got {type(analysis)}")
            return {"contribution": "Analysis failed", "novelty": 1}
        
        # Ensure required fields exist
        if "contribution" not in analysis:
            analysis["contribution"] = "No contribution analysis available"
        if "novelty" not in analysis:
            analysis["novelty"] = 1
            
        return analysis
        
    except json.JSONDecodeError as e:
        print(f"    [!] JSON decode error: {e}")
        return {"contribution": "JSON parsing failed", "novelty": 1}
    except Exception as e:
        print(f"    [!] Error analyzing paper: {e}")
        return {"contribution": "Analysis failed", "novelty": 1}

def _translate_text(text, client, model_name, progress_callback=None):
    """Translate text to Chinese using SiliconFlow"""
    if progress_callback:
        progress_callback("🌐 正在翻译摘要...")
    print("  Translating abstract to Chinese...")
    prompt = REPORT_TEMPLATES["zh"]["translation_template"].format(text=text)
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "你是一个专业的翻译助手。请将英文翻译成简洁的学术中文，只返回翻译结果，不要包含任何解释、说明或格式标记。"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"    [!] Error translating text: {e}")
        return None

def generate_markdown_report(analyzed_papers, provider, lang, client, model_name, progress_callback=None):
    """生成 Markdown 格式的报告"""
    template = REPORT_TEMPLATES[lang]
    if not analyzed_papers:
        return template["no_papers_found"]

    # Safe sorting with error handling
    def safe_get_novelty(x):
        try:
            analysis = x.get('analysis', {})
            if isinstance(analysis, dict):
                return analysis.get('novelty', 0)
            else:
                print(f"    [!] Warning: Analysis is not a dict for paper, got {type(analysis)}")
                return 0
        except Exception as e:
            print(f"    [!] Error getting novelty: {e}")
            return 0
    
    analyzed_papers.sort(key=safe_get_novelty, reverse=True)
    report_date = datetime.now().strftime("%Y-%m-%d")
    md_content = template["title"].format(report_date=report_date) + "\n\n"
    md_content += template["summary_by"].format(provider=provider) + "\n\n"

    for idx, item in enumerate(analyzed_papers, 1):
        try:
            p = item['paper']
            a = item['analysis']
            
            # Ensure analysis is a dictionary
            if not isinstance(a, dict):
                print(f"    [!] Warning: Analysis for paper {idx} is not a dict, got {type(a)}")
                a = {"contribution": "Analysis format error", "novelty": 1}
            
            md_content += f"## {idx}. [{p['title']}]({p['url']})\n"
            md_content += f"- **链接**: [{p['doi']}]({p['url']})\n"
            md_content += f"- **作者**: {', '.join(p['authors'])}\n"
            md_content += f"- **期刊**: {p['journal']}\n"
            md_content += f"- **年份**: {p['year']}\n"
            md_content += f"- **DOI**: {p['doi']}\n"
            if p['keywords']:
                md_content += f"- **关键字**: {', '.join(p['keywords'])}\n"
            md_content += f"- **新颖性评分**: {a.get('novelty', 'N/A')}/5\n"
            # 添加新的评分维度
            if 'biological_impact' in a:
                md_content += f"- **生物学影响**: {a.get('biological_impact', 'N/A')}/5\n"
            if 'technical_innovation' in a:
                md_content += f"- **技术创新**: {a.get('technical_innovation', 'N/A')}/5\n"
            md_content += f"- **核心贡献**: {a.get('contribution', 'N/A')}\n"
            
            # Abstract
            abstract_to_display = p['abstract'].replace('\n', ' ')
            if lang == 'zh' and abstract_to_display and abstract_to_display.strip():
                print(f"    [DEBUG] Translating abstract for paper {idx}...")
                translated_abstract = _translate_text(p['abstract'], client, model_name, progress_callback)
                if translated_abstract and translated_abstract.strip():
                    print(f"    [DEBUG] Translation successful for paper {idx}")
                    abstract_to_display = translated_abstract.replace('\n', ' ')
                else:
                    print(f"    [DEBUG] Translation failed for paper {idx}, using original")
            md_content += f"- **摘要**: {abstract_to_display}\n\n"
            
        except Exception as e:
            print(f"    [!] Error processing paper {idx}: {e}")
            # Add a fallback entry for this paper
            try:
                p = item['paper']
                md_content += f"## {idx}. [{p['title']}]({p['url']})\n"
                md_content += f"- **链接**: [{p['doi']}]({p['url']})\n"
                md_content += f"- **作者**: {', '.join(p['authors'])}\n"
                md_content += f"- **期刊**: {p['journal']}\n"
                md_content += f"- **年份**: {p['year']}\n"
                md_content += f"- **新颖性评分**: N/A/5\n"
                md_content += f"- **核心贡献**: 处理出错\n"
                md_content += f"- **摘要**: {p['abstract'].replace('\n', ' ')}\n\n"
            except Exception as e2:
                print(f"    [!] Error creating fallback entry for paper {idx}: {e2}")
                md_content += f"## {idx}. 论文处理出错\n\n"
    
    return md_content

def print_progress(message, callback=None):
    """打印进度信息"""
    print(message)
    if callback:
        callback(message)

def update_progress_with_percentage(current, total, message, callback=None):
    """更新带百分比的进度信息"""
    progress_msg = f"{message} ({current}/{total})"
    print(progress_msg)
    if callback:
        callback(progress_msg)

def main(progress_callback=None):
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Fetch and analyze recent papers from Crossref using SiliconFlow.")
    parser.add_argument("--provider", type=str, default="siliconflow", help="LLM provider (SiliconFlow only)")
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-7B-Instruct", help="Model to use")
    parser.add_argument("--max-results", type=int, default=20, help="Maximum number of papers to process")
    parser.add_argument("-d", "--days", type=int, default=2, help="Number of days back to search for papers (set 0 for unlimited)")
    parser.add_argument("--lang", type=str, default="zh", choices=["en", "zh"], help="Language for output report")
    parser.add_argument("--query", type=str, default="machine learning", help="Search query for Crossref")
    parser.add_argument("--siliconflow-api-key", type=str, default=os.getenv("SILICONFLOW_API_KEY"), help="SiliconFlow API Key")

    args = parser.parse_args()

    # Configuration
    SEARCH_QUERY = args.query
    RESULT_DIR = "result"
    
    print(f"[DEBUG] Search query: {SEARCH_QUERY}")

    if not args.siliconflow_api_key:
        raise ValueError("SiliconFlow API Key not provided. Set SILICONFLOW_API_KEY environment variable or use --siliconflow-api-key.")
    
    client = openai.OpenAI(api_key=args.siliconflow_api_key, base_url="https://api.siliconflow.cn/v1")
    model_name = args.model

    print(f"Using SiliconFlow with model: {model_name}")

    # 添加其他过滤器（可以根据需要调整）
    additional_filters = {
        'type': 'journal-article'
    }

    papers = fetch_recent_papers(SEARCH_QUERY, args.max_results, args.days, additional_filters)
    if not papers:
        print("No new papers to process. Exiting.")
        return

    analyzed_papers = []
    print_progress(f"🔍 开始分析 {len(papers)} 篇论文...", progress_callback)
    
    for i, paper in enumerate(papers, 1):
        update_progress_with_percentage(i, len(papers), f"正在分析论文", progress_callback)
        print(f"[DEBUG] Processing paper {i}/{len(papers)}: {paper['title'][:60]}...")
        analysis = analyze_paper(client, model_name, paper, args.lang)
        if analysis:
            print(f"[DEBUG] Successfully analyzed paper {i}")
            analyzed_papers.append({"paper": paper, "analysis": analysis})
        else:
            print(f"[DEBUG] Failed to analyze paper {i}")
    
    print_progress(f"✅ 成功分析了 {len(analyzed_papers)}/{len(papers)} 篇论文", progress_callback)
    
    report = generate_markdown_report(analyzed_papers, args.provider, args.lang, client, model_name, progress_callback)

    # Save to result folder only
    if not os.path.exists(RESULT_DIR):
        print_progress("📁 创建结果目录...", progress_callback)
        os.makedirs(RESULT_DIR)
    
    report_date = datetime.now().strftime("%Y-%m-%d")
    result_filename = os.path.join(RESULT_DIR, f"digest_{report_date}.md")
    print_progress("📝 正在保存报告...", progress_callback)
    with open(result_filename, "w", encoding="utf-8") as f:
        f.write(report)
        
    success_message = f"\n✅ 摘要报告生成成功！\n📊 报告已保存到: {result_filename}"
    print_progress(success_message, progress_callback)
    
    if analyzed_papers:
        print_progress("\n🌟 今日推荐论文", progress_callback)
        recommendation_part = report.split("---")[0]
        print_progress(recommendation_part, progress_callback)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
