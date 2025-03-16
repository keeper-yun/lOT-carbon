
from flask import Flask, send_file
import io
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import statsmodels.api as sm

def generate_plot(i):
    # 读取数据
    data_df = pd.read_csv(
        r"D:\Project-forecast\carbon\testdata\air-data.csv",
        index_col="Date",
        parse_dates=['Date']  # 解析时间
    )

    # 根据 i 的值选择不同的列进行预测
    if i == 1:
        filtered_data = data_df[(data_df['NO2(GT)'] > 200) & (data_df['NO2(GT)'] < 650)]
    elif i == 2:
        filtered_data = data_df[(data_df['PT08.S1(CO)'] > 750) & (data_df['PT08.S1(CO)'] < 1400)]
    elif i == 3:
        filtered_data = data_df[(data_df['PT08.S5(O3)'] > 750) & (data_df['PT08.S5(O3)'] < 1400)]
    elif i == 4:
        filtered_data = data_df[(data_df['PT08.S4(NO2)'] > 1250) & (data_df['PT08.S4(NO2)'] < 2000)]
    else:
        return False

    # 确保索引去重并进行数据预处理
    filtered_data = filtered_data[~filtered_data.index.duplicated(keep='first')]
    filtered_data = filtered_data.infer_objects()
    filtered_data = filtered_data.asfreq('h').interpolate()

    # 确保数据集非空
    if filtered_data.empty:
        return False

    # 数据划分
    steps = 48  # 预测48小时
    if i == 1:
        train_series = filtered_data.iloc[:-steps]['NO2(GT)']
        test_series = filtered_data.iloc[-steps:]['NO2(GT)']
    elif i == 2:
        train_series = filtered_data.iloc[:-steps]['PT08.S1(CO)']
        test_series = filtered_data.iloc[-steps:]['PT08.S1(CO)']
    elif i == 3:
        train_series = filtered_data.iloc[:-steps]['PT08.S5(O3)']
        test_series = filtered_data.iloc[-steps:]['PT08.S5(O3)']
    elif i == 4:
        train_series = filtered_data.iloc[:-steps]['PT08.S4(NO2)']
        test_series = filtered_data.iloc[-steps:]['PT08.S4(NO2)']
    else:
        return False

    # 设定 ARIMA 参数
    p, d, q = 1, 1, 0

    # 训练 ARIMA 模型
    model = sm.tsa.ARIMA(train_series, order=(p, d, q))
    model_fit = model.fit()

    # 预测未来 48 小时
    forecast = model_fit.forecast(steps=steps)

    # 生成未来 48 小时的时间索引
    future_dates = test_series.index

    # 创建预测数据表
    future_forecast = pd.Series(forecast, index=future_dates)

    # 绘图
    plt.figure(figsize=(12, 6))
    # plt.plot(train_series.index, train_series, label='Train', color='blue')
    plt.plot(test_series.index, test_series, label='Test', color='orange')
    plt.plot(future_forecast.index, future_forecast, label='Predict', linestyle='--', color='green')

    plt.legend()
    plt.xticks(rotation=45)
    plt.title("ARIMA")

    # 设置 X 轴单位为小时
    plt.gca().xaxis.set_major_locator(dates.HourLocator(interval=6))
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%m-%d %H:%M'))

    plt.grid(True)
    plt.gcf().autofmt_xdate()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf

# Flask 应用
app = Flask(__name__)

@app.route('/predict/<int:i>', methods=['GET'])
def plot(i):
    try:
        buf = generate_plot(i)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return f"Error: {str(e)}", 500

import matplotlib
matplotlib.use('Agg')

# 直接运行
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
