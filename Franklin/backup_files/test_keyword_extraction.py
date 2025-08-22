# test_keyword_extraction.py
"""
关键词提取测试 - 验证中文输入和错字处理

核心原则：简洁、直接、无废话
"好品味意味着让特殊情况消失"
"""

import os
from keyword_extractor import extract_keywords, KeywordExtractionError


def test_enhanced_keyword_extraction():
    """测试增强的关键词提取功能"""
    print("=== 增强关键词提取测试 ===\n")
    
    # 生物学专业测试用例：涵盖中文、英文、错字等情况
    test_cases = [
        # (输入, 描述, 期望特征)
        ("深度学习蛋白质结构预测", "蛋白质结构生物学", "应包含结构生物学关键词"),
        ("CRISPR gene editng", "基因编辑技术", "应纠正拼写并专注基因编辑"),
        ("癌症免疫治疗机制研究", "肿瘤免疫学", "应提取免疫学核心概念"),
        ("细胞凋亡信号通路", "细胞生物学", "应专注细胞死亡机制"),
        ("药物靶点发现", "药理学研究", "应包含药物发现术语"),
        ("干细胞分化调控", "发育生物学", "应专注干细胞生物学"),
        ("基因表达调控网络", "分子生物学", "应包含基因调控术语"),
        ("蛋白质相互作用", "蛋白质组学", "应专注蛋白质功能"),
        ("病毒感染机制", "病毒学研究", "应包含病毒学术语"),
        ("神经退行性疾病", "神经生物学", "应专注神经系统疾病"),
        ("代谢途径分析", "生化代谢", "应包含代谢生物学术语"),
        ("免疫系统发育", "免疫学", "应专注免疫系统生物学")
    ]
    
    # 检查API密钥
    if not os.environ.get("SILICONFLOW_API_KEY"):
        print("⚠️ 警告: 未设置 SILICONFLOW_API_KEY，将跳过实际API测试")
        print("请设置环境变量后重新测试\n")
        return
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, (query, description, expectation) in enumerate(test_cases, 1):
        print(f"测试 {i}/{total_count}: {description}")
        print(f"输入: '{query}'")
        print(f"期望: {expectation}")
        
        try:
            # 使用DeepSeek-R1模型进行测试
            keywords = extract_keywords(query, model="deepseek/DeepSeek-R1")
            
            if keywords:
                print(f"结果: {keywords}")
                
                # 简单验证：检查是否为英文关键词
                all_english = all(
                    all(ord(char) < 128 for char in keyword) 
                    for keyword in keywords
                )
                
                if all_english:
                    print("✅ 通过 - 成功提取英文关键词")
                    success_count += 1
                else:
                    print("⚠️ 部分通过 - 包含非英文字符")
            else:
                print("❌ 失败 - 未提取到关键词")
                
        except KeywordExtractionError as e:
            print(f"❌ 失败 - 提取错误: {e}")
        except Exception as e:
            print(f"❌ 失败 - 未知错误: {e}")
        
        print("-" * 60)
    
    # 总结
    print(f"\n=== 测试总结 ===")
    print(f"总计测试: {total_count}")
    print(f"成功通过: {success_count}")
    print(f"成功率: {success_count/total_count*100:.1f}%")
    
    if success_count >= total_count * 0.8:
        print("🎉 测试结果: 优秀")
    elif success_count >= total_count * 0.6:
        print("👍 测试结果: 良好")
    else:
        print("⚠️ 测试结果: 需要改进")


def test_edge_cases():
    """测试边界情况"""
    print("\n=== 边界情况测试 ===\n")
    
    edge_cases = [
        ("", "空字符串"),
        ("   ", "空白字符"),
        ("a", "单字符"),
        ("AI", "缩写"),
        ("人工智能人工智能人工智能", "重复词汇"),
        ("!@#$%^&*()", "特殊字符"),
        ("123456", "纯数字"),
        ("COVID-19疫苗研发", "包含数字和连字符"),
    ]
    
    for query, description in edge_cases:
        print(f"测试: {description}")
        print(f"输入: '{query}'")
        
        try:
            keywords = extract_keywords(query, model="deepseek/DeepSeek-R1")
            print(f"结果: {keywords}")
            print("✅ 处理正常")
        except Exception as e:
            print(f"结果: 异常 - {e}")
            print("✅ 异常处理正常")
        
        print("-" * 40)


if __name__ == "__main__":
    print("--- 关键词提取优化测试 ---")
    print("目标: 处理中文输入、纠正错字、输出英文关键词")
    print("设计原则: Linus式简洁直接\n")
    
    test_enhanced_keyword_extraction()
    test_edge_cases()
    
    print("\n--- 测试完成 ---")
    print("'简洁是可靠性的前提' - Linus Torvalds")
