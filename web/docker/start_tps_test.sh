#!/bin/bash

# TPS测试工具启动脚本

echo "==================================="
echo "大模型 TPS 性能测试工具"
echo "==================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装 Python3"
    exit 1
fi

# 检查依赖
echo "检查依赖..."
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "安装 Flask 依赖..."
    pip3 install flask flask-cors requests
fi

# 启动选项
echo ""
echo "请选择启动模式："
echo "1. 启动代理服务器 + 网页服务器（推荐）"
echo "2. 仅启动网页服务器"
echo "3. 仅启动代理服务器"
echo ""
read -p "请输入选项 (1-3): " choice

case $choice in
    1)
        echo ""
        echo "启动代理服务器..."
        python3 tps-proxy-server.py &
        PROXY_PID=$!
        echo "代理服务器 PID: $PROXY_PID"
        
        sleep 2
        
        echo ""
        echo "启动网页服务器..."
        python3 -m http.server 8080 &
        WEB_PID=$!
        echo "网页服务器 PID: $WEB_PID"
        
        echo ""
        echo "==================================="
        echo "服务已启动！"
        echo ""
        echo "测试页面地址: http://localhost:8080/tps-test.html"
        echo "代理服务器地址: http://localhost:5000"
        echo ""
        echo "使用说明："
        echo "1. 确保 vLLM 服务已在 http://localhost:8000 运行"
        echo "2. 在测试页面中设置 API URL 为: http://localhost:5000/v1"
        echo "3. 选择模型并点击'开始测试'"
        echo ""
        echo "按 Ctrl+C 停止所有服务"
        echo "==================================="
        
        # 等待用户中断
        trap "kill $PROXY_PID $WEB_PID 2>/dev/null; echo ''; echo '服务已停止'; exit" INT
        wait
        ;;
        
    2)
        echo ""
        echo "启动网页服务器..."
        python3 -m http.server 8080 &
        WEB_PID=$!
        
        echo ""
        echo "==================================="
        echo "网页服务器已启动！"
        echo ""
        echo "测试页面地址: http://localhost:8080/tps-test.html"
        echo ""
        echo "注意：如遇到 CORS 错误，请使用选项 1 启动代理服务器"
        echo ""
        echo "按 Ctrl+C 停止服务"
        echo "==================================="
        
        trap "kill $WEB_PID 2>/dev/null; echo ''; echo '服务已停止'; exit" INT
        wait
        ;;
        
    3)
        echo ""
        echo "启动代理服务器..."
        python3 tps-proxy-server.py
        ;;
        
    *)
        echo "无效选项"
        exit 1
        ;;
esac
