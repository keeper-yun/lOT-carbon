

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller as ADF

# 读取数据
data_df = pd.read_csv(
    r"D:\Project-forecast\carbon\v2.0\factory1.csv",
    index_col="timestamp",
    parse_dates=['timestamp']  # 将 'timestamp' 转为 DatetimeIndex
)

# 确保索引单调递增并设置频率
data_df = data_df.sort_index()
data_df.index.freq = pd.infer_freq(data_df.index)  # 自动推断频率

# 差分处理
data_df['diff_1'] = data_df['co2_Output'].diff(1)
data_df['diff_2'] = data_df['diff_1'].diff(1)

# 检查数据范围
print("数据时间范围：", data_df.index.min(), "至", data_df.index.max())

# 数据切片
try:
    sub = data_df.loc['2025-01-03 18:53:01':'2025-01-04 17:53:01']
    if sub.empty:
        raise ValueError("切片范围内没有数据，请检查时间范围！")
except KeyError as e:
    print("时间切片失败：", e)
    raise

# 提取训练集和测试集
train = sub.loc['2025-01-03 18:53:01':'2025-01-04 15:53:01']['co2_Output']
test = sub.loc['2025-01-04 16:53:01':'2025-01-04 17:53:01']['co2_Output']

# 绘制训练集时间序列
plt.figure(figsize=(12, 6))
plt.plot(train, label="Training Data")
plt.xticks(rotation=45)
plt.legend()
plt.title("Training Data")
plt.show()

# 单位根检验（ADF检验）
timeseries_adf = ADF(train)
print('ADF 检验结果：', timeseries_adf)

# 一阶差分
train_dif1 = train.diff(1).dropna()

# 打印一阶差分后的单位根检验结果
print('一阶差分 ADF检验：', ADF(train_dif1))

# 绘制一阶差分后的图像
plt.figure(figsize=(12, 6))
train_dif1.plot(title="First-order Differenced Series")
plt.show()

# 绘制 ACF 和 PACF 图
fig, axes = plt.subplots(2, 1, figsize=(12, 8))
sm.graphics.tsa.plot_acf(train_dif1, lags=20, ax=axes[0])
sm.graphics.tsa.plot_pacf(train_dif1, lags=12, ax=axes[1])
axes[0].set_title("ACF")
axes[1].set_title("PACF")
plt.tight_layout()
plt.show()

# 参数选择：使用AIC和BIC选择最优的ARIMA(p,d,q)参数
train_results = sm.tsa.arma_order_select_ic(train, ic=['aic', 'bic'], trend='n', max_ar=6, max_ma=6)
print('AIC 最优参数：', train_results.aic_min_order)
print('BIC 最优参数：', train_results.bic_min_order)

# 根据AIC或BIC的最优参数选择
p, d, q = 1,1,0

# 拟合ARIMA模型
model = sm.tsa.ARIMA(train, order=(p, d, q))
results = model.fit()

# 获取残差并绘图
resid = results.resid
fig, ax = plt.subplots(figsize=(12, 5))
sm.graphics.tsa.plot_acf(resid, lags=20, ax=ax)
plt.title("Residuals ACF")
plt.show()


start_index = train.index[2]
end_index = train.index[-1]
predict_sunspots = results.predict(start_index, end=end_index)
print(predict_sunspots)

# 查看训练集的时间序列与数据(只包含训练集)
plt.figure(figsize=(12, 6))
plt.plot(train)
plt.xticks(rotation=45)  # 旋转45度
plt.plot(predict_sunspots,linestyle='--')
plt.show()


p = 1
d = 1
q = 0

history = list(train.values)
forecast = list()
for t in range(len(test.values)):
    model = sm.tsa.ARIMA(history, order=(p, d, q))
    model_fit = model.fit()
    output = model_fit.forecast()
    yhat = output[0]
    forecast.append(yhat)
    obs = test[t]
    history.append(obs)  # 这里实现了滚动预测，应该是ARIMA只能预测下一步而不能多步

predict = pd.Series(forecast, index=test.index)
# 绘制结果
plt.figure(figsize=(12, 6))
plt.plot(train.index, train, label='Train')
plt.plot(test.index, test, label='Test',color='orange')
plt.plot(predict.index, predict, label='Predict', linestyle='--', color='green')
# plt.plot(predict_sunspots, label='Fit')
plt.legend()
plt.xticks(rotation=45)
plt.show()

