#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
唐诗网站数据预处理工具
将原始JSON数据转换为适合网站使用的格式
"""

import json
import os
import re
from pathlib import Path
from collections import defaultdict

class TangPoetryWebsiteData:
    def __init__(self, json_dir='json'):
        self.json_dir = Path(json_dir)
        self.output_dir = Path('website_data')
        self.output_dir.mkdir(exist_ok=True)
    
    def load_all_data(self):
        """加载所有JSON数据"""
        all_data = []
        json_files = list(self.json_dir.glob('*.json'))
        
        for json_file in sorted(json_files):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_data.extend(data)
                    print(f"已加载 {json_file.name}: {len(data)} 首诗歌")
            except Exception as e:
                print(f"错误: 无法加载文件 {json_file}: {e}")
        
        return all_data
    
    def extract_keywords(self, poem):
        """从诗歌内容提取关键词"""
        keywords = set()
        
        # 常见主题关键词
        theme_keywords = ['月', '山', '水', '花', '春', '秋', '风', '云', '雨', '雪',
                         '日', '夜', '江', '河', '海', '湖', '天', '地', '人', '心',
                         '酒', '茶', '琴', '棋', '书', '画', '诗', '歌', '舞', '梦']
        
        # 检查标题和内容
        text = poem.get('title', '') + ' '.join(poem.get('paragraphs', []))
        
        for keyword in theme_keywords:
            if keyword in text:
                keywords.add(keyword)
        
        return list(keywords)
    
    def determine_dynasty(self, author):
        """根据作者确定朝代"""
        # 唐代主要诗人朝代判断
        early_tang = ['李世民', '王勃', '杨炯', '卢照邻', '骆宾王']
        high_tang = ['李白', '杜甫', '王维', '孟浩然', '高适', '岑参']
        mid_tang = ['白居易', '元稹', '韩愈', '柳宗元', '刘禹锡', '李贺']
        late_tang = ['李商隐', '杜牧', '温庭筠', '韦庄']
        
        if author in early_tang:
            return '初唐'
        elif author in high_tang:
            return '盛唐'
        elif author in mid_tang:
            return '中唐'
        elif author in late_tang:
            return '晚唐'
        else:
            return '唐代'
    
    def preprocess_data(self):
        """预处理数据，生成网站所需格式"""
        print("开始预处理数据...")
        raw_data = self.load_all_data()
        
        processed_poems = []
        author_index = defaultdict(list)
        volume_index = defaultdict(list)
        keyword_index = defaultdict(list)
        dynasty_index = defaultdict(list)
        
        for i, poem in enumerate(raw_data):
            # 生成唯一ID
            poem_id = f"{poem.get('volume', '未知')}-{poem.get('no#', i+1)}"
            
            # 提取关键词
            keywords = self.extract_keywords(poem)
            
            # 确定朝代
            author = poem.get('author', '未知')
            dynasty = self.determine_dynasty(author)
            
            # 构建处理后的诗歌数据
            processed_poem = {
                'id': poem_id,
                'title': poem.get('title', '无题'),
                'author': author,
                'volume': poem.get('volume', '未知'),
                'number': poem.get('no#', ''),
                'paragraphs': poem.get('paragraphs', []),
                'biography': poem.get('biography', ''),
                'keywords': keywords,
                'dynasty': dynasty
            }
            
            processed_poems.append(processed_poem)
            
            # 构建索引
            author_index[author].append(poem_id)
            volume_index[poem['volume']].append(poem_id)
            dynasty_index[dynasty].append(poem_id)
            
            for keyword in keywords:
                keyword_index[keyword].append(poem_id)
        
        return {
            'poems': processed_poems,
            'indexes': {
                'authors': dict(author_index),
                'volumes': dict(volume_index),
                'keywords': dict(keyword_index),
                'dynasties': dict(dynasty_index)
            },
            'statistics': {
                'total_poems': len(processed_poems),
                'total_authors': len(author_index),
                'total_volumes': len(volume_index),
                'total_keywords': len(keyword_index)
            }
        }
    
    def generate_search_data(self, processed_data):
        """生成搜索数据"""
        search_data = []
        
        for poem in processed_data['poems']:
            search_item = {
                'id': poem['id'],
                'title': poem['title'],
                'author': poem['author'],
                'content': ' '.join(poem['paragraphs']),
                'keywords': poem['keywords'],
                'dynasty': poem['dynasty']
            }
            search_data.append(search_item)
        
        return search_data
    
    def save_website_data(self):
        """保存网站数据"""
        print("生成网站数据...")
        processed_data = self.preprocess_data()
        
        # 保存主数据文件
        with open(self.output_dir / 'poems_data.json', 'w', encoding='utf-8') as f:
            json.dump(processed_data['poems'], f, ensure_ascii=False, indent=2)
        
        # 保存索引文件
        with open(self.output_dir / 'indexes.json', 'w', encoding='utf-8') as f:
            json.dump(processed_data['indexes'], f, ensure_ascii=False, indent=2)
        
        # 保存统计信息
        with open(self.output_dir / 'statistics.json', 'w', encoding='utf-8') as f:
            json.dump(processed_data['statistics'], f, ensure_ascii=False, indent=2)
        
        # 保存搜索数据
        search_data = self.generate_search_data(processed_data)
        with open(self.output_dir / 'search_data.json', 'w', encoding='utf-8') as f:
            json.dump(search_data, f, ensure_ascii=False, indent=2)
        
        # 生成作者排名
        author_stats = []
        for author, poems in processed_data['indexes']['authors'].items():
            author_stats.append({
                'author': author,
                'count': len(poems),
                'dynasty': self.determine_dynasty(author)
            })
        
        author_stats.sort(key=lambda x: x['count'], reverse=True)
        with open(self.output_dir / 'author_ranking.json', 'w', encoding='utf-8') as f:
            json.dump(author_stats, f, ensure_ascii=False, indent=2)
        
        # 生成热门关键词
        keyword_stats = []
        for keyword, poems in processed_data['indexes']['keywords'].items():
            keyword_stats.append({
                'keyword': keyword,
                'count': len(poems)
            })
        
        keyword_stats.sort(key=lambda x: x['count'], reverse=True)
        with open(self.output_dir / 'keyword_ranking.json', 'w', encoding='utf-8') as f:
            json.dump(keyword_stats, f, ensure_ascii=False, indent=2)
        
        print(f"数据预处理完成！")
        print(f"总诗歌数: {processed_data['statistics']['total_poems']}")
        print(f"作者数: {processed_data['statistics']['total_authors']}")
        print(f"卷数: {processed_data['statistics']['total_volumes']}")
        print(f"关键词数: {processed_data['statistics']['total_keywords']}")
        print(f"数据文件保存在: {self.output_dir}/")

def main():
    print("唐诗网站数据预处理工具")
    print("=" * 50)
    
    processor = TangPoetryWebsiteData()
    processor.save_website_data()

if __name__ == "__main__":
    main()