# LLM 基准测试工具

用于评估大语言模型(LLM)性能的基准测试工具。

## 功能
- 精度测试 (位于/precision目录)
  - vLLM服务: 高性能LLM推理框架
  - Ollama服务: 本地LLM运行环境
- 速度测试 (位于/speed目录)

## 最新基准测试结果 (按IQ+EQ分数排序)

| 模型名称 | 日期 | IQ分数 | EQ分数 | 参数量 | 量化方式 | 架构 |
|------------|------|---------|---------|------------|-------------|-------------|
| claude-3.7-sonnet | 2025-04-24 15:06:49 | 0.825 | 0.95 | - | - | claude |
| deepseek-chat | 2025-04-24 14:23:40 | 0.85 | 0.8875 | 684B | - | deepseek |
| deepseek-r1-32b-qwen-distill-fp16 | 2025-04-27 21:49:41 | 0.85 | 0.8 | 32.8B | F16 | qwen2 |
| deepseek-r1-32b-qwen-distill-q8_0 | 2025-04-27 21:01:28 | 0.825 | 0.7375 | 32.8B | Q8_0 | qwen2 |
| qwq-latest | 2025-04-25 16:47:10 | 0.8 | 0.7375 | 32.8B | Q4_K_M | qwen2 |
| deepseek-r1-32b-qwen-distill-q4_K_M | 2025-04-27 23:07:59 | 0.75 | 0.725 | 32.8B | Q4_K_M | qwen2 |
| deepseek-r1-32b | 2025-04-25 09:53:02 | 0.75 | 0.725 | 32.8B | Q4_K_M | qwen2 |
| deepseek-r1-70b-llama-distill-q4_K_M | 2025-04-28 06:04:27 | 0.675 | 0.775 | 70.6B | Q4_K_M | llama |
| deepseek-r1-14b-qwen-distill-fp16 | 2025-04-27 19:57:39 | 0.7 | 0.6375 | 14.8B | F16 | qwen2 |
| deepseek-r1-14b-qwen-distill-q8_0 | 2025-04-27 19:30:21 | 0.7 | 0.6375 | 14.8B | Q8_0 | qwen2 |

(显示前10条结果，完整结果见precision/model_scores.csv)

## 目录结构
- /precision: 包含模型评估和评分脚本
- /speed: 性能基准测试工具

## 快速开始
1. 克隆仓库
2. 从precision或speed目录运行所需的评估脚本
