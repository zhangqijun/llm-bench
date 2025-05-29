import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_csv('precision/model_scores.csv')

# 定义提取模型结构的函数
def extract_model_structure(model_name):
    model_name_lower = str(model_name).lower()  # 确保是字符串并转为小写
    
    # 优先匹配更具体的模型系列
    if 'gpt' in model_name_lower:
        return 'GPT'
    elif 'deepseek' in model_name_lower:
        return 'DeepSeek'
    elif 'qwen3' in model_name_lower:
        return 'Qwen3'
    elif 'qwen2.5' in model_name_lower:
        return 'Qwen2.5'
    elif 'claude' in model_name_lower:
        return 'Claude'
    elif 'gemini' in model_name_lower:
        return 'Gemini'
    elif 'llama' in model_name_lower:
        return 'Llama'
    elif 'glm' in model_name_lower:
        return 'GLM'
    elif 'qvq' in model_name_lower or 'qwq' in model_name_lower:
        return 'QVQ/QWQ'
    elif 'qwen' in model_name_lower:  # 通用qwen匹配放在最后
        return 'Qwen'
    
    # 如果没有匹配到，返回模型名称的主要部分
    parts = model_name_lower.replace('/', '-').split('-')
    return parts[0].upper() if parts else 'Other'

# 应用函数提取模型结构
df['model_structure'] = df['model_name'].apply(extract_model_structure)

# 为不同模型结构分配颜色
model_structures = df['model_structure'].unique()
colors = plt.cm.tab20(np.linspace(0, 1, len(model_structures))) # 使用tab20颜色映射表，更适合分类
color_map = dict(zip(model_structures, colors))

# 创建图表
plt.figure(figsize=(16, 12))
ax = plt.gca()

# 绘制散点图
for model_structure_val, color in color_map.items():
    subset = df[df['model_structure'] == model_structure_val]
    if not subset.empty: # 确保子集不为空
        plt.scatter(subset['EQ_score'], subset['IQ_score'], 
                    color=color, label=model_structure_val, s=100)

# 添加标注并解决重叠问题
from adjustText import adjust_text
texts = []
for i, row in df.iterrows():
    texts.append(ax.text(row['EQ_score'], row['IQ_score'], 
                      row['model_name'], fontsize=7,
                      bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1)))
adjust_text(texts, 
           arrowprops=dict(arrowstyle='->', color='gray', lw=0.5),
           expand_points=(1.2, 1.2), 
           expand_text=(1.1, 1.1),
           force_text=(0.5, 0.5))

# 设置图表属性
plt.title('AI模型EQ-IQ得分分布', fontsize=16)
plt.xlabel('EQ Score', fontsize=14)
plt.ylabel('IQ Score', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# 调整布局并保存
plt.tight_layout()
plt.savefig('model_scores_plot.png', dpi=300, bbox_inches='tight')
print("图表已保存为 model_scores_plot.png")
