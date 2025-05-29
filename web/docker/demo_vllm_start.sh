#!/bin/bash

# vLLM 服务启动示例脚本

echo "==================================="
echo "vLLM 服务启动示例"
echo "==================================="
echo ""
echo "此脚本展示如何启动 vLLM 服务以配合 TPS 测试工具使用"
echo ""

# 检查是否安装了 vLLM
python3 -c "import vllm" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "警告: 未检测到 vLLM 安装"
    echo ""
    echo "请先安装 vLLM:"
    echo "pip install vllm"
    echo ""
    echo "或使用 Docker:"
    echo "docker run --runtime nvidia --gpus all \\"
    echo "    -v ~/.cache/huggingface:/root/.cache/huggingface \\"
    echo "    -p 8000:8000 \\"
    echo "    --ipc=host \\"
    echo "    vllm/vllm-openai:latest \\"
    echo "    --model Qwen/Qwen2.5-0.5B-Instruct \\"
    echo "    --host 0.0.0.0"
    echo ""
    exit 1
fi

echo "以下是启动 vLLM 服务的示例命令："
echo ""
echo "1. 基础启动（Qwen2.5-0.5B）:"
echo "   python -m vllm.entrypoints.openai.api_server \\"
echo "       --model Qwen/Qwen2.5-0.5B-Instruct \\"
echo "       --host 0.0.0.0 \\"
echo "       --port 8000"
echo ""
echo "2. 高性能配置:"
echo "   python -m vllm.entrypoints.openai.api_server \\"
echo "       --model Qwen/Qwen2.5-0.5B-Instruct \\"
echo "       --host 0.0.0.0 \\"
echo "       --port 8000 \\"
echo "       --max-model-len 2048 \\"
echo "       --gpu-memory-utilization 0.9 \\"
echo "       --enforce-eager"
echo ""
echo "3. 多GPU配置:"
echo "   python -m vllm.entrypoints.openai.api_server \\"
echo "       --model Qwen/Qwen2.5-7B-Instruct \\"
echo "       --host 0.0.0.0 \\"
echo "       --port 8000 \\"
echo "       --tensor-parallel-size 2"
echo ""
echo "4. 量化模型配置:"
echo "   python -m vllm.entrypoints.openai.api_server \\"
echo "       --model Qwen/Qwen2.5-7B-Instruct-AWQ \\"
echo "       --host 0.0.0.0 \\"
echo "       --port 8000 \\"
echo "       --quantization awq"
echo ""
echo "==================================="
echo ""
read -p "是否立即启动 vLLM 服务？(y/n): " start_now

if [ "$start_now" = "y" ] || [ "$start_now" = "Y" ]; then
    echo ""
    echo "启动 vLLM 服务 (Qwen2.5-0.5B-Instruct)..."
    echo "服务将在 http://localhost:8000 运行"
    echo ""
    python -m vllm.entrypoints.openai.api_server \
        --model Qwen/Qwen2.5-0.5B-Instruct \
        --host 0.0.0.0 \
        --port 8000
fi
