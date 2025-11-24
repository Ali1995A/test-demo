# JSON查询工具使用指南

## 概述

这是一个类似jq命令的JSON查询工具，专门用于查询和分析《御定全唐詩》数据库。该工具提供了多种查询和统计功能，可以方便地检索唐诗数据。

## 安装要求

- Python 3.x
- 标准库：json, os, sys, argparse, pathlib

## 基本用法

```bash
python json_query_tool.py [选项]
```

## 主要功能

### 1. 基本信息显示
不提供任何参数时显示数据库基本信息：

```bash
python json_query_tool.py
```

输出示例：
```
唐诗数据库信息:
  总诗歌数: 43103
  作者数: 2536
  卷数: 900
```

### 2. 按关键词查询
搜索包含特定关键词的诗歌：

```bash
python json_query_tool.py --keyword 月
python json_query_tool.py -k 月
```

### 3. 按字段查询
按特定字段和值查询：

```bash
# 查询作者为李世民的诗歌
python json_query_tool.py --field author --value 李世民
python json_query_tool.py -f author -v 李世民

# 精确匹配
python json_query_tool.py --field author --value 李世民 --exact
```

### 4. 统计功能
按字段统计数量：

```bash
# 统计作者分布
python json_query_tool.py --count author
python json_query_tool.py -c author

# 统计卷数分布
python json_query_tool.py --count volume
```

### 5. 列出字段值
列出字段的所有唯一值：

```bash
# 列出所有作者
python json_query_tool.py --list-values author
python json_query_tool.py -l author

# 列出所有卷数
python json_query_tool.py --list-values volume
```

### 6. 输出格式控制
指定输出格式：

```bash
# 简单格式（默认）
python json_query_tool.py --keyword 月 --format simple

# 详细格式
python json_query_tool.py --keyword 月 --format detailed

# JSON格式
python json_query_tool.py --keyword 月 --format json
```

### 7. 指定输出字段
自定义输出字段：

```bash
python json_query_tool.py --keyword 月 --fields title,author
```

## 实用示例

### 查找特定主题的诗歌
```bash
# 查找包含"月"的诗歌
python json_query_tool.py --keyword 月

# 查找包含"山"的诗歌
python json_query_tool.py --keyword 山

# 查找包含"水"的诗歌
python json_query_tool.py --keyword 水
```

### 查找特定作者的诗歌
```bash
# 查找李白的诗歌
python json_query_tool.py --field author --value 李白

# 查找杜甫的诗歌
python json_query_tool.py --field author --value 杜甫
```

### 统计分析
```bash
# 查看作者排名
python json_query_tool.py --count author

# 查看卷数分布
python json_query_tool.py --count volume
```

### 数据探索
```bash
# 查看所有作者
python json_query_tool.py --list-values author

# 查看所有卷数
python json_query_tool.py --list-values volume
```

## 输出格式说明

### 简单格式（默认）
```
1. title: 诗歌标题, author: 作者, volume: 卷数, no#: 编号
2. title: 诗歌标题, author: 作者, volume: 卷数, no#: 编号
...
```

### 详细格式
```
=== 诗歌 1 ===
title: 诗歌标题
author: 作者
volume: 卷数
no#: 编号
biography: 作者简介
内容:
  1. 第一行诗句
  2. 第二行诗句
...
```

### JSON格式
完整的JSON数据结构，便于程序处理。

## 性能说明

- 工具会缓存所有JSON数据，第一次运行较慢，后续查询会更快
- 支持处理43,103首诗歌的大型数据集
- 内存使用优化，适合在普通配置的计算机上运行

## 错误处理

- 如果JSON文件损坏或格式错误，会显示错误信息并跳过该文件
- 如果查询无结果，会显示"找到 0 个结果"
- 如果字段不存在，统计和列表功能会返回空结果

## 扩展功能

如果需要更复杂的查询功能，可以修改 `json_query_tool.py` 文件中的 `JSONQueryTool` 类，添加自定义查询方法。

## 注意事项

- 所有查询都支持中文文本
- 工具会自动处理UTF-8编码
- 关键词查询支持模糊匹配
- 字段查询支持精确匹配和模糊匹配