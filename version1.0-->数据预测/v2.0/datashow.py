#
#
# import  pandas as pd
# import matplotlib.pyplot as plt
# from altair.examples.select_detail import timeseries
#
# data_df = pd.read_csv(r"D:\Project-forecast\carbon\v2.0\factory1.csv",index_col="timestamp",parse_dates=['timestamp'])
# # data_df.index = data_df.index.strftime('%H')
#
#
# data_df['diff_1'] = data_df['co2_Output'].diff(1)
# data_df['diff_2'] = data_df['diff_1'].diff(1)
#
# # fig = plt.figure(figsize=(12,10))
# #
# # # 原数据
# # ax1 = fig.add_subplot(311)
# # ax1.plot(data_df['co2_Output'])
# # # 1阶差分
# # ax2 = fig.add_subplot(312)
# # ax2.plot(data_df['diff_1'])
# # # 2阶差分
# # ax3 = fig.add_subplot(313)
# # ax3.plot(data_df['diff_2'])
# #
# # plt.show()
#
#
# import statsmodels.api as sm
# from statsmodels.tsa.seasonal import seasonal_decompose
# from statsmodels.tsa.stattools import adfuller as ADF
#
#
# data_df.index = pd.to_datetime(data_df.index)
# sub = data_df.loc['2025-01-03 18:53:01':'2025-01-04 17:53:01']
#
# sub.head()
#
# train = sub.loc['2025-01-03 18:53:01':'2025-01-04 15:53:01']
# test = sub.loc['2025-01-04 16:53:01':'2025-01-04 17:53:01']
#
#
# fig = plt.figure(figsize=(12,7))
#
# ax1 = fig.add_subplot(211)
# fig = sm.graphics.tsa.plot_acf(train,lags = 20,ax=ax1)
# ax1.xaxis.set_ticks_position('bottom')
#
# ax2 = fig.add_subplot(212)
# fig = sm.graphics.tsa.plot_pacf(test,lags = 14,ax=ax2)
# ax2.xaxis.set_ticks_position('bottom')
#
# plt.show()




# import pandas as pd
# import matplotlib.pyplot as plt
# import statsmodels.api as sm
#
# # 读取数据
# data_df = pd.read_csv(
#     r"D:\Project-forecast\carbon\v2.0\factory1.csv",
#     index_col="timestamp",
#     parse_dates=['timestamp']  # 将 'timestamp' 转为 DatetimeIndex
# )
#
# # 确保索引单调递增
# data_df = data_df.sort_index()
#
# # 差分处理
# data_df['diff_1'] = data_df['co2_Output'].diff(1)
# data_df['diff_2'] = data_df['diff_1'].diff(1)
#
# # 检查数据范围
# print("数据时间范围：", data_df.index.min(), "至", data_df.index.max())
#
# # 数据切片
# try:
#     sub = data_df.loc['2025-01-03 18:53:01':'2025-01-04 17:53:01']
#     if sub.empty:
#         raise ValueError("切片范围内没有数据，请检查时间范围！")
# except KeyError as e:
#     print("时间切片失败：", e)
#     raise
#
# # 划分训练集和测试集
# train = sub.loc['2025-01-03 18:53:01':'2025-01-04 15:53:01']['co2_Output']
# test = sub.loc['2025-01-04 16:53:01':'2025-01-04 17:53:01']['co2_Output']
#
# # 绘制 ACF 和 PACF 图
# fig = plt.figure(figsize=(12, 7))
#
# # 自相关函数 (ACF)
# ax1 = fig.add_subplot(211)
# sm.graphics.tsa.plot_acf(train.dropna(), lags=20, ax=ax1)
# ax1.set_title("Autocorrelation Function (ACF)")
# ax1.xaxis.set_ticks_position('bottom')
#
# # 偏自相关函数 (PACF)
# ax2 = fig.add_subplot(212)
# sm.graphics.tsa.plot_pacf(train.dropna(), lags=14, ax=ax2)
# ax2.set_title("Partial Autocorrelation Function (PACF)")
# ax2.xaxis.set_ticks_position('bottom')
#
# plt.tight_layout()
# plt.show()




import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import itertools

# 读取数据
data_df = pd.read_csv(
    r"D:\Project-forecast\carbon\v2.0\factory1.csv",
    index_col="timestamp",
    parse_dates=['timestamp']  # 将 'timestamp' 转为 DatetimeIndex
)

# 确保索引单调递增
data_df = data_df.sort_index()

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

# 划分训练集和测试集
train = sub.loc['2025-01-03 18:53:01':'2025-01-04 15:53:01']['co2_Output']
test = sub.loc['2025-01-04 16:53:01':'2025-01-04 17:53:01']['co2_Output']

# 绘制 ACF 和 PACF 图
fig = plt.figure(figsize=(12, 7))

# 自相关函数 (ACF)
ax1 = fig.add_subplot(211)
sm.graphics.tsa.plot_acf(train.dropna(), lags=20, ax=ax1)
ax1.set_title("Autocorrelation Function (ACF)")
ax1.xaxis.set_ticks_position('bottom')

# 偏自相关函数 (PACF)
ax2 = fig.add_subplot(212)
sm.graphics.tsa.plot_pacf(train.dropna(), lags=14, ax=ax2)
ax2.set_title("Partial Autocorrelation Function (PACF)")
ax2.xaxis.set_ticks_position('bottom')

plt.tight_layout()
plt.show()

# 参数搜索 - BIC 准则
p_min = 0
d_min = 0
q_min = 0
p_max = 5
d_max = 0
q_max = 2

# 初始化存储 BIC 的 DataFrame
results_bic = pd.DataFrame(index=['AR{}'.format(i) for i in range(p_min, p_max+1)],
                           columns=['MA{}'.format(i) for i in range(q_min, q_max+1)])

for p, d, q in itertools.product(range(p_min, p_max+1),
                                 range(d_min, d_max+1),
                                 range(q_min, q_max+1)):
    if p == 0 and d == 0 and q == 0:
        results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = np.nan
        continue
    try:
        model = sm.tsa.ARIMA(train, order=(p, d, q))
        results = model.fit()
        results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = results.bic
    except:
        continue

# BIC 热力图
results_bic = results_bic[results_bic.columns].astype(float)
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(
    results_bic,
    mask=results_bic.isnull(),
    annot=True,
    fmt='.2f',
    cmap="Purples",
    ax=ax
)
ax.set_title('BIC Scores')
plt.show()

# 获取最优参数组合
min_bic = results_bic.min().min()
optimal_params = results_bic.stack().idxmin()
p, q = int(optimal_params[0][2:]), int(optimal_params[1][2:])
print(f"最优参数：p={p}, d=0, q={q}, BIC={min_bic:.2f}")

# 使用最优参数拟合模型
optimal_model = sm.tsa.ARIMA(train, order=(p, 0, q))
optimal_results = optimal_model.fit()
print(optimal_results.summary())

# 拟合结果
predict_train = optimal_results.predict(dynamic=False)
print("拟合结果：", predict_train)

# 绘制训练集拟合结果
plt.figure(figsize=(12, 6))
plt.plot(train, label="Training Data")
plt.plot(predict_train, label="Fitted Data", linestyle="--")
plt.xticks(rotation=45)
plt.legend()
plt.title("Training Data vs Fitted Data")
plt.show()

# 预测测试集
forecast_steps = 5
forecast = optimal_results.forecast(steps=forecast_steps)

# 如果预测时间超过测试集范围，则生成新索引
forecast_start_time = test.index[-1]  # 测试集的最后一个时间点

forecast_index = pd.date_range(
    start=forecast_start_time,
    periods=forecast_steps + 1,
    freq='H'  # 手动指定为小时
)[1:]

forecast.index = forecast_index

# forecast.index = test.index

# 预测结果与实际值对比
plt.figure(figsize=(12, 6))
plt.plot(train.index, train, label='Train')
plt.plot(test.index, test, label='Test', color='orange')
plt.plot(forecast.index, forecast, label='Forecast', linestyle='--', color='green')
plt.legend()
plt.xticks(rotation=45)
plt.title("Forecast vs Test Data")
plt.show()
