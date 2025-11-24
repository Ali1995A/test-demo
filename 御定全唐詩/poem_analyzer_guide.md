# 古诗词智能分析工具使用指南

## 工具概述

本工具是一个智能的古诗词分析系统，能够自动分析诗词内容，根据风格、场景、类型等维度为数据增加更多智能标签，极大丰富诗词数据的检索和分类能力。

## 功能特性

### 🎯 智能分析维度
- **风格分析**: 豪放、婉约、田园、边塞、咏史、抒情、写景
- **场景分析**: 春天、夏天、秋天、冬天、夜晚、早晨、山水、城市、乡村
- **情感分析**: 喜悦、忧愁、思念、孤独、豪迈、闲适
- **主题分析**: 爱情、友情、家国、人生、自然、哲理
- **修辞分析**: 比喻、对仗、夸张、拟人、借代
- **复杂度评分**: 0-10分的复杂度评估
- **长度分类**: 短诗、中诗、长诗、超长诗

### 🔍 增强搜索能力
通过智能标签，可以实现更精确的多维度搜索：
- 按风格搜索：`豪放风格的诗`
- 按场景搜索：`春天的诗`、`夜晚的诗`
- 按情感搜索：`忧愁的诗`、`喜悦的诗`
- 组合搜索：`春天+婉约+忧愁的诗`

## 安装依赖

```bash
# 安装jieba分词库
pip install jieba

# 或者使用conda
conda install jieba
```

## 快速开始

### 1. 单首诗词分析演示

```bash
python poem_analyzer_demo.py
```

这将演示如何分析单首诗词（如《静夜思》）并展示分析结果。

### 2. 批量分析全部数据

```bash
python poem_analyzer.py
```

这将分析全部43,103首诗词数据，生成增强的数据文件。

### 3. 自定义分析样本

在 `poem_analyzer.py` 中修改 `sample_size` 参数：

```python
# 分析前1000首诗词进行测试
sample_size = 1000

# 分析全部诗词
sample_size = None
```

## 输出文件

分析完成后会生成以下文件：

### 1. 增强数据文件
- **文件**: `website_data/enhanced_poems_data.json`
- **内容**: 包含原始数据 + 智能分析标签
- **结构**:
```json
{
  "title": "静夜思",
  "author": "李白",
  "paragraphs": ["..."],
  "analysis": {
    "styles": ["抒情", "写景"],
    "scenes": ["夜晚"],
    "emotions": ["思念"],
    "themes": ["人生"],
    "complexity_score": 6.5
  },
  "enhanced_tags": {
    "styles": ["抒情", "写景"],
    "scenes": ["夜晚"],
    "emotions": ["思念"],
    "themes": ["人生"],
    "rhetoric": ["比喻"],
    "complexity": 6.5,
    "length_category": "短诗"
  }
}
```

### 2. 分析统计文件
- **文件**: `website_data/analysis_statistics.json`
- **内容**: 整体分析统计信息
- **用途**: 了解数据集的整体特征分布

## 集成到网站

### 1. 更新网站数据

将增强数据文件复制到网站目录：

```bash
# Windows
copy website_data\enhanced_poems_data.json website\data\

# Linux/Mac
cp website_data/enhanced_poems_data.json website/data/
```

### 2. 修改网站搜索功能

在 `website/app.js` 中添加新的搜索维度：

```javascript
// 在setupSearch方法中添加新的搜索字段
const options = {
    keys: [
        'title', 
        'author', 
        'content', 
        'keywords',
        'enhanced_tags.styles',    // 新增：风格搜索
        'enhanced_tags.scenes',    // 新增：场景搜索
        'enhanced_tags.emotions',  // 新增：情感搜索
        'enhanced_tags.themes'     // 新增：主题搜索
    ],
    threshold: 0.3
};
```

### 3. 添加新的筛选器

在HTML中添加新的筛选下拉菜单：

```html
<!-- 风格筛选 -->
<select id="styleFilter" class="form-select" onchange="filterByStyle()">
    <option value="">选择风格</option>
    <option value="豪放">豪放</option>
    <option value="婉约">婉约</option>
    <option value="田园">田园</option>
    <!-- 更多风格选项 -->
</select>

<!-- 场景筛选 -->
<select id="sceneFilter" class="form-select" onchange="filterByScene()">
    <option value="">选择场景</option>
    <option value="春天">春天</option>
    <option value="夜晚">夜晚</option>
    <option value="山水">山水</option>
    <!-- 更多场景选项 -->
</select>
```

### 4. 添加筛选函数

在JavaScript中添加新的筛选函数：

```javascript
// 按风格筛选
filterByStyle(style = null) {
    if (!style) {
        style = document.getElementById('styleFilter').value;
    }
    
    if (!style) {
        this.showAllPoems();
        return;
    }

    this.currentResults = this.poems.filter(poem => 
        poem.enhanced_tags && poem.enhanced_tags.styles.includes(style)
    );
    
    this.displayResults(this.currentResults, '', `风格: ${style}`);
}

// 按场景筛选
filterByScene(scene = null) {
    if (!scene) {
        scene = document.getElementById('sceneFilter').value;
    }
    
    if (!scene) {
        this.showAllPoems();
        return;
    }

    this.currentResults = this.poems.filter(poem => 
        poem.enhanced_tags && poem.enhanced_tags.scenes.includes(scene)
    );
    
    this.displayResults(this.currentResults, '', `场景: ${scene}`);
}
```

## 自定义分析规则

### 1. 添加新的风格关键词

在 `poem_analyzer.py` 的 `setup_keywords` 方法中添加：

```python
self.style_keywords = {
    '豪放': ['豪情', '壮志', '英雄', ...],
    '婉约': ['柔情', '相思', '离别', ...],
    # 添加新的风格
    '浪漫': ['浪漫', '梦幻', '想象', '奇幻'],
    '现实': ['现实', '真实', '实际', '生活']
}
```

### 2. 调整分析权重

修改分析方法的评分逻辑：

```python
def analyze_style(self, content, words):
    styles = []
    for style, keywords in self.style_keywords.items():
        # 可以调整评分算法
        score = sum(content.count(keyword) * 2 for keyword in keywords)  # 权重加倍
        if score > 0:
            styles.append({
                'style': style,
                'score': score,
                'keywords_found': [kw for kw in keywords if kw in content]
            })
```

### 3. 自定义复杂度算法

修改 `calculate_complexity` 方法：

```python
def calculate_complexity(self, content, words):
    # 基于更多因素计算复杂度
    unique_words = len(set(word for word, flag in words))
    total_words = len(words)
    lexical_diversity = unique_words / total_words if total_words > 0 else 0
    
    # 考虑句子长度变化
    sentence_lengths = [len(p) for p in content.split('，')]
    length_variance = np.var(sentence_lengths) if len(sentence_lengths) > 1 else 0
    
    complexity = lexical_diversity * 8 + length_variance * 2
    return min(round(complexity, 2), 10)
```

## 性能优化建议

### 1. 分批处理
对于大量数据，建议分批处理：

```python
def batch_analyze_with_chunks(self, poems_data, chunk_size=1000):
    """分批处理大量数据"""
    results = []
    total_chunks = (len(poems_data) + chunk_size - 1) // chunk_size
    
    for i in range(total_chunks):
        start = i * chunk_size
        end = start + chunk_size
        chunk = poems_data[start:end]
        
        print(f"处理第 {i+1}/{total_chunks} 批数据...")
        chunk_results = self.batch_analyze(chunk)
        results.extend(chunk_results)
    
    return results
```

### 2. 缓存分析结果
避免重复分析：

```python
import hashlib

def get_poem_hash(self, poem):
    """生成诗词内容的哈希值用于缓存"""
    content = poem.get('title', '') + ' '.join(poem.get('paragraphs', []))
    return hashlib.md5(content.encode('utf-8')).hexdigest()
```

## 故障排除

### 常见问题

1. **内存不足**
   - 解决方案：减少 `sample_size` 或使用分批处理

2. **分词不准确**
   - 解决方案：在 `setup_jieba` 方法中添加更多自定义词典

3. **分析结果不理想**
   - 解决方案：调整关键词库和评分阈值

4. **文件编码问题**
   - 解决方案：确保所有文件使用UTF-8编码

### 调试技巧

1. 使用演示脚本测试单首诗词分析
2. 检查控制台输出的错误信息
3. 验证输入数据的格式和完整性
4. 检查输出文件的JSON格式

## 扩展功能

### 1. 机器学习集成
可以集成机器学习模型进行更精确的分析：

```python
# 使用预训练模型进行情感分析
from transformers import pipeline

class AdvancedPoemAnalyzer(PoemAnalyzer):
    def __init__(self):
        super().__init__()
        self.sentiment_analyzer = pipeline('sentiment-analysis')
    
    def advanced_emotion_analysis(self, content):
        """使用机器学习进行情感分析"""
        result = self.sentiment_analyzer(content[:512])  # 限制长度
        return result[0]
```

### 2. 可视化分析
生成分析结果的可视化报告：

```python
import matplotlib.pyplot as plt

def generate_visualization(self, stats):
    """生成统计可视化"""
    # 风格分布饼图
    styles = list(stats['style_distribution'].keys())
    counts = list(stats['style_distribution'].values())
    
    plt.figure(figsize=(10, 6))
    plt.pie(counts, labels=styles, autopct='%1.1f%%')
    plt.title('诗词风格分布')
    plt.savefig('style_distribution.png')
```

---

通过本工具，您可以为《御定全唐詩》数据增加丰富的智能标签，极大提升搜索和分类的精确度，为用户提供更优质的诗词检索体验。