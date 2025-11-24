// 唐诗网站应用主脚本
class TangPoetryApp {
    constructor() {
        this.poems = [];
        this.indexes = {};
        this.statistics = {};
        this.authorRanking = [];
        this.keywordRanking = [];
        this.searchData = [];
        this.currentResults = [];
        this.fuse = null;
        
        this.init();
    }

    // 初始化应用
    async init() {
        try {
            // 等待所有数据加载完成
            await this.loadData();
            this.setupSearch();
            this.renderStatistics();
            this.renderCategories();
            this.setupEventListeners();
            
            console.log('唐诗网站应用初始化完成');
        } catch (error) {
            console.error('初始化失败:', error);
        }
    }

    // 加载数据
    async loadData() {
        // 注意：在实际部署时，这些数据应该通过AJAX请求加载
        // 这里假设数据已经通过script标签加载到全局变量中
        
        this.poems = window.poemsData || [];
        this.indexes = window.indexesData || {};
        this.statistics = window.statisticsData || {};
        this.authorRanking = window.authorRankingData || [];
        this.keywordRanking = window.keywordRankingData || [];
        this.searchData = window.searchData || [];
        
        console.log('数据加载完成:', {
            poems: this.poems.length,
            authors: Object.keys(this.indexes.authors || {}).length,
            keywords: Object.keys(this.indexes.keywords || {}).length
        });
    }

    // 设置搜索功能
    setupSearch() {
        const options = {
            keys: ['title', 'author', 'content', 'keywords'],
            threshold: 0.3,
            includeScore: true,
            includeMatches: true
        };
        
        this.fuse = new Fuse(this.searchData, options);
    }

    // 渲染统计信息
    renderStatistics() {
        const statsContainer = document.getElementById('statisticsCards');
        
        const stats = [
            { title: '总诗歌数', value: this.statistics.total_poems, icon: 'fas fa-book', color: 'primary' },
            { title: '作者数', value: this.statistics.total_authors, icon: 'fas fa-user', color: 'success' },
            { title: '卷数', value: this.statistics.total_volumes, icon: 'fas fa-layer-group', color: 'info' },
            { title: '主题数', value: this.statistics.total_keywords, icon: 'fas fa-tags', color: 'warning' }
        ];

        statsContainer.innerHTML = stats.map(stat => `
            <div class="col-md-3 mb-3">
                <div class="card bg-${stat.color} text-white">
                    <div class="card-body stat-card">
                        <i class="${stat.icon} fa-2x mb-2"></i>
                        <h3>${stat.value}</h3>
                        <p class="mb-0">${stat.title}</p>
                    </div>
                </div>
            </div>
        `).join('');
    }

    // 渲染分类列表
    renderCategories() {
        this.renderAuthorList();
        this.renderDynastyList();
        this.renderKeywordList();
        this.renderVolumeList();
        this.populateFilters();
    }

    // 渲染作者列表
    renderAuthorList() {
        const container = document.getElementById('authorList');
        const topAuthors = this.authorRanking.slice(0, 20);
        
        container.innerHTML = topAuthors.map(author => `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <a href="#" class="author-link" onclick="app.filterByAuthor('${author.author}')">
                    ${author.author}
                </a>
                <span class="badge bg-secondary">${author.count}</span>
            </div>
        `).join('');
    }

    // 渲染朝代列表
    renderDynastyList() {
        const container = document.getElementById('dynastyList');
        const dynasties = this.indexes.dynasties || {};
        
        container.innerHTML = Object.entries(dynasties).map(([dynasty, poems]) => `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <a href="#" class="author-link" onclick="app.filterByDynasty('${dynasty}')">
                    ${dynasty}
                </a>
                <span class="badge bg-secondary">${poems.length}</span>
            </div>
        `).join('');
    }

    // 渲染关键词列表
    renderKeywordList() {
        const container = document.getElementById('keywordList');
        const topKeywords = this.keywordRanking.slice(0, 15);
        
        container.innerHTML = topKeywords.map(keyword => `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <a href="#" class="author-link" onclick="app.filterByKeyword('${keyword.keyword}')">
                    ${keyword.keyword}
                </a>
                <span class="badge bg-secondary">${keyword.count}</span>
            </div>
        `).join('');
    }

    // 渲染卷数列表
    renderVolumeList() {
        const container = document.getElementById('volumeList');
        const volumes = Object.entries(this.indexes.volumes || {})
            .sort((a, b) => b[1].length - a[1].length)
            .slice(0, 20);
        
        container.innerHTML = volumes.map(([volume, poems]) => `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <a href="#" class="author-link" onclick="app.filterByVolume('${volume}')">
                    ${volume}
                </a>
                <span class="badge bg-secondary">${poems.length}</span>
            </div>
        `).join('');
    }

    // 填充筛选器下拉菜单
    populateFilters() {
        this.populateAuthorFilter();
        this.populateKeywordFilter();
    }

    // 填充作者筛选器
    populateAuthorFilter() {
        const select = document.getElementById('authorFilter');
        const authors = this.authorRanking.slice(0, 50);
        
        select.innerHTML = '<option value="">选择作者</option>' + 
            authors.map(author => `
                <option value="${author.author}">${author.author} (${author.count})</option>
            `).join('');
    }

    // 填充关键词筛选器
    populateKeywordFilter() {
        const select = document.getElementById('keywordFilter');
        const keywords = this.keywordRanking.slice(0, 30);
        
        select.innerHTML = '<option value="">选择主题</option>' + 
            keywords.map(keyword => `
                <option value="${keyword.keyword}">${keyword.keyword} (${keyword.count})</option>
            `).join('');
    }

    // 设置事件监听器
    setupEventListeners() {
        const searchInput = document.getElementById('searchInput');
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.searchPoems();
            }
        });
    }

    // 搜索诗歌
    searchPoems() {
        const query = document.getElementById('searchInput').value.trim();
        
        if (!query) {
            this.showAllPoems();
            return;
        }

        const results = this.fuse.search(query);
        this.currentResults = results.map(result => result.item);
        
        this.displayResults(this.currentResults, query);
    }

    // 显示所有诗歌
    showAllPoems() {
        this.currentResults = this.poems.slice(0, 50); // 限制显示数量
        this.displayResults(this.currentResults);
    }

    // 按作者筛选
    filterByAuthor(author = null) {
        if (!author) {
            author = document.getElementById('authorFilter').value;
        }
        
        if (!author) {
            this.showAllPoems();
            return;
        }

        const poemIds = this.indexes.authors[author] || [];
        this.currentResults = this.poems.filter(poem => poemIds.includes(poem.id));
        
        this.displayResults(this.currentResults, '', `作者: ${author}`);
    }

    // 按朝代筛选
    filterByDynasty(dynasty = null) {
        if (!dynasty) {
            dynasty = document.getElementById('dynastyFilter').value;
        }
        
        if (!dynasty) {
            this.showAllPoems();
            return;
        }

        const poemIds = this.indexes.dynasties[dynasty] || [];
        this.currentResults = this.poems.filter(poem => poemIds.includes(poem.id));
        
        this.displayResults(this.currentResults, '', `朝代: ${dynasty}`);
    }

    // 按关键词筛选
    filterByKeyword(keyword = null) {
        if (!keyword) {
            keyword = document.getElementById('keywordFilter').value;
        }
        
        if (!keyword) {
            this.showAllPoems();
            return;
        }

        const poemIds = this.indexes.keywords[keyword] || [];
        this.currentResults = this.poems.filter(poem => poemIds.includes(poem.id));
        
        this.displayResults(this.currentResults, '', `主题: ${keyword}`);
    }

    // 按卷数筛选
    filterByVolume(volume) {
        const poemIds = this.indexes.volumes[volume] || [];
        this.currentResults = this.poems.filter(poem => poemIds.includes(poem.id));
        
        this.displayResults(this.currentResults, '', `卷数: ${volume}`);
    }

    // 显示搜索结果
    displayResults(results, searchQuery = '', filterInfo = '') {
        const resultsContainer = document.getElementById('poemsList');
        const resultsInfo = document.getElementById('resultsInfo');
        const resultsCount = document.getElementById('resultsCount');
        const noResults = document.getElementById('noResults');

        // 更新结果信息
        resultsCount.textContent = results.length;
        resultsInfo.style.display = results.length > 0 ? 'block' : 'none';
        
        if (filterInfo) {
            resultsInfo.innerHTML = `找到 <strong>${results.length}</strong> 首诗歌 <span class="text-muted">(${filterInfo})</span>`;
        } else {
            resultsInfo.innerHTML = `找到 <strong>${results.length}</strong> 首诗歌`;
        }

        // 显示/隐藏无结果提示
        noResults.style.display = results.length === 0 ? 'block' : 'none';

        // 渲染结果
        if (results.length > 0) {
            resultsContainer.innerHTML = results.slice(0, 100).map(poem => this.renderPoemCard(poem, searchQuery)).join('');
        } else {
            resultsContainer.innerHTML = '';
        }

        // 滚动到结果区域
        document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
    }

    // 渲染诗歌卡片
    renderPoemCard(poem, searchQuery = '') {
        const contentPreview = poem.paragraphs.slice(0, 2).join(' ');
        const truncatedContent = contentPreview.length > 100 ?
            contentPreview.substring(0, 100) + '...' : contentPreview;

        return `
            <div class="col-md-6 col-lg-4">
                <div class="card poem-card h-100">
                    <div class="card-body">
                        <h5 class="card-title">
                            <a href="#" class="poem-title-link" onclick="app.showPoemDetail('${poem.id}')">
                                ${this.highlightText(poem.title, searchQuery)}
                            </a>
                        </h5>
                        <h6 class="card-subtitle mb-2 text-muted">
                            <a href="#" class="author-link" onclick="app.filterByAuthor('${poem.author}')">
                                ${poem.author}
                            </a>
                            <span class="badge bg-light text-dark ms-2">${poem.dynasty}</span>
                        </h6>
                        <p class="card-text">${this.highlightText(truncatedContent, searchQuery)}</p>
                        
                        <div class="mb-2">
                            ${poem.keywords.slice(0, 3).map(keyword =>
                                `<span class="keyword-tag" onclick="app.filterByKeyword('${keyword}')">${keyword}</span>`
                            ).join('')}
                        </div>
                        
                        <small class="text-muted">${poem.volume} · 第${poem.number}首</small>
                    </div>
                    <div class="card-footer bg-transparent">
                        <button class="btn btn-sm btn-outline-primary" onclick="app.showPoemDetail('${poem.id}')">
                            查看全文
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    // 高亮搜索文本
    highlightText(text, query) {
        if (!query || !text) return text;
        
        const regex = new RegExp(`(${this.escapeRegex(query)})`, 'gi');
        return text.replace(regex, '<mark class="search-highlight">$1</mark>');
    }

    // 转义正则表达式特殊字符
    escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // 显示诗歌详情
    showPoemDetail(poemId) {
        const poem = this.poems.find(p => p.id === poemId);
        if (!poem) return;

        const modalTitle = document.getElementById('poemModalTitle');
        const modalBody = document.getElementById('poemModalBody');

        modalTitle.textContent = poem.title;
        
        modalBody.innerHTML = `
            <div class="row">
                <div class="col-md-8">
                    <h6>作者: 
                        <a href="#" class="author-link" onclick="app.filterByAuthor('${poem.author}')">
                            ${poem.author}
                        </a>
                        <span class="badge bg-secondary ms-2">${poem.dynasty}</span>
                    </h6>
                    <p><strong>出处:</strong> ${poem.volume} 第${poem.number}首</p>
                    
                    <div class="poem-content mt-4">
                        ${poem.paragraphs.map(paragraph => 
                            `<p class="mb-2">${paragraph}</p>`
                        ).join('')}
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header">
                            <strong>主题标签</strong>
                        </div>
                        <div class="card-body">
                            ${poem.keywords.map(keyword => 
                                `<span class="keyword-tag" onclick="app.filterByKeyword('${keyword}')">${keyword}</span>`
                            ).join('')}
                        </div>
                    </div>
                    
                    ${poem.biography ? `
                    <div class="card mt-3">
                        <div class="card-header">
                            <strong>作者简介</strong>
                        </div>
                        <div class="card-body">
                            <p class="small">${poem.biography}</p>
                        </div>
                    </div>
                    ` : ''}
                </div>
            </div>
        `;

        // 显示模态框
        const modal = new bootstrap.Modal(document.getElementById('poemModal'));
        modal.show();
    }
}

// 创建全局应用实例
const app = new TangPoetryApp();

// 全局函数供HTML调用
function searchPoems() {
    app.searchPoems();
}

function filterByAuthor() {
    app.filterByAuthor();
}

function filterByDynasty() {
    app.filterByDynasty();
}

function filterByKeyword() {
    app.filterByKeyword();
}