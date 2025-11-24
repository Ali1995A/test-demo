# 唐诗网站部署指南

## 项目概述

本项目将《御定全唐詩》的JSON数据转换为适合网站使用的格式，并提供了完整的前端界面用于分类浏览和检索。采用现代化的交互设计，支持链接式检索和完整内容展示。

## 文件结构

```
御定全唐詩/
├── json/                          # 原始JSON数据
│   ├── 001.json
│   ├── 002.json
│   └── ...
├── website_data/                  # 预处理后的网站数据
│   ├── poems_data.json           # 诗歌主数据
│   ├── indexes.json              # 各类索引
│   ├── statistics.json           # 统计信息
│   ├── author_ranking.json       # 作者排名
│   ├── keyword_ranking.json      # 关键词排名
│   └── search_data.json          # 搜索数据
├── website/                      # 网站前端文件
│   ├── index.html               # 主页面
│   ├── app.js                   # 应用脚本
│   ├── test_website.html        # 功能测试页面
│   └── data/                    # 网站数据文件
│       ├── poems_data.json      # 诗歌主数据
│       ├── indexes.json         # 各类索引
│       ├── statistics.json      # 统计信息
│       ├── author_ranking.json  # 作者排名
│       ├── keyword_ranking.json # 关键词排名
│       └── search_data.json     # 搜索数据
├── 数据处理工具/
│   ├── json_query_tool.py       # JSON查询工具
│   ├── website_data_preprocessor.py # 网站数据预处理
│   └── generate_report.py       # 报告生成器
└── 文档/
    ├── website_structure.md      # 网站结构规划
    └── website_deployment_guide.md # 本文件
```

## 部署步骤

### 1. 数据预处理

首先运行数据预处理脚本，生成网站所需的数据文件：

```bash
python website_data_preprocessor.py
```

这将生成 `website_data/` 目录下的所有数据文件。

### 2. 数据文件复制

将预处理生成的数据文件复制到网站目录：

```bash
# Windows系统
mkdir website\data && copy website_data\*.json website\data\

# Linux/Mac系统
mkdir -p website/data && cp website_data/*.json website/data/
```

### 3. 网站部署

#### 选项A：本地部署（开发环境）

1. 安装Python HTTP服务器：
```bash
# 在项目根目录运行
python -m http.server 8000
```

2. 打开浏览器访问：`http://localhost:8000/website/`

### 4. 功能测试

部署完成后，可以使用测试页面验证网站功能：

1. 访问测试页面：`http://localhost:8000/website/test_website.html`
2. 页面将自动测试数据加载和功能完整性
3. 查看测试结果，确保所有组件正常工作

#### 选项B：静态网站部署（生产环境）

1. 将以下文件上传到Web服务器：
   - `website/index.html`
   - `website/app.js`
   - `website/test_website.html`（可选，用于功能测试）
   - `website/data/` 目录下的所有JSON文件

2. 确保Web服务器正确配置MIME类型：
```nginx
# Nginx配置示例
location ~* \.json$ {
    add_header Content-Type application/json;
    add_header Access-Control-Allow-Origin "*";
}
```

#### 选项C：使用CDN部署

1. 将数据文件上传到CDN
2. 修改 `index.html` 中的数据文件路径为CDN地址

## 网站功能特性

### 1. 智能检索系统
- **链接式检索**：搜索结果以可点击的标题链接形式展示
- **词条详情**：点击标题或"查看全文"按钮进入完整词条页面
- **标签关联**：关键词标签直接关联相关内容，点击可快速筛选
- **作者关联**：点击作者名称查看该作者所有作品

### 2. 分类浏览
- **按作者**：显示前20名作者，点击可查看该作者所有诗歌
- **按朝代**：初唐、盛唐、中唐、晚唐分类
- **按主题**：基于关键词的主题分类（月、山、水、花等）
- **按卷数**：按《御定全唐詩》原书卷数分类

### 3. 搜索功能
- **全文搜索**：支持标题、作者、内容的模糊搜索
- **高级筛选**：作者、朝代、主题多条件筛选
- **实时高亮**：搜索结果中高亮显示匹配内容

### 4. 内容展示
- **搜索结果**：显示诗歌标题、作者、朝代、内容预览和关键词标签
- **完整词条**：模态框展示完整的诗歌内容、作者简介和主题标签
- **统计面板**：数据库整体统计信息

## 技术架构

### 前端技术栈
- **HTML5** + **CSS3** + **原生JavaScript**
- **Bootstrap 5** - UI框架
- **Font Awesome** - 图标库
- **Fuse.js** - 模糊搜索库

### 数据架构
- **主数据文件**：`poems_data.json` - 完整的诗歌数据
- **索引文件**：`indexes.json` - 各类索引数据
- **搜索数据**：`search_data.json` - 优化的搜索数据结构
- **统计文件**：各类统计和排名数据

## 自定义配置

### 修改主题关键词
在 `website_data_preprocessor.py` 中修改 `extract_keywords` 方法：

```python
def extract_keywords(self, poem):
    # 自定义主题关键词列表
    theme_keywords = ['月', '山', '水', '花', '春', '秋', '风', '云', '雨', '雪']
    # ... 其他代码
```

### 调整搜索参数
在 `app.js` 中修改Fuse.js配置：

```javascript
const options = {
    keys: ['title', 'author', 'content', 'keywords'],
    threshold: 0.3,  // 调整搜索敏感度
    includeScore: true,
    includeMatches: true
};
```

### 添加新的分类维度
1. 在预处理脚本中添加新的索引
2. 在前端添加对应的筛选器和展示组件
3. 更新数据加载和筛选逻辑

## 性能优化建议

### 1. 数据分页
对于大量数据，建议实现分页加载：
```javascript
// 在app.js中添加分页逻辑
const ITEMS_PER_PAGE = 20;
let currentPage = 1;

function loadPage(page) {
    const start = (page - 1) * ITEMS_PER_PAGE;
    const end = start + ITEMS_PER_PAGE;
    return results.slice(start, end);
}
```

### 2. 懒加载
对于图片或大量文本内容，实现懒加载：
```javascript
// 使用Intersection Observer API
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            // 加载内容
        }
    });
});
```

### 3. 数据压缩
对于生产环境，可以考虑数据压缩：
```javascript
// 使用gzip压缩JSON数据
// 在服务器端配置压缩
```

## 扩展功能建议

### 1. 用户功能
- 收藏诗歌
- 阅读历史
- 个人诗集

### 2. 社交功能
- 诗歌分享
- 评论系统
- 朗读功能

### 3. 数据分析
- 阅读统计
- 热门诗歌排行
- 用户行为分析

### 4. 移动端优化
- 响应式设计优化
- PWA支持
- 离线缓存

## 故障排除

### 常见问题

1. **数据加载失败**
   - 检查JSON文件路径
   - 验证JSON格式是否正确
   - 检查CORS配置

2. **搜索功能异常**
   - 检查Fuse.js是否正确加载
   - 验证搜索数据格式
   - 检查搜索参数配置

3. **页面显示异常**
   - 检查Bootstrap和Font Awesome CDN
   - 验证JavaScript控制台错误
   - 检查浏览器兼容性

### 调试技巧

1. 打开浏览器开发者工具
2. 检查网络请求状态
3. 查看JavaScript控制台错误信息
4. 验证数据加载情况

## 维护和更新

### 数据更新
当有新的诗歌数据时：
1. 将新JSON文件放入 `json/` 目录
2. 重新运行数据预处理脚本
3. 更新网站数据文件

### 功能更新
1. 备份现有代码
2. 在开发环境测试新功能
3. 部署到生产环境

## 安全考虑

1. **XSS防护**：对所有用户输入进行转义
2. **CORS配置**：合理配置跨域请求
3. **数据验证**：验证所有输入数据的格式
4. **HTTPS**：生产环境使用HTTPS

## 性能监控

建议添加性能监控：
- 页面加载时间
- 搜索响应时间
- 用户交互统计
- 错误日志收集

---

通过本指南，您可以成功部署一个功能完整的《御定全唐詩》在线检索网站，为用户提供丰富的诗歌浏览和搜索体验。