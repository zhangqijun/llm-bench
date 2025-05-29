# from evalscope.perf.main import run_perf_benchmark
import subprocess


def run_eval(model_name: str, port: int):
    """执行评测"""

    cmd = [
        'evalscope', 'perf',
        '--model', model_name,
        '--api', 'local',
        '--dataset', 'speed_benchmark'
    ]
    subprocess.run(cmd)

    
if __name__ == "__main__":
    run_eval("Qwen/Qwen2.5-0.5B-Instruct",11434)