#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
古诗词分析工具演示
展示如何分析单首诗词并查看分析结果
"""

import json
from poem_analyzer import PoemAnalyzer

def demo_single_poem_analysis():
    """演示单首诗词分析"""
    analyzer = PoemAnalyzer()
    
    # 示例诗词数据
    sample_poem = {
        "title": "静夜思",
        "author": "李白",
        "paragraphs": [
            "床前明月光，",
            "疑是地上霜。",
            "举头望明月，",
            "低头思故乡。"
        ],
        "volume": "卷165",
        "number": "1"
    }
    
    print("=== 单首诗词分析演示 ===")
    print(f"标题: {sample_poem['title']}")
    print(f"作者: {sample_poem['author']}")
    print(f"内容: {' '.join(sample_poem['paragraphs'])}")
    print("\n" + "="*50)
    
    # 分析诗词
    analysis = analyzer.analyze_poem(sample_poem)
    
    # 显示分析结果
    print("\n📊 分析结果:")
    print(f"风格: {', '.join(analysis['styles'])}")
    print(f"场景: {', '.join(analysis['scenes'])}")
    print(f"情感: {', '.join(analysis['emotions'])}")
    print(f"主题: {', '.join(analysis['themes'])}")
    print(f"修辞: {', '.join(analysis['rhetoric'])}")
    print(f"复杂度评分: {analysis['complexity_score']}/10")
    print(f"长度分类: {analysis['length_analysis']['length_category']}")
    print(f"关键词: {', '.join(analysis['keywords'][:5])}")

def demo_batch_analysis():
    """演示批量分析"""
    analyzer = PoemAnalyzer()
    
    # 加载少量数据进行演示
    try:
        with open('website_data/poems_data.json', 'r', encoding='utf-8') as f:
            poems_data = json.load(f)
        
        # 取前10首进行演示
        sample_poems = poems_data[:10]
        print(f"\n=== 批量分析演示 (分析 {len(sample_poems)} 首诗词) ===")
        
        analyzed_poems = analyzer.batch_analyze(sample_poems)
        
        # 显示每首诗词的分析摘要
        for i, poem in enumerate(analyzed_poems):
            if 'enhanced_tags' in poem:
                tags = poem['enhanced_tags']
                print(f"\n{i+1}. {poem['title']} - {poem['author']}")
                print(f"   风格: {', '.join(tags.get('styles', []))}")
                print(f"   场景: {', '.join(tags.get('scenes', []))}")
                print(f"   情感: {', '.join(tags.get('emotions', []))}")
        
        # 生成统计信息
        stats = analyzer.generate_statistics(analyzed_poems)
        print(f"\n📈 批量分析统计:")
        print(f"分析诗词总数: {stats['total_analyzed']}")
        
        print(f"\n热门风格:")
        for style, count in stats['style_distribution'].most_common(3):
            print(f"  {style}: {count}首")
            
        print(f"\n热门场景:")
        for scene, count in stats['scene_distribution'].most_common(3):
            print(f"  {scene}: {count}首")
            
    except FileNotFoundError:
        print("未找到 poems_data.json 文件，请先运行数据预处理")

def demo_enhanced_search_capabilities():
    """演示增强的搜索能力"""
    print("\n=== 增强搜索能力演示 ===")
    print("通过智能分析，您现在可以按以下维度搜索:")
    print("1. 风格搜索: 豪放、婉约、田园、边塞等")
    print("2. 场景搜索: 春天、夜晚、山水、城市等") 
    print("3. 情感搜索: 喜悦、忧愁、思念、孤独等")
    print("4. 主题搜索: 爱情、友情、家国、人生等")
    print("5. 复杂度搜索: 简单、中等、复杂")
    print("6. 长度搜索: 短诗、中诗、长诗")
    print("\n示例搜索:")
    print("  - 查找所有'豪放'风格的诗词")
    print("  - 查找'春天'场景的'婉约'风格诗词")
    print("  - 查找'忧愁'情感的'短诗'")
    print("  - 查找复杂度高的'哲理'主题诗词")

def main():
    """主演示函数"""
    print("古诗词智能分析工具演示")
    print("=" * 60)
    
    # 演示单首诗词分析
    demo_single_poem_analysis()
    
    # 演示批量分析
    demo_batch_analysis()
    
    # 演示增强搜索能力
    demo_enhanced_search_capabilities()
    
    print("\n" + "=" * 60)
    print("使用建议:")
    print("1. 运行 'python poem_analyzer.py' 分析全部诗词数据")
    print("2. 分析结果将保存到 enhanced_poems_data.json")
    print("3. 可以使用新的标签维度进行更精确的搜索和分类")
    print("4. 这些智能标签可以集成到网站搜索功能中")

if __name__ == "__main__":
    main()