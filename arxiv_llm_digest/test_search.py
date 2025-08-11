import arxiv

def test_search_query():
    """测试搜索查询是否能找到正确的论文分类"""
    
    # 测试不同的查询格式
    queries = [
        "cat:q-bio.QM OR cat:q-bio.BM OR cat:cs.LG",  # 修复后的格式
        "cat:cs.CL OR cat:cs.AI OR cat:cs.LG",        # LLM相关
        "cat:q-bio.QM",                               # 单个分类测试
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n=== 测试查询 {i}: {query} ===")
        
        try:
            search = arxiv.Search(
                query=query,
                max_results=3,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            papers = list(search.results())
            print(f"找到 {len(papers)} 篇论文:")
            
            for j, paper in enumerate(papers, 1):
                print(f"  {j}. 标题: {paper.title[:60]}...")
                print(f"     分类: {paper.primary_category}")
                print(f"     所有分类: {[cat for cat in paper.categories]}")
                print(f"     发布日期: {paper.published.strftime('%Y-%m-%d')}")
                print()
                
        except Exception as e:
            print(f"查询出错: {e}")

if __name__ == "__main__":
    test_search_query()
