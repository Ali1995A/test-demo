#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek AI诗歌标签分析器演示脚本
展示如何使用AI为诗歌生成智能标签，并演示标签检索功能
"""

import os
import json
import sys
from deepseek_poem_analyzer import AIPoemAnalyzer
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def setup_environment():
    """设置环境变量"""
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        print("请先设置环境变量 DEEPSEEK_API_KEY")
        print("方法1: 在.env文件中设置 DEEPSEEK_API_KEY=your_api_key_here")
        print("方法2: 设置系统环境变量: set DEEPSEEK_API_KEY=your_api_key_here")
        return None
    return api_key

def demo_single_poem_analysis(analyzer):
    """演示单首诗歌分析"""
    print("\n" + "="*60)
    print("单首诗歌AI分析演示")
    print("="*60)
    
    # 示例诗歌
    sample_poems = [
        {
            "title": "静夜思",
            "author": "李白",
            "paragraphs": [
                "床前明月光，",
                "疑是地上霜。",
                "举头望明月，",
                "低头思故乡。"
            ]
        },
        {
            "title": "登鹳雀楼",
            "author": "王之涣", 
            "paragraphs": [
                "白日依山尽，",
                "黄河入海流。",
                "欲穷千里目，",
                "更上一层楼。"
            ]
        },
        {
            "title": "春晓",
            "author": "孟浩然",
            "paragraphs": [
                "春眠不觉晓，",
                "处处闻啼鸟。",
                "夜来风雨声，",
                "花落知多少。"
            ]
        }
    ]
    
    for i, poem in enumerate(sample_poems, 1):
        print(f"\n示例 {i}: {poem['title']} - {poem['author']}")
        print(f"内容: {' '.join(poem['paragraphs'])}")
        
        # AI分析
        print("\nAI分析中...")
        analysis = analyzer.analyze_poem(poem)
        
        if analysis:
            print("\nAI分析结果:")
            print(f"  风格标签: {', '.join(analysis.get('styles', []))}")
            print(f"  场景标签: {', '.join(analysis.get('scenes', []))}")
            print(f"  情感标签: {', '.join(analysis.get('emotions', []))}")
            print(f"  主题标签: {', '.join(analysis.get('themes', []))}")
            print(f"  修辞手法: {', '.join(analysis.get('rhetoric', []))}")
            print(f"  关键词: {', '.join(analysis.get('keywords', []))}")
            print(f"  意境描述: {analysis.get('artistic_description', '')}")
        else:
            print("分析失败")

def demo_batch_analysis(analyzer):
    """演示批量分析"""
    print("\n" + "="*60)
    print("批量诗歌AI分析演示")
    print("="*60)
    
    # 加载少量测试数据
    try:
        with open('website_data/poems_data.json', 'r', encoding='utf-8') as f:
            poems_data = json.load(f)
        
        # 取前5首进行演示
        sample_poems = poems_data[:5]
        print(f"将分析 {len(sample_poems)} 首诗歌...")
        
        # 批量分析
        analyzed_poems = analyzer.batch_analyze(sample_poems, batch_size=2, delay=0.5)
        
        # 显示结果
        print("\n批量分析结果:")
        for i, poem in enumerate(analyzed_poems, 1):
            if 'ai_tags' in poem:
                tags = poem['ai_tags']
                print(f"\n{i}. {poem['title']} - {poem['author']}")
                print(f"   风格: {', '.join(tags.get('styles', []))}")
                print(f"   场景: {', '.join(tags.get('scenes', []))}")
                print(f"   情感: {', '.join(tags.get('emotions', []))}")
                print(f"   主题: {', '.join(tags.get('themes', []))}")
        
        # 生成统计
        stats = analyzer.generate_analysis_statistics(analyzed_poems)
        print(f"\n分析统计:")
        print(f"  分析总数: {stats['total_analyzed']}")
        print(f"  成功分析: {stats['successful_analysis']}")
        
    except FileNotFoundError:
        print("未找到 poems_data.json 文件")
    except Exception as e:
        print(f"批量分析失败: {e}")

def demo_tag_retrieval(analyzer):
    """演示标签检索功能"""
    print("\n" + "="*60)
    print("AI标签检索演示")
    print("="*60)
    
    print("通过AI生成的智能标签，您可以实现以下检索:")
    print("\n检索维度:")
    print("  1. 按风格检索: 豪放、婉约、田园、边塞等")
    print("  2. 按场景检索: 春天、夜晚、山水、城市等")
    print("  3. 按情感检索: 喜悦、忧愁、思念、孤独等")
    print("  4. 按主题检索: 爱情、友情、家国、人生等")
    print("  5. 按关键词检索: 明月、故乡、春风、秋雨等")
    
    print("\n检索示例:")
    print("  - 查找所有'豪放'风格的诗歌")
    print("  - 查找'春天'场景的'婉约'风格诗歌")
    print("  - 查找包含'明月'关键词的诗歌")
    print("  - 查找'忧愁'情感的'夜晚'场景诗歌")
    
    # 模拟检索示例
    print("\n模拟检索结果:")
    sample_results = [
        {"title": "将进酒", "author": "李白", "tags": ["豪放", "饮酒", "人生哲理"]},
        {"title": "春夜喜雨", "author": "杜甫", "tags": ["春天", "夜晚", "喜悦", "自然"]},
        {"title": "相思", "author": "王维", "tags": ["思念", "爱情", "婉约", "红豆"]}
    ]
    
    for poem in sample_results:
        print(f"  {poem['title']} - {poem['author']}")
        print(f"    标签: {', '.join(poem['tags'])}")

def demo_integration_with_existing_data():
    """演示与现有数据的集成"""
    print("\n" + "="*60)
    print("与现有数据集成演示")
    print("="*60)
    
    print("AI标签可以与现有诗歌数据完美集成:")
    print("\n数据增强:")
    print("  - 在原有数据基础上添加AI分析结果")
    print("  - 保留原有的关键词、朝代等信息")
    print("  - 新增ai_analysis和ai_tags字段")
    
    print("\n集成示例数据结构:")
    enhanced_poem_example = {
        "id": "001",
        "title": "静夜思", 
        "author": "李白",
        "volume": "卷165",
        "number": "1",
        "paragraphs": ["床前明月光，", "疑是地上霜。", "举头望明月，", "低头思故乡。"],
        "biography": "李白（701年－762年），字太白，号青莲居士...",
        "keywords": ["明月", "故乡", "思念"],
        "dynasty": "盛唐",
        # AI增强字段
        "ai_analysis": {
            "styles": ["抒情", "婉约"],
            "scenes": ["夜晚", "室内"],
            "emotions": ["思念", "忧愁"], 
            "themes": ["思乡", "人生"],
            "rhetoric": ["比喻", "对仗"],
            "keywords": ["明月", "故乡", "思念", "夜晚", "孤独"],
            "artistic_description": "这首诗通过明月意象，表达了游子思乡的深切情感..."
        },
        "ai_tags": {
            "styles": ["抒情", "婉约"],
            "scenes": ["夜晚", "室内"],
            "emotions": ["思念", "忧愁"],
            "themes": ["思乡", "人生"],
            "rhetoric": ["比喻", "对仗"],
            "keywords": ["明月", "故乡", "思念", "夜晚", "孤独"]
        }
    }
    
    print("数据结构完整，便于检索和展示")

def show_usage_instructions():
    """显示使用说明"""
    print("\n" + "="*60)
    print("使用说明")
    print("="*60)
    
    print("1. 环境设置:")
    print("   export DEEPSEEK_API_KEY=your_api_key_here")
    
    print("\n2. 运行分析:")
    print("   # 分析单首诗歌")
    print("   python deepseek_poem_analyzer.py")
    
    print("   # 批量分析诗歌")
    print("   python deepseek_poem_analyzer_demo.py")
    
    print("\n3. 输出文件:")
    print("   - ai_enhanced_poems.json: 包含AI标签的增强数据")
    print("   - 与现有website_data/目录结构兼容")
    
    print("\n4. 检索使用:")
    print("   - 可以直接在代码中通过ai_tags字段进行检索")
    print("   - 支持多维度组合检索")
    print("   - 标签格式标准化，便于前端展示")

def main():
    """主演示函数"""
    print("DeepSeek AI诗歌标签分析器演示")
    print("基于大模型的智能诗歌分析与标签生成")
    
    # 检查环境
    api_key = setup_environment()
    if not api_key:
        return
    
    # 创建分析器
    try:
        analyzer = AIPoemAnalyzer(api_key)
        print("AI分析器初始化成功")
    except Exception as e:
        print(f"分析器初始化失败: {e}")
        return
    
    # 运行演示
    demo_single_poem_analysis(analyzer)
    demo_batch_analysis(analyzer) 
    demo_tag_retrieval(analyzer)
    demo_integration_with_existing_data()
    show_usage_instructions()
    
    print("\n" + "="*60)
    print("🎉 演示完成！")
    print("="*60)
    print("\n💡 下一步:")
    print("1. 运行批量分析处理全部诗歌数据")
    print("2. 将AI标签集成到网站搜索功能中")
    print("3. 享受智能化的诗歌检索体验！")

if __name__ == "__main__":
    main()