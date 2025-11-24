#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
古诗词智能分析工具
根据诗词内容自动分析风格、场景、类型等，为数据增加更多标签
"""

import json
import re
import os
from collections import Counter
import jieba
import jieba.posseg as pseg

class PoemAnalyzer:
    def __init__(self):
        """初始化分析器"""
        self.setup_jieba()
        self.setup_keywords()
        
    def setup_jieba(self):
        """设置jieba分词"""
        # 添加诗词相关的自定义词典
        jieba.add_word('明月', freq=1000, tag='n')
        jieba.add_word('青山', freq=1000, tag='n')
        jieba.add_word('流水', freq=1000, tag='n')
        jieba.add_word('春风', freq=1000, tag='n')
        jieba.add_word('秋雨', freq=1000, tag='n')
        jieba.add_word('相思', freq=1000, tag='v')
        jieba.add_word('离别', freq=1000, tag='v')
        jieba.add_word('忧愁', freq=1000, tag='a')
        
    def setup_keywords(self):
        """设置分析关键词库"""
        # 诗词风格关键词
        self.style_keywords = {
            '豪放': ['豪情', '壮志', '英雄', '战场', '边塞', '大漠', '长河', '风云', '雷霆', '雄浑'],
            '婉约': ['柔情', '相思', '离别', '愁绪', '闺怨', '春愁', '秋思', '缠绵', '细腻', '含蓄'],
            '田园': ['田园', '农家', '山水', '自然', '闲适', '隐逸', '渔樵', '耕读', '林泉', '幽居'],
            '边塞': ['边塞', '戍边', '征战', '沙场', '胡马', '烽火', '关山', '大漠', '长城', '戍楼'],
            '咏史': ['历史', '古人', '兴亡', '朝代', '帝王', '英雄', '古迹', '怀古', '沧桑', '兴衰'],
            '抒情': ['抒情', '感慨', '情怀', '心境', '思绪', '情感', '感怀', '咏怀', '抒怀', '情怀'],
            '写景': ['写景', '风景', '山水', '自然', '景物', '景色', '风光', '景象', '景致', '景观']
        }
        
        # 场景关键词
        self.scene_keywords = {
            '春天': ['春', '春风', '春雨', '春花', '春色', '春日', '春意', '春愁', '春思'],
            '夏天': ['夏', '夏日', '夏雨', '荷花', '莲叶', '蝉鸣', '炎热', '盛夏'],
            '秋天': ['秋', '秋风', '秋雨', '秋叶', '秋色', '秋思', '秋愁', '秋月', '秋霜'],
            '冬天': ['冬', '冬日', '冬雪', '寒风', '冰雪', '梅花', '严寒', '腊月'],
            '夜晚': ['夜', '月', '星', '灯', '烛', '梦', '眠', '宿', '宵', '更'],
            '早晨': ['晨', '朝', '早', '晓', '旦', '黎明', '曙光', '晨光'],
            '山水': ['山', '水', '江', '河', '湖', '海', '峰', '岭', '溪', '泉'],
            '城市': ['城', '市', '街', '巷', '楼', '台', '阁', '亭', '桥', '路'],
            '乡村': ['村', '乡', '田', '园', '农', '耕', '牧', '渔', '樵', '野']
        }
        
        # 情感关键词
        self.emotion_keywords = {
            '喜悦': ['喜', '乐', '欢', '笑', '欣', '愉', '畅', '快', '怡', '悦'],
            '忧愁': ['愁', '忧', '悲', '哀', '伤', '苦', '痛', '凄', '惨', '戚'],
            '思念': ['思', '念', '想', '忆', '怀', '恋', '慕', '盼', '望', '期'],
            '孤独': ['孤', '独', '寂', '寞', '单', '独', '伶仃', '寂寞', '孤独'],
            '豪迈': ['豪', '壮', '雄', '伟', '宏', '阔', '大', '远', '高', '深'],
            '闲适': ['闲', '适', '静', '安', '宁', '恬', '淡', '悠', '逸', '舒']
        }
        
        # 主题类型关键词
        self.theme_keywords = {
            '爱情': ['爱', '情', '恋', '思', '念', '相思', '恩爱', '情意', '缠绵'],
            '友情': ['友', '朋', '交', '谊', '知己', '故人', '旧友', '同窗'],
            '家国': ['国', '家', '民', '族', '社稷', '江山', '天下', '苍生', '黎民'],
            '人生': ['生', '死', '命', '运', '时', '光', '岁', '年', '老', '少'],
            '自然': ['天', '地', '日', '月', '星', '风', '云', '雨', '雪', '雷'],
            '哲理': ['道', '理', '智', '慧', '悟', '觉', '明', '通', '达', '彻']
        }
        
        # 修辞手法关键词
        self.rhetoric_keywords = {
            '比喻': ['如', '似', '若', '犹', '像', '仿佛', '宛如', '好比'],
            '对仗': ['对', '偶', '仗', '联', '句', '平', '仄', '韵'],
            '夸张': ['千', '万', '百', '九', '极', '绝', '顶', '至', '超'],
            '拟人': ['笑', '哭', '语', '言', '愁', '喜', '悲', '怒', '怨'],
            '借代': ['代', '替', '换', '称', '谓', '名', '号', '字']
        }
        
    def analyze_poem(self, poem_data):
        """分析单首诗词"""
        title = poem_data.get('title', '')
        author = poem_data.get('author', '')
        paragraphs = poem_data.get('paragraphs', [])
        content = ' '.join(paragraphs)
        
        # 分词和词性标注
        words = list(pseg.cut(content))
        
        # 分析结果
        analysis = {
            'title': title,
            'author': author,
            'styles': self.analyze_style(content, words),
            'scenes': self.analyze_scene(content, words),
            'emotions': self.analyze_emotion(content, words),
            'themes': self.analyze_theme(content, words),
            'rhetoric': self.analyze_rhetoric(content, words),
            'keywords': self.extract_keywords(words),
            'length_analysis': self.analyze_length(paragraphs),
            'complexity_score': self.calculate_complexity(content, words)
        }
        
        return analysis
    
    def analyze_style(self, content, words):
        """分析诗词风格"""
        styles = []
        for style, keywords in self.style_keywords.items():
            score = sum(content.count(keyword) for keyword in keywords)
            if score > 0:
                styles.append({
                    'style': style,
                    'score': score,
                    'keywords_found': [kw for kw in keywords if kw in content]
                })
        
        # 按分数排序
        styles.sort(key=lambda x: x['score'], reverse=True)
        return [s['style'] for s in styles[:3]]  # 返回前3个风格
    
    def analyze_scene(self, content, words):
        """分析诗词场景"""
        scenes = []
        for scene, keywords in self.scene_keywords.items():
            score = sum(content.count(keyword) for keyword in keywords)
            if score > 0:
                scenes.append({
                    'scene': scene,
                    'score': score,
                    'keywords_found': [kw for kw in keywords if kw in content]
                })
        
        scenes.sort(key=lambda x: x['score'], reverse=True)
        return [s['scene'] for s in scenes[:3]]
    
    def analyze_emotion(self, content, words):
        """分析诗词情感"""
        emotions = []
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(content.count(keyword) for keyword in keywords)
            if score > 0:
                emotions.append({
                    'emotion': emotion,
                    'score': score,
                    'keywords_found': [kw for kw in keywords if kw in content]
                })
        
        emotions.sort(key=lambda x: x['score'], reverse=True)
        return [e['emotion'] for e in emotions[:3]]
    
    def analyze_theme(self, content, words):
        """分析诗词主题"""
        themes = []
        for theme, keywords in self.theme_keywords.items():
            score = sum(content.count(keyword) for keyword in keywords)
            if score > 0:
                themes.append({
                    'theme': theme,
                    'score': score,
                    'keywords_found': [kw for kw in keywords if kw in content]
                })
        
        themes.sort(key=lambda x: x['score'], reverse=True)
        return [t['theme'] for t in themes[:3]]
    
    def analyze_rhetoric(self, content, words):
        """分析修辞手法"""
        rhetoric = []
        for technique, keywords in self.rhetoric_keywords.items():
            score = sum(content.count(keyword) for keyword in keywords)
            if score > 0:
                rhetoric.append({
                    'technique': technique,
                    'score': score,
                    'keywords_found': [kw for kw in keywords if kw in content]
                })
        
        rhetoric.sort(key=lambda x: x['score'], reverse=True)
        return [r['technique'] for r in rhetoric[:2]]
    
    def extract_keywords(self, words):
        """提取关键词"""
        # 过滤停用词和标点
        stop_words = {'，', '。', '！', '？', '；', '：', '「', '」', '『', '』', '《', '》'}
        filtered_words = [word for word, flag in words 
                         if word not in stop_words and len(word) > 1]
        
        # 统计词频
        word_freq = Counter(filtered_words)
        return [word for word, count in word_freq.most_common(10)]
    
    def analyze_length(self, paragraphs):
        """分析诗词长度"""
        total_chars = sum(len(p) for p in paragraphs)
        total_lines = len(paragraphs)
        avg_line_length = total_chars / total_lines if total_lines > 0 else 0
        
        return {
            'total_chars': total_chars,
            'total_lines': total_lines,
            'avg_line_length': round(avg_line_length, 2),
            'length_category': self.categorize_length(total_chars)
        }
    
    def categorize_length(self, total_chars):
        """分类诗词长度"""
        if total_chars <= 20:
            return '短诗'
        elif total_chars <= 40:
            return '中诗'
        elif total_chars <= 80:
            return '长诗'
        else:
            return '超长诗'
    
    def calculate_complexity(self, content, words):
        """计算诗词复杂度"""
        # 基于词汇多样性、句子长度等计算复杂度
        unique_words = len(set(word for word, flag in words))
        total_words = len(words)
        lexical_diversity = unique_words / total_words if total_words > 0 else 0
        
        # 简单复杂度评分
        complexity = lexical_diversity * 10
        return min(round(complexity, 2), 10)  # 限制在0-10分
    
    def batch_analyze(self, poems_data, sample_size=None):
        """批量分析诗词"""
        if sample_size:
            poems_data = poems_data[:sample_size]
        
        results = []
        print(f"开始分析 {len(poems_data)} 首诗词...")
        
        for i, poem in enumerate(poems_data):
            if i % 100 == 0:
                print(f"已分析 {i} 首诗词...")
            
            try:
                analysis = self.analyze_poem(poem)
                # 将分析结果添加到原数据中
                enriched_poem = poem.copy()
                enriched_poem.update({
                    'analysis': analysis,
                    'enhanced_tags': {
                        'styles': analysis['styles'],
                        'scenes': analysis['scenes'],
                        'emotions': analysis['emotions'],
                        'themes': analysis['themes'],
                        'rhetoric': analysis['rhetoric'],
                        'complexity': analysis['complexity_score'],
                        'length_category': analysis['length_analysis']['length_category']
                    }
                })
                results.append(enriched_poem)
            except Exception as e:
                print(f"分析第 {i} 首诗词时出错: {e}")
                results.append(poem)  # 保留原始数据
        
        print("分析完成！")
        return results
    
    def generate_statistics(self, analyzed_poems):
        """生成统计分析"""
        stats = {
            'total_analyzed': len(analyzed_poems),
            'style_distribution': Counter(),
            'scene_distribution': Counter(),
            'emotion_distribution': Counter(),
            'theme_distribution': Counter(),
            'complexity_stats': {
                'min': 10,
                'max': 0,
                'avg': 0
            }
        }
        
        complexities = []
        
        for poem in analyzed_poems:
            if 'enhanced_tags' in poem:
                tags = poem['enhanced_tags']
                
                # 统计各种标签
                for style in tags.get('styles', []):
                    stats['style_distribution'][style] += 1
                for scene in tags.get('scenes', []):
                    stats['scene_distribution'][scene] += 1
                for emotion in tags.get('emotions', []):
                    stats['emotion_distribution'][emotion] += 1
                for theme in tags.get('themes', []):
                    stats['theme_distribution'][theme] += 1
                
                # 复杂度统计
                complexity = tags.get('complexity', 0)
                complexities.append(complexity)
                stats['complexity_stats']['min'] = min(stats['complexity_stats']['min'], complexity)
                stats['complexity_stats']['max'] = max(stats['complexity_stats']['max'], complexity)
        
        if complexities:
            stats['complexity_stats']['avg'] = round(sum(complexities) / len(complexities), 2)
        
        return stats


def main():
    """主函数"""
    analyzer = PoemAnalyzer()
    
    # 加载数据
    try:
        with open('website_data/poems_data.json', 'r', encoding='utf-8') as f:
            poems_data = json.load(f)
        print(f"成功加载 {len(poems_data)} 首诗词数据")
    except FileNotFoundError:
        print("未找到 poems_data.json 文件，请先运行数据预处理脚本")
        return
    
    # 分析诗词（可以设置样本大小进行测试）
    sample_size = 1000  # 测试用，可以设置为None分析全部数据
    analyzed_poems = analyzer.batch_analyze(poems_data, sample_size)
    
    # 生成统计信息
    stats = analyzer.generate_statistics(analyzed_poems)
    
    # 保存分析结果
    output_file = 'website_data/enhanced_poems_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analyzed_poems, f, ensure_ascii=False, indent=2)
    
    # 保存统计信息
    stats_file = 'website_data/analysis_statistics.json'
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n分析完成！")
    print(f"增强数据已保存到: {output_file}")
    print(f"统计信息已保存到: {stats_file}")
    
    # 打印统计摘要
    print(f"\n=== 分析统计摘要 ===")
    print(f"分析诗词总数: {stats['total_analyzed']}")
    print(f"\n风格分布:")
    for style, count in stats['style_distribution'].most_common(5):
        print(f"  {style}: {count}")
    
    print(f"\n场景分布:")
    for scene, count in stats['scene_distribution'].most_common(5):
        print(f"  {scene}: {count}")
    
    print(f"\n情感分布:")
    for emotion, count in stats['emotion_distribution'].most_common(5):
        print(f"  {emotion}: {count}")
    
    print(f"\n复杂度统计:")
    print(f"  平均: {stats['complexity_stats']['avg']}")
    print(f"  最小: {stats['complexity_stats']['min']}")
    print(f"  最大: {stats['complexity_stats']['max']}")


if __name__ == "__main__":
    main()