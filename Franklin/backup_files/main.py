# main.py
from search_module import search_papers, Paper, SearchError
from analysis_module import analyze_paper
from translation_module import translate_abstract

def main():
    print("--- Starting Project Pauling Test Run (v2 with Structured Analysis) ---")
    search_term = "AI in drug discovery"
    
    try:
        print(f"🔍 Searching for papers with query: '{search_term}'...")
        papers = search_papers(query=search_term, limit=1) # 只测试一篇，节省时间和API调用

        if not papers:
            print("✅ No papers found.")
            return

        print(f"✅ Found {len(papers)} paper(s). Now starting analysis...")

        for paper in papers:
            print(f"\n--- Analyzing: '{paper.title[:60]}...' ---")
            mode_to_test = "Qwen/Qwen3-235B-A22B-Thinking-2507"  # 选择一个模型进行测试
            print(f"Using model: {mode_to_test}")
            
            # 步骤1: 分析论文
            analyzed_paper = analyze_paper(paper, lang="en", model_name=mode_to_test)
            print(f"  Analysis Status: {analyzed_paper.status}")
            
            # 步骤2: 翻译摘要（如果分析成功）
            if analyzed_paper.status == 'ANALYZED':
                print("  🔄 Translating abstract...")
                translated_paper = translate_abstract(analyzed_paper, model_name="Qwen/Qwen2.5-72B-Instruct")
                
                # 输出分析结果
                if translated_paper.analysis_result:
                    result = translated_paper.analysis_result
                    print("  ✅ Analysis successful. Structured data:")
                    print(f"    - Contribution: {result.contribution[:80]}...")
                    print(f"    - Novelty Score: {'★' * result.novelty}{'☆' * (5 - result.novelty)}")
                    print(f"    - Biological Impact: {'★' * result.biological_impact}{'☆' * (5 - result.biological_impact)}")
                    print(f"    - Technical Innovation: {'★' * result.technical_innovation}{'☆' * (5 - result.technical_innovation)}")
                
                # 输出翻译结果
                if translated_paper.translated_abstract:
                    print("  ✅ Translation successful:")
                    print(f"    - 原文摘要: {translated_paper.abstract[:100]}...")
                    print(f"    - 中文翻译: {translated_paper.translated_abstract[:100]}...")
                else:
                    print("  ⚠️ Translation failed or skipped")
            
            # 如果分析失败，打印错误信息
            else:
                print(f"  ❌ Analysis failed: {analyzed_paper.error_message}")

    except SearchError as e:
        print(f"❌ An error occurred during the search: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    
    finally:
        print("\n--- Test Run Finished ---")

if __name__ == "__main__":
    main()
