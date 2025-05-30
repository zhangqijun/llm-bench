// 压测结果页面逻辑
class BenchmarkResults {
    constructor() {
        this.charts = {};
        this.resultsData = null;
        this.init();
    }

    init() {
        // 从URL参数或localStorage获取结果数据
        this.loadResultsData();
        
        // 如果有数据，立即显示结果
        if (this.resultsData) {
            this.displayResults();
        } else {
            // 模拟加载过程
            setTimeout(() => {
                this.loadSampleData();
                this.displayResults();
            }, 1500);
        }
    }

    loadResultsData() {
        // 尝试从URL参数获取数据
        const urlParams = new URLSearchParams(window.location.search);
        const dataParam = urlParams.get('data');
        
        if (dataParam) {
            try {
                this.resultsData = JSON.parse(decodeURIComponent(dataParam));
                return;
            } catch (e) {
                console.error('Failed to parse URL data:', e);
            }
        }

        // 尝试从localStorage获取数据
        const storedData = localStorage.getItem('benchmarkResults');
        if (storedData) {
            try {
                this.resultsData = JSON.parse(storedData);
                return;
            } catch (e) {
                console.error('Failed to parse stored data:', e);
            }
        }

        // 如果都没有，使用示例数据
        this.loadSampleData();
    }

    loadSampleData() {
        // 示例数据，实际使用时会被真实数据替换
        this.resultsData = {
            testConfig: {
                model: 'DeepSeek-R1-Distill-Qwen-7B',
                apiUrl: 'http://localhost:8000/v1',
                parallel: 3,
                dataset: 'openqa',
                testTime: new Date().toLocaleString(),
                status: 'success'
            },
            metrics: {
                total_requests: 100,
                successful_requests: 98,
                failed_requests: 2,
                duration: 2.5,
                requests_per_second: 39.2,
                avg_response_time: 0.65,
                min_response_time: 0.2,
                max_response_time: 1.8,
                total_tokens: 9600,
                tokens_per_second: 3840,
                parallel: 3,
                model: 'DeepSeek-R1-Distill-Qwen-7B',
                dataset: 'openqa'
            },
            percentiles: {
                p50: 0.6,
                p75: 0.8,
                p90: 1.1,
                p95: 1.4,
                p99: 1.7
            }
        };
    }

    displayResults() {
        // 隐藏加载界面，显示结果
        document.getElementById('loadingSection').style.display = 'none';
        document.getElementById('resultsSection').style.display = 'block';

        // 填充测试配置信息
        this.populateTestInfo();
        
        // 填充核心指标
        this.populateMetrics();
        
        // 创建图表
        this.createCharts();
        
        // 计算性能评级
        this.calculatePerformanceGrades();
    }

    populateTestInfo() {
        const config = this.resultsData.testConfig;
        document.getElementById('testModel').textContent = config.model || '-';
        document.getElementById('testApiUrl').textContent = config.apiUrl || '-';
        document.getElementById('testParallel').textContent = config.parallel || '-';
        document.getElementById('testDataset').textContent = config.dataset || '-';
        document.getElementById('testTime').textContent = config.testTime || '-';
        document.getElementById('testStatus').textContent = config.status === 'success' ? '成功' : '失败';
    }

    populateMetrics() {
        const metrics = this.resultsData.metrics;
        
        // 计算成功率
        const successRate = metrics.successful_requests / metrics.total_requests * 100;
        
        document.getElementById('totalRequests').textContent = metrics.total_requests || 0;
        document.getElementById('successRate').textContent = `${successRate.toFixed(1)}%`;
        document.getElementById('avgRps').textContent = (metrics.requests_per_second || 0).toFixed(1);
        document.getElementById('avgTps').textContent = (metrics.tokens_per_second || 0).toFixed(0);
        document.getElementById('totalTokens').textContent = metrics.total_tokens || 0;
        document.getElementById('avgResponseTime').textContent = `${((metrics.avg_response_time || 0) * 1000).toFixed(0)}ms`;
    }

    createCharts() {
        this.createResponseTimeChart();
        this.createPercentileChart();
        this.createPerformanceChart();
    }

    createResponseTimeChart() {
        const ctx = document.getElementById('responseTimeChart').getContext('2d');
        
        // 模拟响应时间分布数据
        const responseTimeData = this.generateResponseTimeDistribution();
        
        this.charts.responseTime = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: responseTimeData.labels,
                datasets: [{
                    label: '请求数量',
                    data: responseTimeData.values,
                    backgroundColor: 'rgba(0, 212, 255, 0.6)',
                    borderColor: 'rgba(0, 212, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#fff'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff'
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: '响应时间 (ms)',
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
                        title: {
                            display: true,
                            text: '请求数量',
                            color: '#fff'
                        },
                        ticks: {
                            color: '#fff'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                }
            }
        });
    }

    createPercentileChart() {
        const ctx = document.getElementById('percentileChart').getContext('2d');
        const percentiles = this.resultsData.percentiles;
        
        this.charts.percentile = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['P50', 'P75', 'P90', 'P95', 'P99'],
                datasets: [{
                    label: '响应时间 (s)',
                    data: [
                        percentiles.p50,
                        percentiles.p75,
                        percentiles.p90,
                        percentiles.p95,
                        percentiles.p99
                    ],
                    borderColor: '#00d4ff',
                    backgroundColor: 'rgba(0, 212, 255, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#00d4ff',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#fff'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ${context.parsed.y.toFixed(3)}s`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: '百分位数',
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
                        title: {
                            display: true,
                            text: '响应时间 (s)',
                            color: '#fff'
                        },
                        ticks: {
                            color: '#fff'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                }
            }
        });
    }

    createPerformanceChart() {
        const ctx = document.getElementById('performanceChart').getContext('2d');
        const metrics = this.resultsData.metrics;
        
        this.charts.performance = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['吞吐量', '响应时间', '成功率', '并发性能', '稳定性'],
                datasets: [{
                    label: '性能指标',
                    data: [
                        this.normalizeMetric(metrics.tokens_per_second, 5000, 100), // 吞吐量
                        this.normalizeMetric(1 / metrics.avg_response_time, 2, 100), // 响应时间（倒数）
                        (metrics.successful_requests / metrics.total_requests) * 100, // 成功率
                        this.normalizeMetric(metrics.parallel * metrics.requests_per_second, 150, 100), // 并发性能
                        this.normalizeMetric(100 - (metrics.failed_requests / metrics.total_requests * 100), 100, 100) // 稳定性
                    ],
                    backgroundColor: 'rgba(0, 212, 255, 0.2)',
                    borderColor: '#00d4ff',
                    borderWidth: 2,
                    pointBackgroundColor: '#00d4ff',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#fff'
                        }
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            color: '#fff',
                            backdropColor: 'transparent'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        angleLines: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        pointLabels: {
                            color: '#fff',
                            font: {
                                size: 12
                            }
                        }
                    }
                }
            }
        });
    }

    generateResponseTimeDistribution() {
        // 基于实际数据生成响应时间分布
        const metrics = this.resultsData.metrics;
        const minTime = metrics.min_response_time * 1000; // 转换为毫秒
        const maxTime = metrics.max_response_time * 1000;
        const avgTime = metrics.avg_response_time * 1000;
        
        const buckets = 10;
        const bucketSize = (maxTime - minTime) / buckets;
        const labels = [];
        const values = [];
        
        for (let i = 0; i < buckets; i++) {
            const start = minTime + i * bucketSize;
            const end = start + bucketSize;
            labels.push(`${start.toFixed(0)}-${end.toFixed(0)}`);
            
            // 生成正态分布样的数据，峰值在平均响应时间附近
            const bucketCenter = (start + end) / 2;
            const distance = Math.abs(bucketCenter - avgTime);
            const value = Math.max(1, Math.round(20 * Math.exp(-distance / (avgTime * 0.3))));
            values.push(value);
        }
        
        return { labels, values };
    }

    normalizeMetric(value, max, scale) {
        return Math.min(scale, (value / max) * scale);
    }

    calculatePerformanceGrades() {
        const metrics = this.resultsData.metrics;
        
        // 计算各项评级
        const tpsGrade = this.calculateGrade(metrics.tokens_per_second, [1000, 2000, 3000, 4000]);
        const latencyGrade = this.calculateGrade(1 / metrics.avg_response_time, [0.5, 1, 1.5, 2]);
        const successRate = metrics.successful_requests / metrics.total_requests;
        const stabilityGrade = this.calculateGrade(successRate, [0.9, 0.95, 0.98, 0.99]);
        
        // 更新页面显示
        document.getElementById('throughputGrade').textContent = tpsGrade;
        document.getElementById('latencyGrade').textContent = latencyGrade;
        document.getElementById('stabilityGrade').textContent = stabilityGrade;
        
        // 计算综合评分
        const gradePoints = { 'A+': 95, 'A': 85, 'B': 75, 'C': 65, 'D': 50 };
        const avgScore = (gradePoints[tpsGrade] + gradePoints[latencyGrade] + gradePoints[stabilityGrade]) / 3;
        document.getElementById('overallScore').textContent = Math.round(avgScore);
    }

    calculateGrade(value, thresholds) {
        if (value >= thresholds[3]) return 'A+';
        if (value >= thresholds[2]) return 'A';
        if (value >= thresholds[1]) return 'B';
        if (value >= thresholds[0]) return 'C';
        return 'D';
    }
}

// 全局函数
function goBack() {
    window.history.back();
}

function exportResults() {
    // 导出结果为JSON文件
    const results = JSON.stringify(window.benchmarkResults?.resultsData || {}, null, 2);
    const blob = new Blob([results], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `benchmark-results-${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    window.benchmarkResults = new BenchmarkResults();
});
