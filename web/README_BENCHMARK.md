# TPS 压测接口使用说明

## 概述

TPS代理服务器现在支持通过POST接口运行性能压测，该接口调用了perf模块的main函数来执行压测并返回结果摘要。

## 接口详情

### 端点
```
POST /v1/benchmark
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| api_url | string | 是 | 目标API的URL地址 |
| parallel | number | 是 | 并发请求数 |
| model | string | 是 | 模型名称 |
| min-tokens | number | 是 | 最小token数 |
| max-tokens | number | 是 | 最大token数 |
| datasets | string | 是 | 数据集名称 |
| api_key | string | 否 | API密钥（可选） |

### 请求示例

```bash
curl -X POST http://localhost:8080/v1/benchmark \
  -H "Content-Type: application/json" \
  -d '{
    "api_url": "http://localhost:8000/v1",
    "parallel": 3,
    "model": "test-model",
    "min-tokens": 50,
    "max-tokens": 100,
    "datasets": "openqa",
    "api_key": "your-api-key"
  }'
```

### 响应格式

成功响应：
```json
{
  "status": "success",
  "metrics": {
    "total_requests": 100,
    "successful_requests": 100,
    "failed_requests": 0,
    "duration": 2.0,
    "requests_per_second": 50.0,
    "avg_response_time": 0.5,
    "min_response_time": 0.2,
    "max_response_time": 1.0,
    "total_tokens": 10000,
    "tokens_per_second": 5000.0,
    "parallel": 3,
    "model": "test-model",
    "dataset": "openqa"
  },
  "percentiles": {
    "p50": 0.4,
    "p75": 0.6,
    "p90": 0.8,
    "p95": 0.9,
    "p99": 1.0
  }
}
```

错误响应：
```json
{
  "error": {
    "message": "错误描述",
    "type": "error_type"
  }
}
```

## 前端集成

在TPS测试页面中，原有的"开始测试"按钮现在直接连接到压测功能，点击后会：

1. 收集当前配置的参数
2. 调用 `/v1/benchmark` 接口
3. 压测完成后自动跳转到美观的结果页面

### 使用步骤

1. 访问 `http://localhost:8080/tps-test.html`
2. 配置API URL、模型、token数等参数
3. 点击"开始测试"按钮
4. 等待压测完成（约2-5秒）
5. 自动跳转到结果页面查看详细报告

### 结果页面特性

- **美观的UI设计**：渐变背景、毛玻璃效果、响应式布局
- **详细的测试信息**：显示所有测试配置参数
- **核心性能指标**：TPS、RPS、响应时间、成功率等关键指标
- **可视化图表**：
  - 响应时间分布柱状图
  - 响应时间百分位数折线图  
  - 性能指标雷达图
- **智能评级系统**：自动计算吞吐量、延迟、稳定性评级
- **结果导出**：支持导出JSON格式的详细结果
- **便捷导航**：返回测试页面或导出报告

## 技术实现

- 接口基于Flask框架实现
- 支持CORS跨域请求
- 集成了perf模块的压测功能
- 返回标准化的JSON格式结果
- 包含详细的性能指标和百分位数据

## 注意事项

1. 当前实现为演示版本，返回模拟的压测数据
2. 实际部署时需要确保perf模块的依赖正确安装
3. 压测过程中请确保目标API服务正常运行
4. 建议在测试环境中使用，避免对生产环境造成压力

## 错误处理

接口会处理以下错误情况：
- 缺少必需参数
- 模块导入失败
- 压测执行异常
- 网络连接问题

所有错误都会返回标准的错误响应格式，便于前端处理。
