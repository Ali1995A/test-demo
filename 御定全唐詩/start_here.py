#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI诗歌标签工具 - 一键启动脚本
最简单的使用方式，适合新手快速上手
Windows兼容版本
"""

import os
import sys
from dotenv import load_dotenv

# Windows终端编码兼容
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    # 加载环境变量
    load_dotenv()
    
    # 检查API密钥
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        print("❌ 未找到DeepSeek API密钥")
        print("\n请按以下方式设置API密钥：")
        print("1. 创建 .env 文件，添加：DEEPSEEK_API_KEY=您的API密钥")
        print("2. 或设置环境变量：set DEEPSEEK_API_KEY=您的API密钥")
        print("3. 或直接在命令行使用参数：--api-key 您的API密钥")
        return False
    
    print("✅ API密钥配置正常")
    return True

def show_menu():
    """显示主菜单"""
    print("\n" + "="*50)
    print("🎯 AI诗歌标签工具 - 主菜单")
    print("="*50)
    print("1. 🚀 快速测试（推荐新手）")
    print("2. 📁 单文件批量处理")
    print("3. 📂 文件夹批量处理") 
    print("4. 🔍 标签检索工具")
    print("5. 📊 查看统计信息")
    print("6. 📖 查看使用指南")
    print("0. ❌ 退出")
    print("="*50)

def quick_test():
    """快速测试功能"""
    print("\n🚀 开始快速测试...")
    print("这将处理前3首诗歌，用于验证系统功能")
    
    try:
        # 导入处理器
        from batch_ai_poem_processor import BatchPoemProcessor
        
        # 获取API密钥
        api_key = os.getenv('DEEPSEEK_API_KEY')
        processor = BatchPoemProcessor(api_key)
        
        # 加载数据
        poems_data = processor.load_poems_data()
        
        # 只处理前3首
        test_poems = poems_data[:3]
        print(f"📖 将处理 {len(test_poems)} 首诗歌进行测试...")
        
        # 处理诗歌
        processed_poems = processor.process_poems(
            test_poems,
            batch_size=3,
            delay=2.0
        )
        
        # 保存结果
        processor.save_results(processed_poems, "website_data/test_results.json")
        
        # 生成统计
        stats = processor.generate_comprehensive_statistics(processed_poems)
        processor.print_statistics_summary(stats)
        
        print("\n✅ 快速测试完成！")
        print("📁 测试结果: website_data/test_results.json")
        
        # 询问是否启动检索工具
        choice = input("\n是否启动标签检索工具查看结果？(y/n): ")
        if choice.lower() == 'y':
            start_retriever()
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def start_single_file_processor():
    """启动单文件处理器"""
    print("\n📁 启动单文件批量处理器...")
    os.system("python batch_ai_poem_processor.py --help")

def start_folder_processor():
    """启动文件夹处理器"""
    print("\n📂 启动文件夹批量处理器...")
    os.system("python folder_batch_poem_processor.py --help")

def start_retriever():
    """启动检索工具"""
    print("\n🔍 启动标签检索工具...")
    try:
        from ai_tag_retriever import AITagRetriever
        
        # 检查数据文件
        data_file = "website_data/ai_enhanced_poems.json"
        if not os.path.exists(data_file):
            print("⚠️ 未找到处理后的数据文件，请先运行批量处理")
            data_file = "website_data/test_results.json"
            if not os.path.exists(data_file):
                print("❌ 未找到任何处理后的数据")
                return
        
        retriever = AITagRetriever(data_file)
        retriever.interactive_search()
        
    except Exception as e:
        print(f"❌ 检索工具启动失败: {e}")

def show_statistics():
    """显示统计信息"""
    print("\n📊 查看统计信息...")
    
    stats_files = [
        "website_data/ai_analysis_statistics.json",
        "website_data/folder_ai_analysis_statistics.json",
        "website_data/test_results.json"
    ]
    
    found = False
    for stats_file in stats_files:
        if os.path.exists(stats_file):
            print(f"\n📈 统计文件: {stats_file}")
            try:
                import json
                with open(stats_file, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
                
                # 显示关键统计
                if 'total_analyzed' in stats:
                    print(f"  分析诗歌总数: {stats['total_analyzed']}")
                    print(f"  成功分析数量: {stats['successful_analysis']}")
                    success_rate = stats['successful_analysis'] / stats['total_analyzed'] * 100
                    print(f"  分析成功率: {success_rate:.1f}%")
                
                found = True
                
            except Exception as e:
                print(f"  读取失败: {e}")
    
    if not found:
        print("❌ 未找到统计信息文件，请先运行批量处理")

def show_guide():
    """显示使用指南"""
    print("\n📖 使用指南")
    print("="*30)
    print("1. 首次使用建议选择 '快速测试'")
    print("2. 测试成功后选择批量处理完整数据")
    print("3. 使用标签检索工具查找诗歌")
    print("\n详细指南请查看:")
    print("  - quick_start_guide.md (快速入门)")
    print("  - processing_guide.md (详细说明)")
    print("  - ai_poem_analyzer_guide.md (技术文档)")

def main():
    """主函数"""
    print("🎯 欢迎使用AI诗歌标签工具！")
    
    # 检查环境
    if not check_environment():
        return
    
    while True:
        show_menu()
        choice = input("\n请选择操作 (0-6): ").strip()
        
        if choice == '1':
            quick_test()
        elif choice == '2':
            start_single_file_processor()
        elif choice == '3':
            start_folder_processor()
        elif choice == '4':
            start_retriever()
        elif choice == '5':
            show_statistics()
        elif choice == '6':
            show_guide()
        elif choice == '0':
            print("👋 感谢使用，再见！")
            break
        else:
            print("❌ 无效选择，请重新输入")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 用户中断，再见！")
    except Exception as e:
        print(f"❌ 程序异常: {e}")