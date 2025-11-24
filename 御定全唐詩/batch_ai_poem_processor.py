#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量AI诗歌标签处理器
使用DeepSeek API批量处理诗歌数据，生成智能标签并保存结果
"""

import os
import json
import time
import argparse
import logging
from typing import List, Dict, Any
from deepseek_poem_analyzer import AIPoemAnalyzer
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_poem_processing.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BatchPoemProcessor:
    """批量诗歌处理器"""
    
    def __init__(self, api_key: str):
        """
        初始化批量处理器
        
        Args:
            api_key: DeepSeek API密钥
        """
        self.analyzer = AIPoemAnalyzer(api_key)
        
    def load_poems_data(self, input_file: str = "website_data/poems_data.json") -> List[Dict]:
        """
        加载诗歌数据
        
        Args:
            input_file: 输入文件路径
            
        Returns:
            诗歌数据列表
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                poems_data = json.load(f)
            logger.info(f"成功加载 {len(poems_data)} 首诗歌数据")
            return poems_data
        except FileNotFoundError:
            logger.error(f"未找到输入文件: {input_file}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"JSON文件解析失败: {e}")
            raise
    
    def process_poems(self, poems_data: List[Dict], 
                     start_index: int = 0,
                     end_index: int = None,
                     batch_size: int = 20,
                     delay: float = 1.0) -> List[Dict]:
        """
        处理诗歌数据
        
        Args:
            poems_data: 诗歌数据列表
            start_index: 开始索引
            end_index: 结束索引
            batch_size: 批次大小
            delay: 请求间隔
            
        Returns:
            处理后的诗歌数据
        """
        if end_index is None:
            end_index = len(poems_data)
        
        poems_to_process = poems_data[start_index:end_index]
        total_to_process = len(poems_to_process)
        
        logger.info(f"开始处理诗歌 {start_index} 到 {end_index}，共 {total_to_process} 首")
        logger.info(f"批次大小: {batch_size}, 请求间隔: {delay}秒")
        
        # 批量分析
        processed_poems = self.analyzer.batch_analyze(
            poems_to_process, 
            batch_size=batch_size, 
            delay=delay
        )
        
        return processed_poems
    
    def save_results(self, processed_poems: List[Dict], 
                    output_file: str = "website_data/ai_enhanced_poems.json"):
        """
        保存处理结果
        
        Args:
            processed_poems: 处理后的诗歌数据
            output_file: 输出文件路径
        """
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_poems, f, ensure_ascii=False, indent=2)
        
        logger.info(f"处理结果已保存到: {output_file}")
    
    def generate_comprehensive_statistics(self, processed_poems: List[Dict]) -> Dict[str, Any]:
        """
        生成综合统计信息
        
        Args:
            processed_poems: 处理后的诗歌数据
            
        Returns:
            统计信息字典
        """
        from collections import Counter
        
        stats = self.analyzer.generate_analysis_statistics(processed_poems)
        
        # 添加更多统计维度
        stats['author_distribution'] = Counter()
        stats['dynasty_distribution'] = Counter()
        stats['tag_coverage'] = {
            'has_styles': 0,
            'has_scenes': 0, 
            'has_emotions': 0,
            'has_themes': 0,
            'has_rhetoric': 0
        }
        
        for poem in processed_poems:
            # 作者分布
            stats['author_distribution'][poem.get('author', '未知')] += 1
            
            # 朝代分布
            stats['dynasty_distribution'][poem.get('dynasty', '未知')] += 1
            
            # 标签覆盖统计
            if 'ai_tags' in poem:
                tags = poem['ai_tags']
                if tags.get('styles'):
                    stats['tag_coverage']['has_styles'] += 1
                if tags.get('scenes'):
                    stats['tag_coverage']['has_scenes'] += 1
                if tags.get('emotions'):
                    stats['tag_coverage']['has_emotions'] += 1
                if tags.get('themes'):
                    stats['tag_coverage']['has_themes'] += 1
                if tags.get('rhetoric'):
                    stats['tag_coverage']['has_rhetoric'] += 1
        
        return stats
    
    def save_statistics(self, stats: Dict[str, Any], 
                       stats_file: str = "website_data/ai_analysis_statistics.json"):
        """
        保存统计信息
        
        Args:
            stats: 统计信息
            stats_file: 统计文件路径
        """
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        logger.info(f"统计信息已保存到: {stats_file}")
    
    def print_statistics_summary(self, stats: Dict[str, Any]):
        """
        打印统计摘要
        
        Args:
            stats: 统计信息
        """
        print("\n" + "="*60)
        print("AI诗歌分析统计摘要")
        print("="*60)
        
        print(f"总体统计:")
        print(f"  分析诗歌总数: {stats['total_analyzed']}")
        print(f"  成功分析数量: {stats['successful_analysis']}")
        print(f"  分析成功率: {stats['successful_analysis']/stats['total_analyzed']*100:.1f}%")
        
        print(f"\n风格分布 (Top 5):")
        for style, count in stats['style_distribution'].most_common(5):
            print(f"  {style}: {count}首")
            
        print(f"\n场景分布 (Top 5):")
        for scene, count in stats['scene_distribution'].most_common(5):
            print(f"  {scene}: {count}首")
            
        print(f"\n情感分布 (Top 5):")
        for emotion, count in stats['emotion_distribution'].most_common(5):
            print(f"  {emotion}: {count}首")
            
        print(f"\n主题分布 (Top 5):")
        for theme, count in stats['theme_distribution'].most_common(5):
            print(f"  {theme}: {count}首")
            
        print(f"\n热门关键词 (Top 10):")
        for keyword, count in stats['top_keywords'].most_common(10):
            print(f"  {keyword}: {count}次")
            
        print(f"\n热门作者 (Top 5):")
        for author, count in stats['author_distribution'].most_common(5):
            print(f"  {author}: {count}首")
            
        print(f"\n朝代分布:")
        for dynasty, count in stats['dynasty_distribution'].most_common():
            print(f"  {dynasty}: {count}首")
            
        print(f"\n标签覆盖情况:")
        coverage = stats['tag_coverage']
        total = stats['total_analyzed']
        print(f"  风格标签: {coverage['has_styles']}/{total} ({coverage['has_styles']/total*100:.1f}%)")
        print(f"  场景标签: {coverage['has_scenes']}/{total} ({coverage['has_scenes']/total*100:.1f}%)")
        print(f"  情感标签: {coverage['has_emotions']}/{total} ({coverage['has_emotions']/total*100:.1f}%)")
        print(f"  主题标签: {coverage['has_themes']}/{total} ({coverage['has_themes']/total*100:.1f}%)")
        print(f"  修辞标签: {coverage['has_rhetoric']}/{total} ({coverage['has_rhetoric']/total*100:.1f}%)")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='批量AI诗歌标签处理器')
    parser.add_argument('--api-key', help='DeepSeek API密钥（可选，优先使用环境变量）')
    parser.add_argument('--input', default='website_data/poems_data.json', help='输入文件路径')
    parser.add_argument('--output', default='website_data/ai_enhanced_poems.json', help='输出文件路径')
    parser.add_argument('--start', type=int, default=0, help='开始索引')
    parser.add_argument('--end', type=int, help='结束索引')
    parser.add_argument('--batch-size', type=int, default=20, help='批次大小')
    parser.add_argument('--delay', type=float, default=1.0, help='请求间隔（秒）')
    parser.add_argument('--sample', type=int, help='样本大小（测试用）')
    
    args = parser.parse_args()
    
    # 获取API密钥
    api_key = args.api_key or os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        print("请提供DeepSeek API密钥")
        print("使用方法:")
        print("  1. 在.env文件中设置 DEEPSEEK_API_KEY=your_key")
        print("  2. 设置系统环境变量: set DEEPSEEK_API_KEY=your_key")
        print("  3. 或使用参数: --api-key your_key")
        return
    
    try:
        # 创建处理器
        processor = BatchPoemProcessor(api_key)
        
        # 加载数据
        poems_data = processor.load_poems_data(args.input)
        
        # 如果指定了样本大小，只处理样本
        if args.sample:
            poems_data = poems_data[:args.sample]
            print(f"测试模式: 只处理前 {args.sample} 首诗歌")
        
        # 处理诗歌
        processed_poems = processor.process_poems(
            poems_data,
            start_index=args.start,
            end_index=args.end,
            batch_size=args.batch_size,
            delay=args.delay
        )
        
        # 保存结果
        processor.save_results(processed_poems, args.output)
        
        # 生成统计
        stats = processor.generate_comprehensive_statistics(processed_poems)
        processor.save_statistics(stats)
        
        # 打印摘要
        processor.print_statistics_summary(stats)
        
        print(f"\n批量处理完成！")
        print(f"增强数据: {args.output}")
        print(f"统计信息: website_data/ai_analysis_statistics.json")
        print(f"处理日志: ai_poem_processing.log")
        
    except Exception as e:
        logger.error(f"处理失败: {e}")
        raise

if __name__ == "__main__":
    main()