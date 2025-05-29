#!/bin/bash
cd "$(dirname "$0")" || exit

# 设置基准测试参数
MODEL="qwen3:32b-fp16"
API_KEY="your_api_key_here"  # 替换为实际API密钥
PROMPT_COUNT=100
MAX_TOKENS=512
CONCURRENCY=5

# 运行基准测试
python openai_api_benchmark.py \
  --ollama \
  --model "$MODEL" \
  --api-key "$API_KEY" \
  --prompt-count "$PROMPT_COUNT" \
  --max-tokens "$MAX_TOKENS" \
  --concurrency "$CONCURRENCY"

# 输出结果保存到当前目录的results.csv
