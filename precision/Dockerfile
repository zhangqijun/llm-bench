# 使用官方Python基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /evalscope

# 复制当前目录内容到容器中
COPY . .

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设置默认命令
CMD ["python", "main.py"]
