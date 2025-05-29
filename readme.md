# Web Performance Testing Tool

This project includes a web-based tool for testing the TPS (Tokens Per Second) performance of large language models.

## Web Tool Features

### 主要页面文件说明
- **tps-test.html**: 主测试页面，包含完整的TPS测试功能和可视化图表
- **tps-test.js**: 主测试页面的JavaScript逻辑实现
- **tps-prototype.html**: 原型测试页面，提供基础测试功能
- **tps-proxy-server.py**: 代理服务器脚本，用于处理API请求
- **index.html**: 项目入口页面

### TPS Test Page (tps-test.html)
- **Intuitive Interface**: Breathing animation test button with beautiful dark blue gradient background
- **Real-time Charts**: Uses Chart.js to plot TPS curves in real-time
- **Flexible Configuration**: Supports custom models, API URLs, API Keys and other parameters
- **Detailed Statistics**: Shows current TPS, average TPS, peak TPS and total generated tokens
- **Real-time Logging**: Displays detailed log information during testing
- **Configuration Saving**: Automatically saves user configurations to local storage
- **Multi-model Comparison**: Supports testing multiple models simultaneously
- **Result Export**: Allows exporting test results as CSV files

### Prototype Page (tps-prototype.html)
- **Basic Testing**: Provides simple TPS testing functionality
- **Minimalist Design**: Clean interface focused on core functionality
- **Quick Start**: Ideal for rapid testing without complex configuration
- **Debug Mode**: Includes additional debug information for troubleshooting

## How to Use

1. Start vLLM service:
```bash
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-0.5B-Instruct \
    --port 8000 \
    --host 0.0.0.0
```

2. Start the web server:
```bash
cd web
python -m http.server 8080
```

3. Access the test page at http://localhost:8080/tps-test.html

4. Configure parameters:
   - Model: Qwen/Qwen2.5-0.5B-Instruct
   - API URL: http://localhost:8000/v1
   - API Key: (if required)
   - Test duration: 30 seconds (adjustable)
   - Max tokens: 100 (adjustable)

5. Click "Start Test" button

For more detailed instructions and troubleshooting, see [web/README_TPS_TEST.md](web/README_TPS_TEST.md)
