#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI诗歌标签检索工具
演示如何轻松检索AI生成的诗歌标签，支持多维度组合检索
"""

import json
import argparse
from typing import List, Dict, Any, Set
from collections import defaultdict

class AITagRetriever:
    """AI标签检索器"""
    
    def __init__(self, data_file: str = "website_data/ai_enhanced_poems.json"):
        """
        初始化检索器
        
        Args:
            data_file: 增强诗歌数据文件路径
        """
        self.data_file = data_file
        self.poems_data = self._load_data()
        self.tag_index = self._build_tag_index()
    
    def _load_data(self) -> List[Dict]:
        """加载诗歌数据"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"未找到数据文件: {self.data_file}")
            print("请先运行批量处理生成AI标签数据")
            return []
        except json.JSONDecodeError as e:
            print(f"数据文件解析失败: {e}")
            return []
    
    def _build_tag_index(self) -> Dict[str, Set[int]]:
        """构建标签索引"""
        if not self.poems_data:
            return {}
            
        index = defaultdict(set)
        
        for i, poem in enumerate(self.poems_data):
            if 'ai_tags' not in poem:
                continue
                
            tags = poem['ai_tags']
            
            # 索引各种标签类型
            for style in tags.get('styles', []):
                index[f'style:{style}'].add(i)
            for scene in tags.get('scenes', []):
                index[f'scene:{scene}'].add(i)
            for emotion in tags.get('emotions', []):
                index[f'emotion:{emotion}'].add(i)
            for theme in tags.get('themes', []):
                index[f'theme:{theme}'].add(i)
            for rhetoric in tags.get('rhetoric', []):
                index[f'rhetoric:{rhetoric}'].add(i)
            for keyword in tags.get('keywords', []):
                index[f'keyword:{keyword}'].add(i)
            
            # 索引作者和标题
            index[f'author:{poem.get("author", "")}'].add(i)
            index[f'title:{poem.get("title", "")}'].add(i)
        
        return index
    
    def search_by_tags(self, tags: List[str], operator: str = 'AND') -> List[Dict]:
        """
        根据标签搜索诗歌
        
        Args:
            tags: 标签列表
            operator: 搜索操作符 ('AND' 或 'OR')
            
        Returns:
            匹配的诗歌列表
        """
        if not self.poems_data or not self.tag_index:
            return []
            
        if operator.upper() == 'AND':
            # AND 操作：必须包含所有标签
            result_indices = None
            for tag in tags:
                if tag in self.tag_index:
                    if result_indices is None:
                        result_indices = self.tag_index[tag].copy()
                    else:
                        result_indices &= self.tag_index[tag]
                else:
                    # 如果某个标签不存在，AND 操作返回空结果
                    return []
            
            if result_indices is None:
                return []
                
        else:
            # OR 操作：包含任意标签
            result_indices = set()
            for tag in tags:
                if tag in self.tag_index:
                    result_indices |= self.tag_index[tag]
        
        # 返回匹配的诗歌
        return [self.poems_data[i] for i in result_indices]
    
    def search_by_style(self, styles: List[str]) -> List[Dict]:
        """按风格搜索"""
        style_tags = [f'style:{style}' for style in styles]
        return self.search_by_tags(style_tags, 'OR')
    
    def search_by_scene(self, scenes: List[str]) -> List[Dict]:
        """按场景搜索"""
        scene_tags = [f'scene:{scene}' for scene in scenes]
        return self.search_by_tags(scene_tags, 'OR')
    
    def search_by_emotion(self, emotions: List[str]) -> List[Dict]:
        """按情感搜索"""
        emotion_tags = [f'emotion:{emotion}' for emotion in emotions]
        return self.search_by_tags(emotion_tags, 'OR')
    
    def search_by_theme(self, themes: List[str]) -> List[Dict]:
        """按主题搜索"""
        theme_tags = [f'theme:{theme}' for theme in themes]
        return self.search_by_tags(theme_tags, 'OR')
    
    def search_by_keyword(self, keywords: List[str]) -> List[Dict]:
        """按关键词搜索"""
        keyword_tags = [f'keyword:{keyword}' for keyword in keywords]
        return self.search_by_tags(keyword_tags, 'OR')
    
    def search_combined(self, criteria: Dict[str, List[str]]) -> List[Dict]:
        """
        组合搜索
        
        Args:
            criteria: 搜索条件字典
                {
                    'styles': ['豪放', '婉约'],
                    'scenes': ['春天'],
                    'emotions': ['喜悦'],
                    ...
                }
                
        Returns:
            匹配的诗歌列表
        """
        all_tags = []
        
        for tag_type, values in criteria.items():
            if values:
                if tag_type == 'styles':
                    all_tags.extend([f'style:{v}' for v in values])
                elif tag_type == 'scenes':
                    all_tags.extend([f'scene:{v}' for v in values])
                elif tag_type == 'emotions':
                    all_tags.extend([f'emotion:{v}' for v in values])
                elif tag_type == 'themes':
                    all_tags.extend([f'theme:{v}' for v in values])
                elif tag_type == 'rhetoric':
                    all_tags.extend([f'rhetoric:{v}' for v in values])
                elif tag_type == 'keywords':
                    all_tags.extend([f'keyword:{v}' for v in values])
        
        return self.search_by_tags(all_tags, 'AND')
    
    def get_available_tags(self) -> Dict[str, List[str]]:
        """获取可用的标签列表"""
        tags = {
            'styles': set(),
            'scenes': set(),
            'emotions': set(),
            'themes': set(),
            'rhetoric': set(),
            'keywords': set()
        }
        
        for key in self.tag_index:
            if key.startswith('style:'):
                tags['styles'].add(key[6:])
            elif key.startswith('scene:'):
                tags['scenes'].add(key[6:])
            elif key.startswith('emotion:'):
                tags['emotions'].add(key[8:])
            elif key.startswith('theme:'):
                tags['themes'].add(key[6:])
            elif key.startswith('rhetoric:'):
                tags['rhetoric'].add(key[9:])
            elif key.startswith('keyword:'):
                tags['keywords'].add(key[8:])
        
        # 转换为列表并排序
        return {k: sorted(list(v)) for k, v in tags.items()}
    
    def print_search_results(self, results: List[Dict], limit: int = 10):
        """打印搜索结果"""
        if not results:
            print("未找到匹配的诗歌")
            return
            
        print(f"\n找到 {len(results)} 首匹配的诗歌:")
        
        for i, poem in enumerate(results[:limit]):
            print(f"\n{i+1}. {poem['title']} - {poem['author']}")
            if 'ai_tags' in poem:
                tags = poem['ai_tags']
                print(f"   风格: {', '.join(tags.get('styles', []))}")
                print(f"   场景: {', '.join(tags.get('scenes', []))}")
                print(f"   情感: {', '.join(tags.get('emotions', []))}")
                print(f"   主题: {', '.join(tags.get('themes', []))}")
                print(f"   关键词: {', '.join(tags.get('keywords', []))}")
        
        if len(results) > limit:
            print(f"\n... 还有 {len(results) - limit} 首诗歌未显示")

    def interactive_search(self):
        """交互式搜索界面"""
        print("\n交互式标签检索")
        print("="*40)
        
        if not self.poems_data:
            print("未找到处理后的数据，请先运行批量处理")
            return
        
        # 获取可用标签
        available_tags = self.get_available_tags()
        
        while True:
            print("\n搜索选项:")
            print("1. 按关键词搜索")
            print("2. 按风格搜索")
            print("3. 按场景搜索")
            print("4. 按情感搜索")
            print("5. 按主题搜索")
            print("6. 组合搜索")
            print("7. 查看可用标签")
            print("0. 返回主菜单")
            
            choice = input("\n请选择搜索方式 (0-7): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self._search_by_keyword_interactive()
            elif choice == '2':
                self._search_by_style_interactive(available_tags['styles'])
            elif choice == '3':
                self._search_by_scene_interactive(available_tags['scenes'])
            elif choice == '4':
                self._search_by_emotion_interactive(available_tags['emotions'])
            elif choice == '5':
                self._search_by_theme_interactive(available_tags['themes'])
            elif choice == '6':
                self._search_combined_interactive(available_tags)
            elif choice == '7':
                self._show_available_tags(available_tags)
            else:
                print("无效选择，请重新输入")
    
    def _search_by_keyword_interactive(self):
        """交互式关键词搜索"""
        keyword = input("\n请输入关键词: ").strip()
        if keyword:
            results = self.search_by_keyword([keyword])
            self.print_search_results(results)
        else:
            print("关键词不能为空")
    
    def _search_by_style_interactive(self, available_styles):
        """交互式风格搜索"""
        print(f"\n可用风格: {', '.join(available_styles)}")
        style = input("请输入风格: ").strip()
        if style:
            results = self.search_by_style([style])
            self.print_search_results(results)
        else:
            print("风格不能为空")
    
    def _search_by_scene_interactive(self, available_scenes):
        """交互式场景搜索"""
        print(f"\n可用场景: {', '.join(available_scenes)}")
        scene = input("请输入场景: ").strip()
        if scene:
            results = self.search_by_scene([scene])
            self.print_search_results(results)
        else:
            print("场景不能为空")
    
    def _search_by_emotion_interactive(self, available_emotions):
        """交互式情感搜索"""
        print(f"\n可用情感: {', '.join(available_emotions)}")
        emotion = input("请输入情感: ").strip()
        if emotion:
            results = self.search_by_emotion([emotion])
            self.print_search_results(results)
        else:
            print("情感不能为空")
    
    def _search_by_theme_interactive(self, available_themes):
        """交互式主题搜索"""
        print(f"\n可用主题: {', '.join(available_themes)}")
        theme = input("请输入主题: ").strip()
        if theme:
            results = self.search_by_theme([theme])
            self.print_search_results(results)
        else:
            print("主题不能为空")
    
    def _search_combined_interactive(self, available_tags):
        """交互式组合搜索"""
        criteria = {}
        
        print("\n组合搜索 - 请输入搜索条件（留空跳过）:")
        
        if available_tags['styles']:
            print(f"可用风格: {', '.join(available_tags['styles'])}")
            styles = input("风格 (多个用空格分隔): ").strip()
            if styles:
                criteria['styles'] = styles.split()
        
        if available_tags['scenes']:
            print(f"可用场景: {', '.join(available_tags['scenes'])}")
            scenes = input("场景 (多个用空格分隔): ").strip()
            if scenes:
                criteria['scenes'] = scenes.split()
        
        if available_tags['emotions']:
            print(f"可用情感: {', '.join(available_tags['emotions'])}")
            emotions = input("情感 (多个用空格分隔): ").strip()
            if emotions:
                criteria['emotions'] = emotions.split()
        
        if available_tags['themes']:
            print(f"可用主题: {', '.join(available_tags['themes'])}")
            themes = input("主题 (多个用空格分隔): ").strip()
            if themes:
                criteria['themes'] = themes.split()
        
        keywords = input("关键词 (多个用空格分隔): ").strip()
        if keywords:
            criteria['keywords'] = keywords.split()
        
        if criteria:
            results = self.search_combined(criteria)
            self.print_search_results(results)
        else:
            print("请至少提供一个搜索条件")
    
    def _show_available_tags(self, available_tags):
        """显示可用标签"""
        print("\n可用标签:")
        for tag_type, tags in available_tags.items():
            print(f"\n{tag_type}:")
            if tags:
                print(f"  {', '.join(tags)}")
            else:
                print("  暂无标签")

def demo_retrieval_capabilities():
    """演示检索能力"""
    print("AI标签检索能力演示")
    print("="*50)
    
    retriever = AITagRetriever()
    
    if not retriever.poems_data:
        print("请先运行批量处理生成AI标签数据")
        return
    
    # 获取可用标签
    available_tags = retriever.get_available_tags()
    
    print("\n可用标签维度:")
    for tag_type, tags in available_tags.items():
        print(f"  {tag_type}: {len(tags)} 种")
        if tags:
            print(f"    示例: {', '.join(tags[:5])}")
    
    print("\n检索示例:")
    
    # 示例1: 按风格搜索
    print("\n1. 搜索'豪放'风格的诗歌:")
    results = retriever.search_by_style(['豪放'])
    retriever.print_search_results(results, 3)
    
    # 示例2: 按场景搜索
    print("\n2. 搜索'春天'场景的诗歌:")
    results = retriever.search_by_scene(['春天'])
    retriever.print_search_results(results, 3)
    
    # 示例3: 组合搜索
    print("\n3. 搜索'春天'场景且'喜悦'情感的诗歌:")
    criteria = {
        'scenes': ['春天'],
        'emotions': ['喜悦']
    }
    results = retriever.search_combined(criteria)
    retriever.print_search_results(results, 3)
    
    # 示例4: 按关键词搜索
    print("\n4. 搜索包含'明月'关键词的诗歌:")
    results = retriever.search_by_keyword(['明月'])
    retriever.print_search_results(results, 3)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='AI诗歌标签检索工具')
    parser.add_argument('--data', default='website_data/ai_enhanced_poems.json', help='数据文件路径')
    parser.add_argument('--style', nargs='+', help='按风格搜索')
    parser.add_argument('--scene', nargs='+', help='按场景搜索')
    parser.add_argument('--emotion', nargs='+', help='按情感搜索')
    parser.add_argument('--theme', nargs='+', help='按主题搜索')
    parser.add_argument('--keyword', nargs='+', help='按关键词搜索')
    parser.add_argument('--limit', type=int, default=10, help='显示结果数量限制')
    parser.add_argument('--demo', action='store_true', help='运行演示')
    
    args = parser.parse_args()
    
    if args.demo:
        demo_retrieval_capabilities()
        return
    
    # 创建检索器
    retriever = AITagRetriever(args.data)
    
    if not retriever.poems_data:
        return
    
    # 构建搜索条件
    criteria = {}
    if args.style:
        criteria['styles'] = args.style
    if args.scene:
        criteria['scenes'] = args.scene
    if args.emotion:
        criteria['emotions'] = args.emotion
    if args.theme:
        criteria['themes'] = args.theme
    if args.keyword:
        criteria['keywords'] = args.keyword
    
    # 执行搜索
    if criteria:
        results = retriever.search_combined(criteria)
        retriever.print_search_results(results, args.limit)
    else:
        print("请提供搜索条件，或使用 --demo 查看演示")
        print("\n使用示例:")
        print("  python ai_tag_retriever.py --style 豪放 --scene 山水")
        print("  python ai_tag_retriever.py --emotion 忧愁 --keyword 明月")
        print("  python ai_tag_retriever.py --demo")

if __name__ == "__main__":
    main()