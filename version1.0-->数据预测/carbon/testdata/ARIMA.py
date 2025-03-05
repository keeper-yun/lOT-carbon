import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import matplotlib.dates as mdates
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def generate_plot():
    # 读取数据
    data_df = pd.read_csv(
        r"D:\Project-forecast\carbon\testdata\air-quality-data.csv",
        index_col="Date",
        parse_dates=['Date']  # 解析时间
    )

    # 设定合理的数值范围
    filtered_data = data_df[(data_df['PT08.S1(CO)'] > 750) & (data_df['PT08.S1(CO)'] < 1800)]

    # 确保索引去重，防止 `asfreq('D')` 报错
    filtered_data = filtered_data[~filtered_data.index.duplicated(keep='first')]

    # 确保时间索引只保留日期（去掉具体时间）
    filtered_data.index = filtered_data.index.normalize()

    # 设置日期频率，并填充缺失值
    filtered_data = filtered_data.asfreq('D').interpolate()

    # 按 80% 训练集，20% 测试集 划分
    train_size = int(len(filtered_data) * 0.8)
    train = filtered_data.iloc[:train_size]['PT08.S1(CO)']
    test = filtered_data.iloc[train_size:]['PT08.S1(CO)']

    # 设定 ARIMA 参数
    p, d, q = 1, 1, 0
    history = list(train.values)
    forecast = []

    for t in range(len(test.values)):
        model = sm.tsa.ARIMA(history, order=(p, d, q))
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        forecast.append(yhat)
        obs = test.iloc[t]
        history.append(obs)

    # 预测结果
    predict = pd.Series(forecast, index=test.index)

    # 计算误差指标
    mae = mean_absolute_error(test, predict)
    rmse = mean_squared_error(test, predict, squared=False)
    mape = (abs((test - predict) / test)).mean() * 100
    r2 = r2_score(test, predict)

    print("\n=== 预测模型评估指标 ===")
    print(f"MAE  = {mae:.4f}")
    print(f"RMSE = {rmse:.4f}")
    print(f"MAPE = {mape:.2f}%")
    print(f"R²   = {r2:.4f}")

    # 绘图
    plt.figure(figsize=(12, 6))
    plt.plot(train.index, train, label='Train')
    plt.plot(test.index, test, label='Test', color='orange')
    plt.plot(predict.index, predict, label='Predict', linestyle='--', color='green')

    plt.legend()
    plt.xticks(rotation=45)
    plt.title("ARIMA")

    # 设置 X 轴日期格式
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()

    plt.show()

# 直接运行
if __name__ == "__main__":
    generate_plot()
