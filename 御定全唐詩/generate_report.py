#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
唐诗数据库查询报告生成器
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

class TangPoetryReport:
    def __init__(self, json_dir='json'):
        self.json_dir = Path(json_dir)
        self.data_cache = []
    
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
                    print(f"已加载 {json_file.name}: {len(data)} 首诗歌")
            except Exception as e:
                print(f"错误: 无法加载文件 {json_file}: {e}")
        
        self.data_cache = all_data
        return all_data
    
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
                        for item in field_value:
                            if keyword in str(item):
                                results.append(poem)
                                break
                    else:
                        if keyword in str(field_value):
                            results.append(poem)
                            break
        
        return results
    
    def query_by_field(self, field, value=None, exact_match=True):
        """按字段查询"""
        data = self.load_all_data()
        results = []
        
        for poem in data:
            if field in poem:
                if value is None:
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
    
    def generate_comprehensive_report(self):
        """生成综合报告"""
        data = self.load_all_data()
        
        report = []
        report.append("=" * 80)
        report.append("《御定全唐詩》数据库查询报告")
        report.append("=" * 80)
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # 基本信息
        report.append("一、数据库基本信息")
        report.append("-" * 40)
        report.append(f"总诗歌数量: {len(data)} 首")
        
        # 作者统计
        author_counts = self.count_by_field('author')
        report.append(f"作者总数: {len(author_counts)} 位")
        
        # 卷数统计
        volume_counts = self.count_by_field('volume')
        report.append(f"卷数总数: {len(volume_counts)} 卷")
        report.append("")
        
        # 作者排名
        report.append("二、作者诗歌数量排名（前20名）")
        report.append("-" * 40)
        sorted_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        for i, (author, count) in enumerate(sorted_authors, 1):
            report.append(f"{i:2d}. {author}: {count} 首")
        report.append("")
        
        # 热门主题分析
        report.append("三、热门主题分析")
        report.append("-" * 40)
        
        # 常见关键词统计
        keywords = ['月', '山', '水', '花', '春', '秋', '风', '云', '雨', '雪']
        keyword_counts = {}
        for keyword in keywords:
            results = self.query_by_keyword(keyword)
            keyword_counts[keyword] = len(results)
        
        for keyword, count in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(data)) * 100
            report.append(f"包含 '{keyword}' 的诗歌: {count} 首 ({percentage:.1f}%)")
        report.append("")
        
        # 卷数分布
        report.append("四、卷数分布统计（前10卷）")
        report.append("-" * 40)
        sorted_volumes = sorted(volume_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        for i, (volume, count) in enumerate(sorted_volumes, 1):
            report.append(f"{i:2d}. {volume}: {count} 首")
        report.append("")
        
        # 具体查询示例
        report.append("五、具体查询示例")
        report.append("-" * 40)
        
        # 查询李世民的诗
        li_shimin_poems = self.query_by_field('author', '李世民')
        report.append(f"1. 作者 '李世民' 的诗歌: {len(li_shimin_poems)} 首")
        
        # 查询包含"月"的诗
        moon_poems = self.query_by_keyword('月')
        report.append(f"2. 包含 '月' 的诗歌: {len(moon_poems)} 首")
        
        # 查询包含"山"的诗
        mountain_poems = self.query_by_keyword('山')
        report.append(f"3. 包含 '山' 的诗歌: {len(mountain_poems)} 首")
        
        # 查询包含"水"的诗
        water_poems = self.query_by_keyword('水')
        report.append(f"4. 包含 '水' 的诗歌: {len(water_poems)} 首")
        report.append("")
        
        # 数据质量分析
        report.append("六、数据质量分析")
        report.append("-" * 40)
        
        # 检查缺失字段
        missing_author = sum(1 for poem in data if 'author' not in poem or not poem['author'])
        missing_title = sum(1 for poem in data if 'title' not in poem or not poem['title'])
        missing_paragraphs = sum(1 for poem in data if 'paragraphs' not in poem or not poem['paragraphs'])
        
        report.append(f"缺少作者信息的诗歌: {missing_author} 首 ({missing_author/len(data)*100:.1f}%)")
        report.append(f"缺少标题的诗歌: {missing_title} 首 ({missing_title/len(data)*100:.1f}%)")
        report.append(f"缺少内容的诗歌: {missing_paragraphs} 首 ({missing_paragraphs/len(data)*100:.1f}%)")
        report.append("")
        
        report.append("=" * 80)
        report.append("报告结束")
        report.append("=" * 80)
        
        return "\n".join(report)

def main():
    print("正在生成唐诗数据库查询报告...")
    
    reporter = TangPoetryReport()
    
    try:
        report = reporter.generate_comprehensive_report()
        
        # 保存报告到文件
        report_file = "tang_poetry_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"报告已生成并保存到: {report_file}")
        print("\n报告摘要:")
        print("-" * 40)
        
        # 显示报告摘要
        lines = report.split('\n')
        for line in lines[:50]:  # 显示前50行作为摘要
            print(line)
        
        print("\n... (完整报告请查看文件)")
        
    except Exception as e:
        print(f"生成报告时出错: {e}")

if __name__ == "__main__":
    main()