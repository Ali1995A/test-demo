# AI诗歌标签分析器使用指南

基于DeepSeek API的智能诗歌标签生成与检索系统

## 📋 概述

本系统使用DeepSeek大模型为唐诗自动生成智能标签，包括风格、场景、情感、主题等多维度分析，使诗歌数据具备更丰富的语义信息，便于精确检索和分类。

## 🛠️ 工具组件

### 1. 核心分析器
- **`deepseek_poem_analyzer.py`** - AI诗歌分析器核心类
- **`AIPoemAnalyzer`** - 主要分析类，集成DeepSeek API
- **`DeepSeekAPIClient`** - API客户端封装

### 2. 批量处理器
- **`batch_ai_poem_processor.py`** - 批量处理工具
- **`BatchPoemProcessor`** - 批量处理类

### 3. 检索工具
- **`ai_tag_retriever.py`** - 标签检索工具
- **`AITagRetriever`** - 检索器类

### 4. 演示脚本
- **`deepseek_poem_analyzer_demo.py`** - 功能演示

## 🚀 快速开始

### 环境设置

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **获取DeepSeek API密钥**
   - 访问 [DeepSeek官网](https://platform.deepseek.com/) 获取API密钥

3. **配置环境变量**
   
   **方法1: 使用.env文件（推荐）**
   - 编辑 `.env` 文件
   - 设置 `DEEPSEEK_API_KEY=your_api_key_here`
   
   **方法2: 设置系统环境变量**
   ```bash
   # Windows
   set DEEPSEEK_API_KEY=your_api_key_here
   
   # Linux/Mac
   export DEEPSEEK_API_KEY=your_api_key_here
   ```

### 单首诗歌分析测试

```bash
# 测试单首诗歌分析
python deepseek_poem_analyzer.py
```

### 功能演示

```bash
# 运行完整演示
python deepseek_poem_analyzer_demo.py
```

### 批量处理全部诗歌

```bash
# 处理全部诗歌数据（约3600首）
python batch_ai_poem_processor.py

# 测试模式（只处理前10首）
python batch_ai_poem_processor.py --sample 10

# 自定义参数
python batch_ai_poem_processor.py --batch-size 30 --delay 2.0
```

### 标签检索

```bash
# 检索演示
python ai_tag_retriever.py --demo

# 按风格检索
python ai_tag_retriever.py --style 豪放

# 组合检索
python ai_tag_retriever.py --style 豪放 --scene 山水 --emotion 豪迈

# 按关键词检索
python ai_tag_retriever.py --keyword 明月 故乡
```

## 📊 输出文件

处理完成后会生成以下文件：

- **`website_data/ai_enhanced_poems.json`** - 包含AI标签的增强诗歌数据
- **`website_data/ai_analysis_statistics.json`** - 分析统计信息
- **`ai_poem_processing.log`** - 处理日志

## 🏷️ 标签维度

AI生成的标签包含以下维度：

### 1. 风格标签 (Styles)
- 豪放、婉约、田园、边塞、咏史、抒情、写景等

### 2. 场景标签 (Scenes)  
- 春天、夏天、秋天、冬天、夜晚、早晨、山水、城市、乡村等

### 3. 情感标签 (Emotions)
- 喜悦、忧愁、思念、孤独、豪迈、闲适等

### 4. 主题标签 (Themes)
- 爱情、友情、家国、人生、自然、哲理等

### 5. 修辞手法 (Rhetoric)
- 比喻、对仗、夸张、拟人、借代等

### 6. 关键词 (Keywords)
- 提取5-8个最具代表性的关键词

### 7. 意境描述 (Artistic Description)
- 用一段话描述诗歌的意境和艺术特色

## 🔍 检索示例

### 简单检索
```python
from ai_tag_retriever import AITagRetriever

retriever = AITagRetriever()

# 按风格检索
results = retriever.search_by_style(['豪放'])

# 按场景检索  
results = retriever.search_by_scene(['春天'])

# 按情感检索
results = retriever.search_by_emotion(['忧愁'])
```

### 组合检索
```python
# AND 组合检索
criteria = {
    'styles': ['豪放'],
    'scenes': ['山水'],
    'emotions': ['豪迈']
}
results = retriever.search_combined(criteria)

# OR 组合检索
results = retriever.search_by_tags(['style:豪放', 'scene:山水'], 'OR')
```

### 获取可用标签
```python
available_tags = retriever.get_available_tags()
print("可用风格:", available_tags['styles'])
print("可用场景:", available_tags['scenes'])
```

## ⚙️ 配置参数

### 批量处理参数
- `--batch-size`: 批次大小 (默认: 20)
- `--delay`: 请求间隔秒数 (默认: 1.0)
- `--sample`: 样本大小 (测试用)
- `--start/--end`: 处理范围索引

### API参数
- 温度 (temperature): 0.3 (较低温度确保标签一致性)
- 最大token数: 2000
- 模型: deepseek-chat

## 💡 使用建议

### 1. 测试先行
```bash
# 先用小样本测试
python batch_ai_poem_processor.py --sample 5
```

### 2. 调整批次大小
- 网络稳定：批次大小 20-30
- 网络较差：批次大小 10-15
- 请求间隔：1-2秒避免限流

### 3. 错误处理
- 系统会自动记录处理日志
- 失败的诗句会保留原始数据
- 可使用备用分析方案

### 4. 数据集成
AI标签与现有数据结构完全兼容：
```json
{
  "id": "001",
  "title": "静夜思",
  "author": "李白",
  // ... 原有字段
  "ai_analysis": { /* 详细分析结果 */ },
  "ai_tags": { /* 结构化标签 */ }
}
```

## 🎯 应用场景

### 1. 智能搜索
- 多维度组合搜索
- 语义相似度搜索
- 个性化推荐

### 2. 数据分析
- 诗歌风格分布统计
- 作者创作特点分析
- 时代背景研究

### 3. 内容展示
- 标签云展示
- 分类浏览
- 关联推荐

### 4. 教育应用
- 按主题分类学习
- 风格对比分析
- 创作特点研究

## 🔧 故障排除

### 常见问题

1. **API密钥错误**
   ```
   ❌ 请提供DeepSeek API密钥
   ```
   解决方案：检查环境变量设置

2. **数据文件不存在**
   ```
   ❌ 未找到数据文件
   ```
   解决方案：先运行数据预处理脚本

3. **API限流**
   ```
   API请求失败: 429 Too Many Requests
   ```
   解决方案：增加请求间隔 `--delay 2.0`

4. **网络超时**
   ```
   API请求失败: Timeout
   ```
   解决方案：减少批次大小 `--batch-size 10`

### 日志查看
```bash
# 查看处理日志
tail -f ai_poem_processing.log
```

## 📈 性能优化

### 处理速度
- 平均每首诗：3-5秒
- 3600首诗：约3-5小时
- 建议分批处理

### 内存使用
- 索引构建：约50-100MB
- 数据处理：流式处理，内存友好

### 存储空间
- 增强数据：原数据大小 + 30-50%
- 索引文件：自动构建，无需额外存储

## 🔄 更新维护

### 数据更新
当有新诗歌数据时：
```bash
# 重新运行批量处理
python batch_ai_poem_processor.py
```

### 模型升级
如需使用新版模型：
- 修改 `deepseek_poem_analyzer.py` 中的模型参数
- 重新处理数据以获得更好的标签质量

## 📞 技术支持

如有问题请检查：
1. API密钥是否正确
2. 网络连接是否稳定
3. 数据文件路径是否正确
4. 查看详细错误日志

---

**🎉 开始使用AI诗歌标签分析器，享受智能化的诗歌检索体验！**