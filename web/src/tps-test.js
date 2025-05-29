// TPS测试应用主逻辑
class TPSTest {
    constructor() {
        this.chart = null;
        this.isRunning = false;
        this.testData = {
            timestamps: [],
            tpsValues: [],
            totalTokens: 0,
            requestCount: 0,
            startTime: null,
            endTime: null
        };
        this.abortController = null;
        this.initializeChart();
        this.bindEvents();
        this.loadSavedConfig();
    }

    initializeChart() {
        const ctx = document.getElementById('tpsChart').getContext('2d');
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'TPS (Tokens Per Second)',
                    data: [],
                    borderColor: '#00d4ff',
                    backgroundColor: 'rgba(0, 212, 255, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    pointHoverBackgroundColor: '#00d4ff',
                    pointHoverBorderColor: '#fff',
                    pointHoverBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    legend: {
                        display: true,
                        labels: {
                            color: '#fff',
                            font: {
                                size: 14
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: '#00d4ff',
                        borderWidth: 1,
                        displayColors: false,
                        callbacks: {
                            label: function(context) {
                                return `TPS: ${context.parsed.y.toFixed(2)}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: '时间 (秒)',
                            color: '#fff'
                        },
                        ticks: {
                            color: '#fff'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'TPS',
                            color: '#fff'
                        },
                        ticks: {
                            color: '#fff',
                            beginAtZero: true
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                }
            }
        });
    }

    bindEvents() {
        const testButton = document.getElementById('testButton');
        const modelSelect = document.getElementById('modelSelect');
        const customModelInput = document.getElementById('customModel');
        const backendTypeSelect = document.getElementById('backendType');
        const apiUrlInput = document.getElementById('apiUrl');
        const testDuration = document.getElementById('testDuration');
        const minTokens = document.getElementById('minTokens');
        const maxTokens = document.getElementById('maxTokens');

        testButton.addEventListener('click', () => this.toggleTest());

        modelSelect.addEventListener('change', (e) => {
            if (e.target.value === 'custom') {
                customModelInput.disabled = false;
                customModelInput.focus();
            } else {
                customModelInput.disabled = true;
                customModelInput.value = '';
            }
            this.saveConfig();
        });

        backendTypeSelect.addEventListener('change', (e) => {
            const backendUrls = {
                'vllm': 'http://localhost:8000/v1',
                'sglang': 'http://localhost:30000',
                'ollama': 'http://localhost:11434',
                'custom': ''
            };
            
            if (e.target.value !== 'custom') {
                apiUrlInput.value = backendUrls[e.target.value];
            }
            this.saveConfig();
        });

        // 保存配置
        document.querySelectorAll('input, select').forEach(element => {
            element.addEventListener('change', () => this.saveConfig());
        });
    }

    async loadModels() {
        try {
            const config = this.getConfig();
            const headers = {
                'Content-Type': 'application/json'
            };
            
            if (config.apiKey) {
                headers['Authorization'] = `Bearer ${config.apiKey}`;
            }

            const response = await fetch(`${config.apiUrl}/models`, {
                method: 'GET',
                headers: headers
            });

            if (!response.ok) {
                throw new Error(`获取模型列表失败: ${response.status}`);
            }

            const data = await response.json();
            return data.data.map(model => model.id);
        } catch (error) {
            this.log(`获取模型列表错误: ${error.message}`, 'error');
            return [];
        }
    }

    async loadSavedConfig() {
        const savedConfig = localStorage.getItem('tpsTestConfig');
        if (savedConfig) {
            const config = JSON.parse(savedConfig);
            document.getElementById('apiUrl').value = config.apiUrl || 'http://localhost:8000/v1';
            document.getElementById('apiKey').value = config.apiKey || '';
            document.getElementById('testDuration').value = config.testDuration || 30;
            document.getElementById('minTokens').value = config.minTokens || 10;
            document.getElementById('maxTokens').value = config.maxTokens || 100;

            // 获取模型列表并更新选择器
            const models = await this.loadModels();
            const modelSelect = document.getElementById('modelSelect');
            
            // 清空现有选项
            modelSelect.innerHTML = '';
            
            // 添加默认选项
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = '-- 选择模型 --';
            modelSelect.appendChild(defaultOption);
            
            // 添加获取到的模型
            models.forEach(model => {
                const option = document.createElement('option');
                option.value = model;
                option.textContent = model;
                modelSelect.appendChild(option);
            });
            
            // 添加自定义选项
            const customOption = document.createElement('option');
            customOption.value = 'custom';
            customOption.textContent = '自定义模型';
            modelSelect.appendChild(customOption);
            
            // 恢复选中的模型
            if (config.model) {
                if (models.includes(config.model)) {
                    modelSelect.value = config.model;
                } else if (config.model === 'custom' && config.customModel) {
                    modelSelect.value = 'custom';
                    document.getElementById('customModel').value = config.customModel;
                    document.getElementById('customModel').disabled = false;
                }
            }
        }
    }

    saveConfig() {
        const config = {
            model: document.getElementById('modelSelect').value,
            customModel: document.getElementById('customModel').value,
            apiUrl: document.getElementById('apiUrl').value,
            apiKey: document.getElementById('apiKey').value,
            testDuration: document.getElementById('testDuration').value,
            minTokens: document.getElementById('minTokens').value,
            maxTokens: document.getElementById('maxTokens').value,
            backendType: document.getElementById('backendType').value
        };
        localStorage.setItem('tpsTestConfig', JSON.stringify(config));
    }

    toggleTest() {
        if (this.isRunning) {
            this.stopTest();
        } else {
            this.startTest();
        }
    }

    async startTest() {
        const testButton = document.getElementById('testButton');
        testButton.textContent = '停止测试';
        testButton.classList.add('testing');
        this.isRunning = true;

        // 重置数据
        this.testData = {
            timestamps: [],
            tpsValues: [],
            totalTokens: 0,
            requestCount: 0,
            startTime: Date.now(),
            endTime: null
        };

        // 清空图表
        this.chart.data.labels = [];
        this.chart.data.datasets[0].data = [];
        this.chart.update();

        // 重置统计
        this.updateStats(0, 0, 0, 0);

        // 获取配置
        const config = this.getConfig();
        this.log('开始测试...', 'success');
        this.log(`模型: ${config.model}`);
        this.log(`API URL: ${config.apiUrl}`);
        this.log(`测试时长: ${config.testDuration}秒`);

        this.abortController = new AbortController();

        try {
            await this.runTest(config);
        } catch (error) {
            if (error.name !== 'AbortError') {
                this.log(`测试错误: ${error.message}`, 'error');
            }
        } finally {
            this.stopTest();
        }
    }

    stopTest() {
        const testButton = document.getElementById('testButton');
        testButton.textContent = '开始测试';
        testButton.classList.remove('testing');
        this.isRunning = false;

        if (this.abortController) {
            this.abortController.abort();
        }

        this.testData.endTime = Date.now();
        this.log('测试已停止', 'success');
        
        // 计算最终统计
        if (this.testData.tpsValues.length > 0) {
            const avgTps = this.testData.tpsValues.reduce((a, b) => a + b, 0) / this.testData.tpsValues.length;
            const maxTps = Math.max(...this.testData.tpsValues);
            this.log(`平均 TPS: ${avgTps.toFixed(2)}, 最高 TPS: ${maxTps.toFixed(2)}`);
        }
    }

    getConfig() {
        const modelSelect = document.getElementById('modelSelect').value;
        const customModel = document.getElementById('customModel').value;
        const model = modelSelect === 'custom' ? customModel : modelSelect;

        return {
            model: model,
            apiUrl: document.getElementById('apiUrl').value,
            apiKey: document.getElementById('apiKey').value,
            testDuration: parseInt(document.getElementById('testDuration').value),
            minTokens: parseInt(document.getElementById('minTokens').value),
            maxTokens: parseInt(document.getElementById('maxTokens').value),
            backendType: document.getElementById('backendType').value
        };
    }

    async runTest(config) {
        const testEndTime = Date.now() + (config.testDuration * 1000);
        const updateInterval = 1000; // 每秒更新一次
        let lastUpdateTime = Date.now();
        let tokensInInterval = 0;
        let requestsInInterval = 0;

        // 并发请求数
        const concurrentRequests = 3;
        const activeRequests = new Set();

        const makeRequest = async () => {
            if (!this.isRunning || Date.now() >= testEndTime) {
                return;
            }

            const requestId = Math.random().toString(36).substr(2, 9);
            activeRequests.add(requestId);

            try {
                const startTime = Date.now();
                const response = await this.callAPI(config);
                const endTime = Date.now();
                
                if (response && response.usage) {
                    const tokens = response.usage.completion_tokens || 0;
                    this.testData.totalTokens += tokens;
                    tokensInInterval += tokens;
                    requestsInInterval++;
                    this.testData.requestCount++;

                    // 更新当前token数
                    document.getElementById('totalTokens').textContent = this.testData.totalTokens;
                }

                // 检查是否需要更新图表
                const currentTime = Date.now();
                if (currentTime - lastUpdateTime >= updateInterval) {
                    const elapsedSeconds = (currentTime - this.testData.startTime) / 1000;
                    const intervalSeconds = (currentTime - lastUpdateTime) / 1000;
                    const currentTps = tokensInInterval / intervalSeconds;

                    // 更新图表
                    this.testData.timestamps.push(elapsedSeconds);
                    this.testData.tpsValues.push(currentTps);
                    
                    this.chart.data.labels.push(elapsedSeconds.toFixed(0));
                    this.chart.data.datasets[0].data.push(currentTps);
                    
                    // 限制数据点数量
                    if (this.chart.data.labels.length > 60) {
                        this.chart.data.labels.shift();
                        this.chart.data.datasets[0].data.shift();
                    }
                    
                    this.chart.update();

                    // 更新统计
                    const avgTps = this.testData.tpsValues.reduce((a, b) => a + b, 0) / this.testData.tpsValues.length;
                    const maxTps = Math.max(...this.testData.tpsValues);
                    this.updateStats(currentTps, avgTps, maxTps, this.testData.totalTokens);

                    // 重置间隔计数
                    tokensInInterval = 0;
                    requestsInInterval = 0;
                    lastUpdateTime = currentTime;
                }

            } catch (error) {
                if (error.name !== 'AbortError') {
                    this.log(`请求错误: ${error.message}`, 'error');
                }
            } finally {
                activeRequests.delete(requestId);
                
                // 继续下一个请求
                if (this.isRunning && Date.now() < testEndTime) {
                    setTimeout(() => makeRequest(), 100);
                }
            }
        };

        // 启动并发请求
        for (let i = 0; i < concurrentRequests; i++) {
            makeRequest();
        }

        // 等待所有请求完成或超时
        while (this.isRunning && (Date.now() < testEndTime || activeRequests.size > 0)) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }
    }

    async callAPI(config) {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (config.apiKey) {
            headers['Authorization'] = `Bearer ${config.apiKey}`;
        }

        const requestBody = {
            model: config.model,
            messages: [
                {
                    role: "system",
                    content: "You are a helpful assistant."
                },
                {
                    role: "user",
                    content: "请详细介绍一下人工智能的发展历史和未来趋势。"
                }
            ],
            max_tokens: config.maxTokens,
            temperature: 0.7,
            stream: false
        };

        const response = await fetch(`${config.apiUrl}/chat/completions`, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(requestBody),
            signal: this.abortController.signal
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`API错误 (${response.status}): ${errorText}`);
        }

        return await response.json();
    }

    updateStats(current, avg, max, total) {
        document.getElementById('currentTps').textContent = current.toFixed(2);
        document.getElementById('avgTps').textContent = avg.toFixed(2);
        document.getElementById('maxTps').textContent = max.toFixed(2);
        document.getElementById('totalTokens').textContent = total;
    }

    log(message, type = 'info') {
        const logContainer = document.getElementById('logContainer');
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${type}`;
        const timestamp = new Date().toLocaleTimeString();
        logEntry.textContent = `[${timestamp}] ${message}`;
        logContainer.appendChild(logEntry);
        logContainer.scrollTop = logContainer.scrollHeight;

        // 限制日志条目数量
        while (logContainer.children.length > 100) {
            logContainer.removeChild(logContainer.firstChild);
        }
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new TPSTest();
});
