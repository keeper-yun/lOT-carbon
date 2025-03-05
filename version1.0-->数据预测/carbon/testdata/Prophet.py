import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.dates as mdates

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

    # Prophet 要求数据列名为 'ds' 和 'y'，因此需要重命名
    prophet_data = filtered_data.reset_index()[['Date', 'PT08.S1(CO)']]
    prophet_data.columns = ['ds', 'y']

    # 按 80% 训练集，20% 测试集 划分
    train_size = int(len(prophet_data) * 0.8)
    train = prophet_data.iloc[:train_size]
    test = prophet_data.iloc[train_size:]

    # 创建 Prophet 模型
    model = Prophet(daily_seasonality=True)
    model.fit(train)

    # 生成未来日期框架，用于预测
    future = model.make_future_dataframe(periods=len(test))  # 注意，只需要传递 periods 参数
    forecast = model.predict(future)

    # 预测值
    predicted_values = forecast[['ds', 'yhat']].iloc[train_size:]

    # 计算误差指标
    mae = mean_absolute_error(test['y'], predicted_values['yhat'])
    rmse = mean_squared_error(test['y'], predicted_values['yhat'], squared=False)
    mape = (abs((test['y'] - predicted_values['yhat']) / test['y'])).mean() * 100
    r2 = r2_score(test['y'], predicted_values['yhat'])

    print("\n=== 预测模型评估指标 ===")
    print(f"MAE  = {mae:.4f}")
    print(f"RMSE = {rmse:.4f}")
    print(f"MAPE = {mape:.2f}%")
    print(f"R²   = {r2:.4f}")

    # 绘图
    plt.figure(figsize=(12, 6))
    plt.plot(train['ds'], train['y'], label='Train')
    plt.plot(test['ds'], test['y'], label='Test', color='orange')
    plt.plot(predicted_values['ds'], predicted_values['yhat'], label='Predict', linestyle='--', color='green')

    plt.legend()
    plt.xticks(rotation=45)
    plt.title("Prophet")

    # 设置 X 轴日期格式
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()

    plt.show()

# 直接运行
if __name__ == "__main__":
    generate_plot()
