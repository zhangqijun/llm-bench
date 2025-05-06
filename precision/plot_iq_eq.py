import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_csv('model_scores.csv')

# 为不同api_url分配颜色
api_urls = df['api_url'].unique()
colors = plt.cm.tab20(np.linspace(0, 1, len(api_urls)))
color_map = dict(zip(api_urls, colors))

# 创建图表
plt.figure(figsize=(16, 12))
ax = plt.gca()

# 绘制散点图
for api_url, color in color_map.items():
    subset = df[df['api_url'] == api_url]
    plt.scatter(subset['EQ_score'], subset['IQ_score'], 
                color=color, label=api_url, s=100)

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
