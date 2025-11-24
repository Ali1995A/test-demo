#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件夹批量AI诗歌标签处理器
支持按文件夹批量处理多个JSON文件，生成智能标签
支持暂停和续传功能
"""

import os
import json
import time
import argparse
import logging
import signal
import sys
from typing import List, Dict, Any
from deepseek_poem_analyzer import AIPoemAnalyzer
from progress_manager import ProgressManager, check_resume_processing, cleanup_progress_file
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('folder_ai_poem_processing.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FolderBatchPoemProcessor:
    """文件夹批量诗歌处理器"""
    
    def __init__(self, api_key: str):
        """
        初始化文件夹批量处理器
        
        Args:
            api_key: DeepSeek API密钥
        """
        self.analyzer = AIPoemAnalyzer(api_key)
        self.progress_manager = ProgressManager()
        self.should_pause = False
        
        # 设置信号处理器，支持Ctrl+C暂停
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """信号处理器，支持Ctrl+C暂停"""
        print("\n\n⏸️  收到暂停信号，正在保存进度...")
        self.should_pause = True
        
    def scan_json_files(self, folder_path: str = "json") -> List[str]:
        """
        扫描文件夹中的JSON文件
        
        Args:
            folder_path: 文件夹路径
            
        Returns:
            JSON文件路径列表
        """
        if not os.path.exists(folder_path):
            logger.error(f"文件夹不存在: {folder_path}")
            raise FileNotFoundError(f"文件夹不存在: {folder_path}")
            
        json_files = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                json_files.append(os.path.join(folder_path, filename))
        
        json_files.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))
        logger.info(f"扫描到 {len(json_files)} 个JSON文件")
        return json_files
    
    def load_poems_from_file(self, file_path: str) -> List[Dict]:
        """
        从单个JSON文件加载诗歌数据
        
        Args:
            file_path: JSON文件路径
            
        Returns:
            诗歌数据列表
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                poems_data = json.load(f)
            
            # 为每首诗歌添加文件来源信息
            for poem in poems_data:
                poem['source_file'] = os.path.basename(file_path)
                
            logger.info(f"从 {file_path} 加载了 {len(poems_data)} 首诗歌")
            return poems_data
        except FileNotFoundError:
            logger.error(f"未找到文件: {file_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"JSON文件解析失败 {file_path}: {e}")
            raise
    
    def process_folder(self, folder_path: str = "json",
                      start_file: int = 1,
                      end_file: int = None,
                      batch_size: int = 20,
                      delay: float = 1.0,
                      output_folder: str = "website_data",
                      resume: bool = False) -> Dict[str, Any]:
        """
        处理文件夹中的所有JSON文件，支持暂停和续传
        
        Args:
            folder_path: 输入文件夹路径
            start_file: 开始文件编号
            end_file: 结束文件编号
            batch_size: 批次大小
            delay: 请求间隔
            output_folder: 输出文件夹路径
            resume: 是否恢复之前的处理
            
        Returns:
            处理结果统计
        """
        # 扫描JSON文件
        json_files = self.scan_json_files(folder_path)
        
        if end_file is None:
            end_file = len(json_files)
        
        # 筛选文件范围
        files_to_process = json_files[start_file-1:end_file]
        
        # 检查是否需要恢复处理
        if resume and check_resume_processing():
            print("🔄 检测到未完成的处理任务，正在恢复...")
            remaining_files = self.progress_manager.get_remaining_files(files_to_process)
            files_to_process = remaining_files
            self.progress_manager.resume_processing()
        else:
            # 开始新的处理
            self.progress_manager.start_processing(len(files_to_process))
        
        logger.info(f"处理文件范围: {start_file} 到 {end_file}，共 {len(files_to_process)} 个文件")
        
        all_processed_poems = []
        file_stats = {}
        
        for file_path in files_to_process:
            # 检查是否需要暂停
            if self.should_pause:
                print("\n⏸️ 正在暂停处理...")
                self.progress_manager.pause_processing()
                self.progress_manager.print_progress_summary()
                print("💡 提示: 使用 --resume 参数可以恢复处理")
                return {"status": "paused", "processed_files": len(all_processed_poems)}
            
            file_name = os.path.basename(file_path)
            logger.info(f"开始处理文件: {file_name}")
            
            try:
                # 设置当前处理文件
                poems_data = self.load_poems_from_file(file_path)
                self.progress_manager.set_current_file(file_path, len(poems_data))
                
                # 处理诗歌
                processed_poems = self.analyzer.batch_analyze(
                    poems_data,
                    batch_size=batch_size,
                    delay=delay
                )
                
                # 更新进度
                successful_count = len([p for p in processed_poems if 'ai_tags' in p])
                self.progress_manager.update_file_progress(len(processed_poems), successful_count)
                
                # 保存单个文件的结果
                output_file = os.path.join(output_folder, f"ai_enhanced_{file_name}")
                self.save_results(processed_poems, output_file)
                
                # 统计信息
                file_stats[file_name] = {
                    'total_poems': len(poems_data),
                    'successful_analysis': successful_count,
                    'failed_analysis': len([p for p in processed_poems if 'ai_tags' not in p])
                }
                
                # 完成文件处理
                self.progress_manager.complete_file(file_path, successful_count, len(poems_data))
                
                all_processed_poems.extend(processed_poems)
                logger.info(f"文件 {file_name} 处理完成")
                
                # 打印进度
                self.progress_manager.print_progress_summary()
                
            except Exception as e:
                logger.error(f"处理文件 {file_name} 失败: {e}")
                self.progress_manager.mark_file_failed(file_path, str(e))
                file_stats[file_name] = {
                    'total_poems': 0,
                    'successful_analysis': 0,
                    'failed_analysis': 0,
                    'error': str(e)
                }
        
        # 保存合并结果
        if all_processed_poems:
            merged_output = os.path.join(output_folder, "ai_enhanced_poems_merged.json")
            self.save_results(all_processed_poems, merged_output)
        
        # 生成统计信息
        stats = self.generate_comprehensive_statistics(all_processed_poems)
        stats['file_statistics'] = file_stats
        
        # 标记处理完成
        self.progress_manager.complete_processing()
        
        return stats
    
    def save_results(self, processed_poems: List[Dict], output_file: str):
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
        stats['file_distribution'] = Counter()
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
            
            # 文件分布
            stats['file_distribution'][poem.get('source_file', '未知')] += 1
            
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
                       stats_file: str = "website_data/folder_ai_analysis_statistics.json"):
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
        print("📊 文件夹批量AI诗歌分析统计摘要")
        print("="*60)
        
        print(f"📈 总体统计:")
        print(f"  分析诗歌总数: {stats['total_analyzed']}")
        print(f"  成功分析数量: {stats['successful_analysis']}")
        print(f"  分析成功率: {stats['successful_analysis']/stats['total_analyzed']*100:.1f}%")
        
        print(f"\n📁 文件分布 (Top 10):")
        for file_name, count in stats['file_distribution'].most_common(10):
            print(f"  {file_name}: {count}首")
            
        print(f"\n🎭 风格分布 (Top 5):")
        for style, count in stats['style_distribution'].most_common(5):
            print(f"  {style}: {count}首")
            
        print(f"\n🌄 场景分布 (Top 5):")
        for scene, count in stats['scene_distribution'].most_common(5):
            print(f"  {scene}: {count}首")
            
        print(f"\n💖 情感分布 (Top 5):")
        for emotion, count in stats['emotion_distribution'].most_common(5):
            print(f"  {emotion}: {count}首")
            
        print(f"\n📚 主题分布 (Top 5):")
        for theme, count in stats['theme_distribution'].most_common(5):
            print(f"  {theme}: {count}首")
            
        print(f"\n🔑 热门关键词 (Top 10):")
        for keyword, count in stats['top_keywords'].most_common(10):
            print(f"  {keyword}: {count}次")
            
        print(f"\n👤 热门作者 (Top 5):")
        for author, count in stats['author_distribution'].most_common(5):
            print(f"  {author}: {count}首")
            
        print(f"\n🏛️ 朝代分布:")
        for dynasty, count in stats['dynasty_distribution'].most_common():
            print(f"  {dynasty}: {count}首")
            
        print(f"\n🏷️ 标签覆盖情况:")
        coverage = stats['tag_coverage']
        total = stats['total_analyzed']
        print(f"  风格标签: {coverage['has_styles']}/{total} ({coverage['has_styles']/total*100:.1f}%)")
        print(f"  场景标签: {coverage['has_scenes']}/{total} ({coverage['has_scenes']/total*100:.1f}%)")
        print(f"  情感标签: {coverage['has_emotions']}/{total} ({coverage['has_emotions']/total*100:.1f}%)")
        print(f"  主题标签: {coverage['has_themes']}/{total} ({coverage['has_themes']/total*100:.1f}%)")
        print(f"  修辞标签: {coverage['has_rhetoric']}/{total} ({coverage['has_rhetoric']/total*100:.1f}%)")
        
        # 文件统计详情
        if 'file_statistics' in stats:
            print(f"\n📋 文件处理详情:")
            for file_name, file_stat in stats['file_statistics'].items():
                if 'error' in file_stat:
                    print(f"  {file_name}: ❌ 处理失败 - {file_stat['error']}")
                else:
                    success_rate = file_stat['successful_analysis'] / file_stat['total_poems'] * 100 if file_stat['total_poems'] > 0 else 0
                    print(f"  {file_name}: {file_stat['successful_analysis']}/{file_stat['total_poems']} ({success_rate:.1f}%)")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='文件夹批量AI诗歌标签处理器')
    parser.add_argument('--api-key', help='DeepSeek API密钥（可选，优先使用环境变量）')
    parser.add_argument('--folder', default='json', help='输入文件夹路径')
    parser.add_argument('--output-folder', default='website_data', help='输出文件夹路径')
    parser.add_argument('--start-file', type=int, default=1, help='开始文件编号')
    parser.add_argument('--end-file', type=int, help='结束文件编号')
    parser.add_argument('--batch-size', type=int, default=20, help='批次大小')
    parser.add_argument('--delay', type=float, default=1.0, help='请求间隔（秒）')
    parser.add_argument('--sample-files', type=int, help='样本文件数量（测试用）')
    parser.add_argument('--resume', action='store_true', help='恢复之前的处理')
    parser.add_argument('--show-progress', action='store_true', help='显示当前进度')
    parser.add_argument('--cleanup', action='store_true', help='清理进度文件')
    
    args = parser.parse_args()
    
    # 清理进度文件
    if args.cleanup:
        cleanup_progress_file()
        print("✅ 进度文件已清理")
        return
    
    # 显示进度
    if args.show_progress:
        progress_manager = ProgressManager()
        progress_manager.print_progress_summary()
        return
    
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
        processor = FolderBatchPoemProcessor(api_key)
        
        # 处理文件夹
        stats = processor.process_folder(
            folder_path=args.folder,
            start_file=args.start_file,
            end_file=args.end_file,
            batch_size=args.batch_size,
            delay=args.delay,
            output_folder=args.output_folder,
            resume=args.resume
        )
        
        # 检查是否暂停
        if stats.get('status') == 'paused':
            print("\n⏸️ 处理已暂停")
            print("💡 使用以下命令恢复处理:")
            print(f"   python folder_batch_poem_processor.py --resume")
            return
        
        # 保存统计
        processor.save_statistics(stats)
        
        # 打印摘要
        processor.print_statistics_summary(stats)
        
        print(f"\n🎉 文件夹批量处理完成！")
        print(f"📁 增强数据: {args.output_folder}/ai_enhanced_*.json")
        print(f"📁 合并数据: {args.output_folder}/ai_enhanced_poems_merged.json")
        print(f"📊 统计信息: {args.output_folder}/folder_ai_analysis_statistics.json")
        print(f"📝 处理日志: folder_ai_poem_processing.log")
        
    except Exception as e:
        logger.error(f"处理失败: {e}")
        raise

if __name__ == "__main__":
    main()