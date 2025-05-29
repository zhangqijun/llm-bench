# 大模型 TPS 性能测试工具

这是一个用于测试大语言模型 TPS（Tokens Per Second）性能的网页应用，类似于 speedtest.cn 的界面设计。

## 功能特点

- 🎯 **直观的界面**：呼吸动画的圆形测试按钮，美观的深蓝色渐变背景
- 📊 **实时图表**：使用 Chart.js 实时绘制 TPS 曲线
- 🔧 **灵活配置**：支持自定义模型、API URL、API Key 等参数
- 📈 **详细统计**：显示当前 TPS、平均 TPS、最高 TPS 和总生成 Tokens
- 📝 **实时日志**：显示测试过程中的详细日志信息
- 💾 **配置保存**：自动保存用户配置到本地存储

## 文件说明

- `tps-test.html` - 主页面文件
- `tps-test.js` - JavaScript 逻辑文件
- `tps-proxy-server.py` - Python 代理服务器（用于解决 CORS 问题）

## 使用方法

### 方法一：直接使用（如果 vLLM 服务支持 CORS）

1. 启动 vLLM 服务：
```bash
# 示例：使用 vLLM 启动 Qwen2.5-0.5B-Instruct 模型
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-0.5B-Instruct \
    --port 8000 \
    --host 0.0.0.0
```

2. 打开测试页面：
```bash
# 在 web 目录下
python -m http.server 8080
# 或使用其他静态文件服务器
```

3. 访问 http://localhost:8080/tps-test.html

4. 配置参数：
   - 选择模型：Qwen/Qwen2.5-0.5B-Instruct
   - API URL：http://localhost:8000/v1
   - API Key：（如果需要）
   - 测试时长：30秒（可调整）
   - 最大生成Token数：100（可调整）

5. 点击"开始测试"按钮

### 方法二：使用代理服务器（推荐，解决 CORS 问题）

1. 安装依赖：
```bash
pip install flask flask-cors requests
```

2. 启动 vLLM 服务（同上）

3. 启动代理服务器：
```bash
cd web
python tps-proxy-server.py
```

4. 打开测试页面（同上）

5. 配置参数：
   - API URL：http://localhost:5000/v1 （注意端口是 5000）
   - 其他参数同上

## 测试原理

1. **并发请求**：默认使用 3 个并发请求来测试模型的吞吐能力
2. **TPS 计算**：每秒统计生成的 token 数量，计算实时 TPS
3. **图表更新**：每秒更新一次图表，显示最近 60 秒的数据
4. **统计信息**：实时计算并显示各项统计指标

## 配置说明

### 模型选择
- 预设了 Qwen2.5 系列模型（0.5B、1.5B、3B、7B）
- 支持自定义模型名称

### API 配置
- **API URL**：vLLM 服务的 OpenAI 兼容接口地址
- **API Key**：如果服务需要认证，填写 API Key

### 测试参数
- **测试时长**：10-300 秒可调
- **最大生成 Token 数**：每个请求最多生成的 token 数量

## 注意事项

1. **CORS 问题**：如果直接访问 vLLM 服务遇到 CORS 错误，请使用代理服务器
2. **性能影响**：并发请求数和最大 token 数会影响测试结果
3. **网络延迟**：本地测试时网络延迟较小，远程测试需考虑网络因素

## 故障排除

### 常见问题

1. **连接失败**
   - 检查 vLLM 服务是否正常运行
   - 检查 API URL 是否正确
   - 检查防火墙设置

2. **CORS 错误**
   - 使用代理服务器方法
   - 或配置 vLLM 服务允许跨域请求

3. **测试结果异常**
   - 检查模型是否正确加载
   - 调整并发请求数和 token 数量
   - 查看日志了解详细错误信息

## 扩展功能

可以根据需要扩展以下功能：

1. **更多测试模式**：如延迟测试、稳定性测试等
2. **结果导出**：支持导出测试数据为 CSV 或 JSON
3. **批量测试**：支持多个模型的对比测试
4. **高级配置**：如温度、top_p 等参数调整

## 技术栈

- **前端**：原生 HTML/CSS/JavaScript + Chart.js
- **后端**：Python Flask（代理服务器）
- **协议**：OpenAI API 兼容协议
- **目标服务**：vLLM 推理服务

## 许可证

MIT License
