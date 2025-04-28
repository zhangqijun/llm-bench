"""EvalScope iQuiz评测示例脚本

演示如何使用EvalScope API测试iquiz数据集
支持从命令行参数接收模型名称和端口
"""
import argparse
from evalscope.run import run_task
from evalscope.config import TaskConfig

def eval_iquiz_api(model: str, port: int):
    """API服务评测示例
    
    Args:
        model: 模型名称，如'ds-7b'
        port: 服务端口号
    """
    task_cfg = TaskConfig(
        model=model,
        api_url=f'http://127.0.0.1:{port}/v1/',
        api_key='',  # 本地服务不需要API key
        eval_type='service',
        datasets=['iquiz'],
        # debug=True
    )
    print(task_cfg)
    run_task(task_cfg=task_cfg)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, required=True,
                       help='模型名称，如ds-7b')
    parser.add_argument('--port', type=int, default=8801,
                       help='服务端口号，默认8801')
    
    args = parser.parse_args()
    print(f"\n开始评测模型: {args.model}")
    eval_iquiz_api(args.model, args.port)
