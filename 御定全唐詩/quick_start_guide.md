# AI诗歌标签工具快速使用指南

## 第一步：环境准备

### 1. 安装依赖包
```bash
pip install -r requirements.txt
```

### 2. 配置API密钥
创建 `.env` 文件，添加您的DeepSeek API密钥：
```bash
echo "DEEPSEEK_API_KEY=您的API密钥" > .env
```

或者直接在命令行设置：
```bash
set DEEPSEEK_API_KEY=您的API密钥
```

## 第二步：选择处理方式

### 方式一：单文件处理（推荐新手）
处理合并后的完整数据集：

```bash
# 测试模式（只处理前5首诗歌）
python batch_ai_poem_processor.py --sample 5

# 处理所有诗歌
python batch_ai_poem_processor.py

# 自定义参数处理
python batch_ai_poem_processor.py --batch-size 10 --delay 2.0
```

### 方式二：文件夹处理
按原始文件结构处理：

```bash
# 测试模式（只处理前2个文件）
python folder_batch_poem_processor.py --sample-files 2

# 处理所有文件
python folder_batch_poem_processor.py

# 处理指定文件范围
python folder_batch_poem_processor.py --start-file 1 --end-file 10
```

## 第三步：查看结果

### 处理完成后会看到：
```
🎉 批量处理完成！
📁 增强数据: website_data/ai_enhanced_poems.json
📊 统计信息: website_data/ai_analysis_statistics.json
📝 处理日志: ai_poem_processing.log
```

### 查看统计摘要：
处理完成后会自动显示统计信息，包括：
- 分析成功率
- 风格分布
- 场景分布  
- 情感分布
- 热门关键词等

## 第四步：使用标签检索

### 1. 启动检索工具
```bash
python ai_tag_retriever.py
```

### 2. 检索示例
```python
# 检索豪放风格的诗歌
retriever.search_by_tags(styles=["豪放"])

# 检索山水场景的诗歌  
retriever.search_by_tags(scenes=["山水"])

# 组合检索
retriever.search_by_tags(
    styles=["婉约"],
    emotions=["忧伤"],
    themes=["离别"]
)
```

## 快速测试流程

### 完整测试流程（推荐）：
```bash
# 1. 设置API密钥
set DEEPSEEK_API_KEY=您的API密钥

# 2. 测试单文件处理
python batch_ai_poem_processor.py --sample 3

# 3. 查看结果
python ai_tag_retriever.py
```

## 常用命令速查

### 单文件处理
```bash
# 快速测试
python batch_ai_poem_processor.py --sample 5

# 完整处理
python batch_ai_poem_processor.py

# 分批处理（处理前1000首）
python batch_ai_poem_processor.py --start 0 --end 1000
```

### 文件夹处理
```bash
# 快速测试
python folder_batch_poem_processor.py --sample-files 2

# 完整处理
python folder_batch_poem_processor.py

# 分批处理（处理前50个文件）
python folder_batch_poem_processor.py --start-file 1 --end-file 50
```

### 检索工具
```bash
# 启动交互式检索
python ai_tag_retriever.py

# 直接检索
python ai_tag_retriever.py --style 豪放 --scene 山水
```

## 故障排除

### 常见问题：

1. **API密钥错误**
   ```bash
   # 检查.env文件
   cat .env
   # 或重新设置
   set DEEPSEEK_API_KEY=新的API密钥
   ```

2. **网络连接问题**
   ```bash
   # 增加延迟时间
   python batch_ai_poem_processor.py --delay 3.0
   ```

3. **查看详细日志**
   ```bash
   # 查看处理日志
   tail -f ai_poem_processing.log
   ```

## 下一步操作

处理完成后，您可以使用以下工具：

1. **标签检索**：`python ai_tag_retriever.py`
2. **数据查看**：查看生成的JSON文件
3. **统计分析**：查看统计信息文件

现在就开始为您的诗歌添加智能标签吧！🎯