#!/bin/bash

# 创建基础目录
mkdir -p /media/zqj/sda3/deepseek/

# 克隆各模型仓库
git clone https://modelscope.cn/models/tclf90/deepseek-r1-distill-qwen-32b-gptq-int4 /media/zqj/sda3/deepseek/DeepSeek-R1-Distill-Qwen-32B-GPTQ-Int4
git clone https://modelscope.cn/models/tclf90/deepseek-r1-distill-qwen-32b-gptq-int8 /media/zqj/sda3/deepseek/DeepSeek-R1-Distill-Qwen-32B-GPTQ-Int8
git clone https://modelscope.cn/models/tclf90/deepseek-r1-distill-qwen-7b-gptq-int4 /media/zqj/sda3/deepseek/DeepSeek-R1-Distill-Qwen-7B-GPTQ-Int4
git clone https://modelscope.cn/models/tclf90/deepseek-r1-distill-qwen-14b-gptq-int4 /media/zqj/sda3/deepseek/DeepSeek-R1-Distill-Qwen-14B-GPTQ-Int4
git clone https://modelscope.cn/models/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B /media/zqj/sda3/deepseek/DeepSeek-R1-Distill-Qwen-7B
git clone https://modelscope.cn/models/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B /media/zqj/sda3/deepseek/DeepSeek-R1-Distill-Qwen-32B
git clone https://modelscope.cn/models/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B /media/zqj/sda3/deepseek/DeepSeek-R1-Distill-Qwen-1.5B
git clone https://modelscope.cn/models/deepseek-ai/DeepSeek-R1-Distill-Qwen-14B /media/zqj/sda3/deepseek/DeepSeek-R1-Distill-Qwen-14B

echo "所有DeepSeek模型克隆命令已生成，请手动执行此脚本"
