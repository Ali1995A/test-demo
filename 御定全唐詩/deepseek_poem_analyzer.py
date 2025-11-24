#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于DeepSeek API的AI诗歌标签分析器
使用DeepSeek大模型为诗歌生成智能标签，支持风格、场景、情感、主题等多维度分析
"""

import json
import os
import time
import requests
from typing import List, Dict, Any, Optional
import logging
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DeepSeekAPIClient:
    """DeepSeek API客户端"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com/v1"):
        """
        初始化DeepSeek API客户端
        
        Args:
            api_key: DeepSeek API密钥
            base_url: API基础URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
    def chat_completion(self, messages: List[Dict], model: str = "deepseek-chat", 
                       temperature: float = 0.3, max_tokens: int = 2000) -> Optional[str]:
        """
        调用DeepSeek聊天补全API
        
        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            API响应内容或None
        """
        url = f"{self.base_url}/chat/completions"
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求失败: {e}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"API响应解析失败: {e}")
            return None

class AIPoemAnalyzer:
    """AI诗歌分析器 - 基于DeepSeek API"""
    
    def __init__(self, api_key: str):
        """
        初始化AI诗歌分析器
        
        Args:
            api_key: DeepSeek API密钥
        """
        self.api_client = DeepSeekAPIClient(api_key)
        self.analysis_prompt = self._create_analysis_prompt()
        
    def _create_analysis_prompt(self) -> str:
        """创建诗歌分析提示词模板"""
        return """
你是一个专业的古诗词分析专家。请分析以下唐诗，并按照JSON格式返回分析结果。

分析维度：
1. 风格分析：豪放、婉约、田园、边塞、咏史、抒情、写景等
2. 场景分析：春天、夏天、秋天、冬天、夜晚、早晨、山水、城市、乡村等
3. 情感分析：喜悦、忧愁、思念、孤独、豪迈、闲适等
4. 主题分析：爱情、友情、家国、人生、自然、哲理等
5. 修辞手法：比喻、对仗、夸张、拟人、借代等
6. 关键词提取：提取5-8个最能代表诗歌内容的关键词
7. 意境描述：用一段话描述诗歌的意境和艺术特色

请严格按照以下JSON格式返回结果，不要包含其他内容：

{{
    "styles": ["风格1", "风格2", "风格3"],
    "scenes": ["场景1", "场景2", "场景3"],
    "emotions": ["情感1", "情感2", "情感3"],
    "themes": ["主题1", "主题2", "主题3"],
    "rhetoric": ["修辞1", "修辞2"],
    "keywords": ["关键词1", "关键词2", "关键词3", "关键词4", "关键词5"],
    "artistic_description": "意境描述文字"
}}

诗歌信息：
标题：{title}
作者：{author}
内容：
{content}

请开始分析：
"""
    
    def analyze_poem(self, poem_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        分析单首诗歌
        
        Args:
            poem_data: 诗歌数据字典
            
        Returns:
            分析结果字典或None
        """
        title = poem_data.get('title', '')
        author = poem_data.get('author', '')
        paragraphs = poem_data.get('paragraphs', [])
        content = '\n'.join(paragraphs)
        
        if not content:
            logger.warning(f"诗歌内容为空: {title}")
            return None
            
        # 构建提示词
        prompt = self.analysis_prompt.format(
            title=title,
            author=author,
            content=content
        )
        
        messages = [
            {"role": "system", "content": "你是一个专业的古诗词分析专家。"},
            {"role": "user", "content": prompt}
        ]
        
        logger.info(f"开始分析诗歌: {title} - {author}")
        
        # 调用API
        response = self.api_client.chat_completion(messages)
        
        if not response:
            logger.error(f"API调用失败: {title}")
            return None
            
        try:
            # 解析JSON响应
            analysis_result = json.loads(response.strip())
            
            # 添加基础信息
            analysis_result.update({
                'title': title,
                'author': author,
                'content_preview': content[:100] + '...' if len(content) > 100 else content
            })
            
            logger.info(f"成功分析诗歌: {title}")
            return analysis_result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}\n响应内容: {response}")
            return self._fallback_analysis(title, author, content)
    
    def _fallback_analysis(self, title: str, author: str, content: str) -> Dict[str, Any]:
        """
        备用分析方案（当API调用失败时使用）
        
        Args:
            title: 诗歌标题
            author: 作者
            content: 诗歌内容
            
        Returns:
            基础分析结果
        """
        return {
            "title": title,
            "author": author,
            "styles": ["古典"],
            "scenes": ["传统"],
            "emotions": ["中性"], 
            "themes": ["诗歌"],
            "rhetoric": ["古典修辞"],
            "keywords": ["唐诗", "古典"],
            "artistic_description": "这是一首古典唐诗",
            "content_preview": content[:100] + '...' if len(content) > 100 else content,
            "fallback": True
        }
    
    def batch_analyze(self, poems_data: List[Dict], 
                     batch_size: int = 10, 
                     delay: float = 1.0) -> List[Dict]:
        """
        批量分析诗歌
        
        Args:
            poems_data: 诗歌数据列表
            batch_size: 批次大小
            delay: 请求间隔（秒）
            
        Returns:
            增强后的诗歌数据列表
        """
        results = []
        total = len(poems_data)
        
        logger.info(f"开始批量分析 {total} 首诗歌，批次大小: {batch_size}")
        
        for i, poem in enumerate(poems_data):
            if i % batch_size == 0 and i > 0:
                logger.info(f"已分析 {i}/{total} 首诗歌")
                time.sleep(delay)  # 避免API限制
                
            try:
                analysis = self.analyze_poem(poem)
                
                # 合并分析结果到原数据
                enriched_poem = poem.copy()
                if analysis:
                    enriched_poem['ai_analysis'] = analysis
                    enriched_poem['ai_tags'] = {
                        'styles': analysis.get('styles', []),
                        'scenes': analysis.get('scenes', []),
                        'emotions': analysis.get('emotions', []),
                        'themes': analysis.get('themes', []),
                        'rhetoric': analysis.get('rhetoric', []),
                        'keywords': analysis.get('keywords', []),
                        'artistic_description': analysis.get('artistic_description', '')
                    }
                else:
                    # API调用失败时使用基础标签
                    enriched_poem['ai_tags'] = {
                        'styles': ['古典'],
                        'scenes': ['传统'], 
                        'emotions': ['中性'],
                        'themes': ['诗歌'],
                        'rhetoric': ['古典修辞'],
                        'keywords': ['唐诗'],
                        'artistic_description': '分析失败，使用基础标签'
                    }
                    
                results.append(enriched_poem)
                
            except Exception as e:
                logger.error(f"分析诗歌时出错 {poem.get('title', '未知')}: {e}")
                # 保留原始数据
                results.append(poem)
                
        logger.info(f"批量分析完成，成功分析 {len([p for p in results if 'ai_tags' in p])}/{total} 首诗歌")
        return results
    
    def save_analysis_results(self, analyzed_poems: List[Dict], 
                            output_file: str = "website_data/ai_enhanced_poems.json"):
        """
        保存分析结果
        
        Args:
            analyzed_poems: 分析后的诗歌数据
            output_file: 输出文件路径
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analyzed_poems, f, ensure_ascii=False, indent=2)
            
        logger.info(f"分析结果已保存到: {output_file}")
    
    def generate_analysis_statistics(self, analyzed_poems: List[Dict]) -> Dict[str, Any]:
        """
        生成分析统计信息
        
        Args:
            analyzed_poems: 分析后的诗歌数据
            
        Returns:
            统计信息字典
        """
        from collections import Counter
        
        stats = {
            'total_analyzed': len(analyzed_poems),
            'successful_analysis': 0,
            'style_distribution': Counter(),
            'scene_distribution': Counter(),
            'emotion_distribution': Counter(),
            'theme_distribution': Counter(),
            'top_keywords': Counter()
        }
        
        for poem in analyzed_poems:
            if 'ai_tags' in poem:
                stats['successful_analysis'] += 1
                tags = poem['ai_tags']
                
                # 统计各种标签
                for style in tags.get('styles', []):
                    stats['style_distribution'][style] += 1
                for scene in tags.get('scenes', []):
                    stats['scene_distribution'][scene] += 1
                for emotion in tags.get('emotions', []):
                    stats['emotion_distribution'][emotion] += 1
                for theme in tags.get('themes', []):
                    stats['theme_distribution'][theme] += 1
                for keyword in tags.get('keywords', []):
                    stats['top_keywords'][keyword] += 1
        
        return stats

def main():
    """主函数 - 演示使用"""
    # 从环境变量获取API密钥
    api_key = os.getenv('DEEPSEEK_API_KEY')
    
    if not api_key:
        print("请设置环境变量 DEEPSEEK_API_KEY")
        print("方法1: 在.env文件中设置 DEEPSEEK_API_KEY=your_api_key_here")
        print("方法2: 设置系统环境变量: set DEEPSEEK_API_KEY=your_api_key_here")
        return
    
    # 创建分析器
    analyzer = AIPoemAnalyzer(api_key)
    
    # 示例诗歌
    sample_poem = {
        "title": "静夜思",
        "author": "李白", 
        "paragraphs": [
            "床前明月光，",
            "疑是地上霜。",
            "举头望明月，",
            "低头思故乡。"
        ]
    }
    
    print("=== AI诗歌标签分析演示 ===")
    print(f"分析诗歌: {sample_poem['title']} - {sample_poem['author']}")
    
    # 分析单首诗歌
    result = analyzer.analyze_poem(sample_poem)
    
    if result:
        print("\n分析结果:")
        print(f"风格: {', '.join(result.get('styles', []))}")
        print(f"场景: {', '.join(result.get('scenes', []))}")
        print(f"情感: {', '.join(result.get('emotions', []))}")
        print(f"主题: {', '.join(result.get('themes', []))}")
        print(f"修辞: {', '.join(result.get('rhetoric', []))}")
        print(f"关键词: {', '.join(result.get('keywords', []))}")
        print(f"意境描述: {result.get('artistic_description', '')}")
    else:
        print("分析失败")

if __name__ == "__main__":
    main()