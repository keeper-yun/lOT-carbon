import pandas as pd
import matplotlib.pyplot as plt

# 解决中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False   # 解决负号显示问题

# 读取Excel文件
df = pd.read_excel(r'E:\碳然生“卫”-智能碳排放监测系统\设计文档\模型预测精度对比.xlsx')

# 设置图形大小
fig, ax = plt.subplots(figsize=(10, 6))

# 设置颜色
colors = ['skyblue', 'olive', 'gold', 'red']

# 绘制柱状图
df_plot = df.set_index('MODEL')[['MAE', 'RMSE', 'MAPE', 'R²']]
bars = df_plot.plot(kind='bar', ax=ax, color=colors)

# 设置标题和坐标轴标签，调整字体大小
ax.set_title('模型预测精度对比', fontsize=12)  # 标题稍微小一点
ax.set_ylabel('误差指标', fontsize=10)  # y轴标签字体变小
ax.set_xlabel('模型', fontsize=10)  # x轴标签字体变小

# 添加中文图例，并调整字体大小
ax.legend(['平均绝对误差 (MAE)', '均方根误差 (RMSE)', '平均绝对百分比误差 (MAPE)', '判定系数 (R*R)'], fontsize=9)

# 在柱状图上标出数值，并降低字体大小
for bars_container in bars.containers:  # 遍历所有 bar 组
    for bar in bars_container:  # 遍历单个 bar
        height = bar.get_height()
        if height != 0:  # 避免标注 0
            ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}',
                    ha='center', va='bottom', fontsize=8, rotation=0)

# 旋转X轴标签，调整字体大小
plt.xticks(rotation=45, fontsize=9)

# 显示图形
plt.show()
