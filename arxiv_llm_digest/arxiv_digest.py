import os
import json
import argparse
import arxiv
import openai
from datetime import datetime, timedelta, timezone

# --- Language & Template Configuration ---

PROMPTS = {
    "en": {
        "system_message": "You are a helpful research assistant providing JSON output.",
        "template": """
You are a senior AI researcher specializing in Large Language Models.
Based on the title and abstract of the following paper, please perform these tasks:

**Paper Title:** {title}
**Paper Abstract:** {abstract}

**Tasks:**
1.  **Summarize the main contribution** in a single, concise sentence.
2.  **Rate its potential novelty** on a scale of 1 to 5 (1=Incremental, 3=Interesting, 5=Potential Breakthrough).

Provide your response in a valid JSON format, like this:
{{"contribution": "...", "novelty": ...}}
"""
    },
    "zh": {
        "system_message": "你是一个乐于助人的研究助理，需提供 JSON 格式的输出。",
        "template": """
你是一位专攻大型语言模型的高级AI研究员。
根据以下论文的标题和摘要，请完成以下任务：

**论文标题:** {title}
**论文摘要:** {abstract}

**任务:**
1.  **总结核心贡献**: 用一个简洁的句子总结论文的核心贡献。
2.  **评定新颖性**: 在1到5的范围内评价其潜在新颖性 (1=微创新, 3=有趣, 5=潜在突破)。

请以有效的JSON格式提供您的回答，例如：
{{"contribution": "...", "novelty": ...}}
"""
    }
}

REPORT_TEMPLATES = {
    "en": {
        "title": "# Daily arXiv LLM Digest - {report_date}",
        "summary_by": "Your daily summary of new papers on LLMs, analyzed by **{provider}**.",
        "top_recommendation": "## 🔥 Today's Top Recommendation",
        "authors": "- **Authors**: {authors}",
        "category": "- **Category**: `{category}`",
        "novelty_score": "- **Novelty Score**: `{novelty}/5`",
        "contribution": "- **Contribution**: {contribution}",
        "abstract": "**Abstract**: *{abstract}*",
        "other_papers": "---\n\n## 📚 Other Papers Today",
        "other_paper_category": "- **Category**: `{category}` | **Novelty**: `{novelty}/5`",
        "no_papers_found": "# Daily arXiv LLM Digest\n\nNo new papers found today."
    },
    "zh": {
        "title": "# arXiv LLM 每日摘要 - {report_date}",
        "summary_by": "您的 LLM 论文每日摘要，由 **{provider}** 分析。",
        "top_recommendation": "## 🔥 今日最佳推荐",
        "authors": "- **作者**: {authors}",
        "category": "- **类别**: `{category}`",
        "novelty_score": "- **新颖性评分**: `{novelty}/5`",
        "contribution": "- **核心贡献**: {contribution}",
        "abstract": "**摘要**: *{abstract}*",
        "other_papers": "---\n\n## 📚 今日其他论文",
        "other_paper_category": "- **类别**: `{category}` | **新颖性**: `{novelty}/5`",
        "no_papers_found": "# arXiv LLM 每日摘要\n\n今日未发现新论文.",
        "translation_template": "请将以下英文摘要翻译成简洁的学术中文，只返回翻译结果，不要包含任何说明或解释：\n\n{text}"
    }
}


# --- 核心功能 (Core Functions) ---

def fetch_recent_papers(search_query, max_results, days):
    """从 Arxiv 获取论文 - 支持无限搜索"""
    if days == 0:
        print(f"Fetching papers from arXiv (unlimited time range)...")
        search = arxiv.Search(
            query=search_query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        papers = []
        for result in search.results():
            papers.append(result)
            
        print(f"Found {len(papers)} papers (unlimited search).")
        return papers
    else:
        print(f"Fetching recent papers from the last {days} day(s) from arXiv...")
        start_date_utc = datetime.now(timezone.utc) - timedelta(days=days)
        
        search = arxiv.Search(
            query=search_query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        recent_papers = []
        for result in search.results():
            if result.published > start_date_utc:
                recent_papers.append(result)
                
        print(f"Found {len(recent_papers)} new papers from the last {days} day(s).")
        return recent_papers

def analyze_paper(client, model_name, paper, lang):
    """Analyze paper using SiliconFlow API"""
    print(f"  Analyzing with SiliconFlow: {paper.title[:60]}...")
    try:
        prompt = PROMPTS[lang]["template"].format(title=paper.title, abstract=paper.summary)
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
            
            md_content += f"## {idx}. [{p.title}]({p.entry_id})\n"
            md_content += f"- **链接**: [{p.entry_id}]({p.entry_id})\n"
            md_content += f"- **作者**: {', '.join(author.name for author in p.authors)}\n"
            md_content += f"- **arXiv分类**: {p.primary_category}\n"
            md_content += f"- **新颖性评分**: {a.get('novelty', 'N/A')}/5\n"
            md_content += f"- **核心贡献**: {a.get('contribution', 'N/A')}\n"
            
            # Abstract
            abstract_to_display = p.summary.replace('\n', ' ')
            if lang == 'zh':
                translated_abstract = _translate_text(p.summary, client, model_name, progress_callback)
                if translated_abstract:
                    abstract_to_display = translated_abstract.replace('\n', ' ')
            md_content += f"- **摘要**: {abstract_to_display}\n\n"
            
        except Exception as e:
            print(f"    [!] Error processing paper {idx}: {e}")
            # Add a fallback entry for this paper
            try:
                p = item['paper']
                md_content += f"## {idx}. [{p.title}]({p.entry_id})\n"
                md_content += f"- **链接**: [{p.entry_id}]({p.entry_id})\n"
                md_content += f"- **作者**: {', '.join(author.name for author in p.authors)}\n"
                md_content += f"- **arXiv分类**: {p.primary_category}\n"
                md_content += f"- **新颖性评分**: N/A/5\n"
                md_content += f"- **核心贡献**: 处理出错\n"
                md_content += f"- **摘要**: {p.summary.replace('\n', ' ')}\n\n"
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
    parser = argparse.ArgumentParser(description="Fetch and analyze recent papers from arXiv using SiliconFlow.")
    parser.add_argument("--provider", type=str, default="siliconflow", help="LLM provider (SiliconFlow only)")
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-7B-Instruct", help="Model to use")
    parser.add_argument("--max-results", type=int, default=20, help="Maximum number of papers to process")
    parser.add_argument("-d", "--days", type=int, default=2, help="Number of days back to search for papers")
    parser.add_argument("--lang", type=str, default="zh", choices=["en", "zh"], help="Language for output report")
    parser.add_argument("--category", type=str, default="cs.CL OR cs.AI OR cs.LG", help="ArXiv category to search")
    parser.add_argument("--siliconflow-api-key", type=str, default=os.getenv("SILICONFLOW_API_KEY"), help="SiliconFlow API Key")

    args = parser.parse_args()

    # Configuration - 修复arXiv查询语法
    # 将 "q-bio.QM OR q-bio.BM OR cs.LG" 转换为正确的arXiv查询格式
    categories = args.category.split(" OR ")
    category_queries = [f"cat:{cat.strip()}" for cat in categories]
    SEARCH_QUERY = " OR ".join(category_queries)
    RESULT_DIR = "result"
    
    print(f"[DEBUG] Search query: {SEARCH_QUERY}")

    if not args.siliconflow_api_key:
        raise ValueError("SiliconFlow API Key not provided. Set SILICONFLOW_API_KEY environment variable or use --siliconflow-api-key.")
    
    client = openai.OpenAI(api_key=args.siliconflow_api_key, base_url="https://api.siliconflow.cn/v1")
    model_name = args.model

    print(f"Using SiliconFlow with model: {model_name}")

    papers = fetch_recent_papers(SEARCH_QUERY, args.max_results, args.days)
    if not papers:
        print("No new papers to process. Exiting.")
        return

    analyzed_papers = []
    print_progress(f"🔍 开始分析 {len(papers)} 篇论文...", progress_callback)
    
    for i, paper in enumerate(papers, 1):
        update_progress_with_percentage(i, len(papers), f"正在分析论文", progress_callback)
        print(f"[DEBUG] Processing paper {i}/{len(papers)}: {paper.title[:60]}...")
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
