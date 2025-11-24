#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Python实现jq风格的JSON标签检索
"""

import json
import os
import sys

def query_json_files():
    """查询JSON文件中的标签"""
    
    # 获取所有JSON文件
    json_files = [f for f in os.listdir('json') if f.endswith('.json')]
    print(f"找到 {len(json_files)} 个JSON文件")
    
    # 演示不同的查询方式
    print("\n=== 基本查询示例 ===")
    
    # 1. 查询所有诗歌的标题和作者
    print("\n1. 查询所有诗歌的标题和作者:")
    for json_file in json_files[:3]:  # 只处理前3个文件作为示例
        with open(f'json/{json_file}', 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"\n文件 {json_file}:")
            for i, poem in enumerate(data[:5]):  # 每个文件只显示前5首
                print(f"  {i+1}. 标题: {poem['title']}, 作者: {poem['author']}")
    
    # 2. 查询特定作者的诗歌
    print("\n2. 查询作者为'李世民'的诗歌:")
    li_shimin_poems = []
    for json_file in json_files[:2]:
        with open(f'json/{json_file}', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for poem in data:
                if poem['author'] == '李世民':
                    li_shimin_poems.append({
                        'title': poem['title'],
                        'volume': poem['volume'],
                        'no#': poem['no#']
                    })
    
    for poem in li_shimin_poems[:10]:  # 只显示前10首
        print(f"  标题: {poem['title']}, 卷: {poem['volume']}, 编号: {poem['no#']}")
    
    # 3. 查询包含特定关键词的诗歌
    print("\n3. 查询标题包含'春'字的诗歌:")
    spring_poems = []
    for json_file in json_files[:3]:
        with open(f'json/{json_file}', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for poem in data:
                if '春' in poem['title']:
                    spring_poems.append({
                        'title': poem['title'],
                        'author': poem['author'],
                        'volume': poem['volume']
                    })
    
    for poem in spring_poems[:10]:
        print(f"  标题: {poem['title']}, 作者: {poem['author']}, 卷: {poem['volume']}")
    
    # 4. 统计信息
    print("\n4. 统计信息:")
    total_poems = 0
    authors = set()
    volumes = set()
    
    for json_file in json_files[:3]:
        with open(f'json/{json_file}', 'r', encoding='utf-8') as f:
            data = json.load(f)
            total_poems += len(data)
            for poem in data:
                authors.add(poem['author'])
                volumes.add(poem['volume'])
    
    print(f"  总诗歌数: {total_poems}")
    print(f"  作者数: {len(authors)}")
    print(f"  卷数: {len(volumes)}")
    print(f"  作者列表: {', '.join(sorted(list(authors))[:10])}...")

def advanced_queries():
    """高级查询示例"""
    print("\n=== 高级查询示例 ===")
    
    # 5. 查询诗歌内容
    print("\n5. 查询诗歌内容 (显示前3行):")
    with open('json/001.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for i, poem in enumerate(data[:3]):
            print(f"\n诗歌 {i+1}: {poem['title']} - {poem['author']}")
            for j, line in enumerate(poem['paragraphs'][:3]):
                print(f"  第{j+1}行: {line}")
    
    # 6. 按卷分组统计
    print("\n6. 按卷分组统计诗歌数量:")
    volume_stats = {}
    for json_file in ['json/001.json', 'json/002.json', 'json/003.json']:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for poem in data:
                volume = poem['volume']
                if volume not in volume_stats:
                    volume_stats[volume] = 0
                volume_stats[volume] += 1
    
    for volume, count in sorted(volume_stats.items()):
        print(f"  {volume}: {count} 首诗歌")

def custom_query():
    """自定义查询函数"""
    print("\n=== 自定义查询 ===")
    
    def query_by_author(author_name):
        """按作者查询"""
        print(f"\n查询作者 '{author_name}' 的诗歌:")
        poems_found = []
        for json_file in ['json/001.json', 'json/002.json', 'json/003.json']:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for poem in data:
                    if poem['author'] == author_name:
                        poems_found.append({
                            'title': poem['title'],
                            'volume': poem['volume'],
                            'no#': poem['no#']
                        })
        
        for poem in poems_found[:5]:
            print(f"  标题: {poem['title']}, 卷: {poem['volume']}, 编号: {poem['no#']}")
        print(f"  共找到 {len(poems_found)} 首诗歌")
    
    def query_by_keyword(keyword):
        """按关键词查询"""
        print(f"\n查询包含关键词 '{keyword}' 的诗歌:")
        poems_found = []
        for json_file in ['json/001.json', 'json/002.json', 'json/003.json']:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for poem in data:
                    if (keyword in poem['title'] or 
                        any(keyword in line for line in poem['paragraphs'])):
                        poems_found.append({
                            'title': poem['title'],
                            'author': poem['author'],
                            'volume': poem['volume']
                        })
        
        for poem in poems_found[:5]:
            print(f"  标题: {poem['title']}, 作者: {poem['author']}, 卷: {poem['volume']}")
        print(f"  共找到 {len(poems_found)} 首诗歌")
    
    # 执行自定义查询
    query_by_author('李世民')
    query_by_keyword('月')

if __name__ == "__main__":
    print("唐诗JSON数据检索工具")
    print("=" * 50)
    
    query_json_files()
    advanced_queries()
    custom_query()
    
    print("\n=== 使用说明 ===")
    print("""
这个脚本演示了如何使用Python来检索JSON标签，类似于jq命令的功能：

1. 基本查询:
   - 查询所有诗歌的标题和作者
   - 按作者筛选
   - 按关键词搜索

2. 高级查询:
   - 显示诗歌内容
   - 统计信息
   - 分组统计

3. 自定义查询:
   - 可以修改query_by_author和query_by_keyword函数
   - 添加新的查询条件

使用方法:
- 修改脚本中的查询条件
- 运行: python json_query_demo.py
    """)