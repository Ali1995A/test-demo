#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON查询工具 - 类似jq的命令行工具
"""

import json
import os
import sys
import argparse
from pathlib import Path

class JSONQueryTool:
    def __init__(self, json_dir='json'):
        self.json_dir = Path(json_dir)
        self.data_cache = {}
    
    def load_all_data(self):
        """加载所有JSON数据"""
        if self.data_cache:
            return self.data_cache
        
        all_data = []
        json_files = list(self.json_dir.glob('*.json'))
        
        for json_file in sorted(json_files):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_data.extend(data)
                    print(f"已加载 {json_file.name}: {len(data)} 首诗歌", file=sys.stderr)
            except Exception as e:
                print(f"错误: 无法加载文件 {json_file}: {e}", file=sys.stderr)
        
        self.data_cache = all_data
        return all_data
    
    def query_by_field(self, field, value=None, exact_match=True):
        """按字段查询"""
        data = self.load_all_data()
        results = []
        
        for poem in data:
            if field in poem:
                if value is None:
                    # 只检查字段存在
                    results.append(poem)
                else:
                    field_value = poem[field]
                    if exact_match:
                        if field_value == value:
                            results.append(poem)
                    else:
                        if value in str(field_value):
                            results.append(poem)
        
        return results
    
    def query_by_keyword(self, keyword, fields=None):
        """按关键词查询"""
        if fields is None:
            fields = ['title', 'author', 'paragraphs']
        
        data = self.load_all_data()
        results = []
        
        for poem in data:
            for field in fields:
                if field in poem:
                    field_value = poem[field]
                    if isinstance(field_value, list):
                        # 处理列表字段（如paragraphs）
                        for item in field_value:
                            if keyword in str(item):
                                results.append(poem)
                                break
                    else:
                        if keyword in str(field_value):
                            results.append(poem)
                            break
        
        return results
    
    def get_field_values(self, field):
        """获取字段的所有唯一值"""
        data = self.load_all_data()
        values = set()
        
        for poem in data:
            if field in poem:
                values.add(poem[field])
        
        return sorted(list(values))
    
    def count_by_field(self, field):
        """按字段统计"""
        data = self.load_all_data()
        counts = {}
        
        for poem in data:
            if field in poem:
                value = poem[field]
                if value not in counts:
                    counts[value] = 0
                counts[value] += 1
        
        return counts
    
    def format_output(self, results, output_format='simple', fields=None):
        """格式化输出"""
        if fields is None:
            fields = ['title', 'author', 'volume', 'no#']
        
        if output_format == 'json':
            return json.dumps(results, ensure_ascii=False, indent=2)
        
        elif output_format == 'simple':
            output_lines = []
            for i, poem in enumerate(results):
                line_parts = []
                for field in fields:
                    if field in poem:
                        line_parts.append(f"{field}: {poem[field]}")
                output_lines.append(f"{i+1}. " + ", ".join(line_parts))
            return "\n".join(output_lines)
        
        elif output_format == 'detailed':
            output_lines = []
            for i, poem in enumerate(results):
                output_lines.append(f"=== 诗歌 {i+1} ===")
                for field in ['title', 'author', 'volume', 'no#', 'biography']:
                    if field in poem and poem[field]:
                        output_lines.append(f"{field}: {poem[field]}")
                
                if 'paragraphs' in poem and poem['paragraphs']:
                    output_lines.append("内容:")
                    for j, line in enumerate(poem['paragraphs']):
                        output_lines.append(f"  {j+1}. {line}")
                
                output_lines.append("")  # 空行分隔
            
            return "\n".join(output_lines)
        
        return str(results)

def main():
    parser = argparse.ArgumentParser(description='JSON查询工具 - 类似jq的命令行工具')
    parser.add_argument('--field', '-f', help='按字段查询')
    parser.add_argument('--value', '-v', help='字段值')
    parser.add_argument('--keyword', '-k', help='按关键词查询')
    parser.add_argument('--exact', '-e', action='store_true', help='精确匹配')
    parser.add_argument('--fields', help='输出字段（逗号分隔）')
    parser.add_argument('--format', '-F', choices=['simple', 'detailed', 'json'], 
                       default='simple', help='输出格式')
    parser.add_argument('--count', '-c', help='按字段统计')
    parser.add_argument('--list-values', '-l', help='列出字段的所有值')
    parser.add_argument('--json-dir', default='json', help='JSON文件目录')
    
    args = parser.parse_args()
    
    tool = JSONQueryTool(args.json_dir)
    
    try:
        if args.list_values:
            values = tool.get_field_values(args.list_values)
            print(f"字段 '{args.list_values}' 的所有值:")
            for value in values:
                print(f"  {value}")
        
        elif args.count:
            counts = tool.count_by_field(args.count)
            print(f"按字段 '{args.count}' 统计:")
            for value, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  {value}: {count}")
        
        elif args.keyword:
            results = tool.query_by_keyword(args.keyword)
            output_fields = args.fields.split(',') if args.fields else None
            print(tool.format_output(results, args.format, output_fields))
            print(f"\n找到 {len(results)} 个结果", file=sys.stderr)
        
        elif args.field:
            results = tool.query_by_field(args.field, args.value, args.exact)
            output_fields = args.fields.split(',') if args.fields else None
            print(tool.format_output(results, args.format, output_fields))
            print(f"\n找到 {len(results)} 个结果", file=sys.stderr)
        
        else:
            # 显示基本信息
            data = tool.load_all_data()
            print(f"唐诗数据库信息:")
            print(f"  总诗歌数: {len(data)}")
            authors = tool.get_field_values('author')
            print(f"  作者数: {len(authors)}")
            volumes = tool.get_field_values('volume')
            print(f"  卷数: {len(volumes)}")
            print(f"\n使用示例:")
            print("  python json_query_tool.py --keyword 月")
            print("  python json_query_tool.py --field author --value 李世民")
            print("  python json_query_tool.py --count author")
            print("  python json_query_tool.py --list-values volume")
    
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()