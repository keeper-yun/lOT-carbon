
import io
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import matplotlib.dates as dates
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from flask import Flask, send_file

def generate_plot(i):
    # 读取数据
    data_df = pd.read_csv(
        r"D:\Project-forecast\carbon\testdata\air-quality-data.csv",
        index_col="Date",
        parse_dates=['Date']  # 解析时间
    )

    # 设定合理的数值范围
    if i == 1:
        filtered_data = data_df[(data_df['NO2(GT)'] > 200) & (data_df['NO2(GT)'] < 650)]
    elif i == 2:
        filtered_data = data_df[(data_df['PT08.S1(CO)'] > 750) & (data_df['PT08.S1(CO)'] < 1400)]
    elif i ==3:
        filtered_data = data_df[(data_df['PT08.S5(O3)'] > 750) & (data_df['PT08.S5(O3)'] < 1400)]
    elif i ==4:
        filtered_data = data_df[(data_df['PT08.S4(NO2)'] > 1250) & (data_df['PT08.S4(NO2)'] < 2000)]
    else:
        return False

    # 确保索引去重
    filtered_data = filtered_data[~filtered_data.index.duplicated(keep='first')]

    # 确保时间索引只保留日期（去掉具体时间）
    filtered_data.index = filtered_data.index.normalize()

    # 设置日期频率，并填充缺失值
    filtered_data = filtered_data.asfreq('D').interpolate()

    # 按 80% 训练集，20% 测试集 划分
    train_size = int(len(filtered_data) * 0.8)

    if i == 1:
        train = filtered_data.iloc[:train_size]['NO2(GT)']
        test = filtered_data.iloc[train_size:]['NO2(GT)']
    elif i == 2:
        train = filtered_data.iloc[:train_size]['PT08.S1(CO)']
        test = filtered_data.iloc[train_size:]['PT08.S1(CO)']
    elif i ==3:
        train = filtered_data.iloc[:train_size]['PT08.S5(O3)']
        test = filtered_data.iloc[train_size:]['PT08.S5(O3)']
    elif i ==4:
        train = filtered_data.iloc[:train_size]['PT08.S4(NO2)']
        test = filtered_data.iloc[train_size:]['PT08.S4(NO2)']
    else:
        return False


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
    train_plot = train.iloc[int(len(train) * 0.8):]
    plt.plot(train_plot.index, train_plot, label='Train')
    plt.plot(test.index, test, label='Test Data', color='orange')
    plt.plot(predict.index, predict, label='Predicted Data', linestyle='--', color='green')

    plt.legend()
    plt.xticks(rotation=45)
    plt.title("ARIMA")

    # 设置 X 轴日期格式
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()

    # plt.show()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')  # 保存图像到内存
    plt.close()  # 关闭图表，释放内存
    buf.seek(0)
    return buf


# Flask 应用
app = Flask(__name__)
@app.route('/predict/<int:i>', methods=['GET'])
def plot(i):
    try:
        buf = generate_plot(i)
        return send_file(buf, mimetype='image/png')
    except FileNotFoundError:
        return f"Factory data not found!", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

import matplotlib
matplotlib.use('Agg')

# 直接运行
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)



# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.dates as dates
# import statsmodels.api as sm
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
#
# def generate_plot():
#     # 读取数据
#     data_df = pd.read_csv(
#         r"D:\Project-forecast\carbon\testdata\air_quality_feature.csv",
#         index_col="timestamp",
#         parse_dates=['timestamp']  # 解析时间
#     )
#     print(data_df.columns)
#
#     # 确保索引列是日期时间类型，强制转换无效日期为 NaT
#     data_df.index = pd.to_datetime(data_df.index, errors='coerce')
#
#     # 删除无效的日期行
#     data_df = data_df.dropna(subset=['timestamp'])
#
#     # 设定合理的数值范围
#     filtered_data = data_df[(data_df['pressure'] > 800) & (data_df['pressure'] < 1100)]
#
#     # 确保索引去重
#     filtered_data = filtered_data[~filtered_data.index.duplicated(keep='first')]
#
#     # 现在可以安全使用 normalize()
#     filtered_data.index = filtered_data.index.normalize()
#
#     # 设置日期频率，并填充缺失值
#     filtered_data = filtered_data.asfreq('D').interpolate()
#
#     # 按 80% 训练集，20% 测试集 划分
#     train_size = int(len(filtered_data) * 0.8)
#     train = filtered_data.iloc[:train_size]['pressure']
#     test = filtered_data.iloc[train_size:]['pressure']
#
#     # 设定 ARIMA 参数
#     p, d, q = 1, 1, 0
#     history = list(train.values)
#     forecast = []
#
#     for t in range(len(test.values)):
#         model = sm.tsa.ARIMA(history, order=(p, d, q))
#         model_fit = model.fit()
#         output = model_fit.forecast()
#         yhat = output[0]
#         forecast.append(yhat)
#         obs = test.iloc[t]
#         history.append(obs)
#
#     # 预测结果
#     predict = pd.Series(forecast, index=test.index)
#
#     # 计算误差指标
#     mae = mean_absolute_error(test, predict)
#     rmse = mean_squared_error(test, predict, squared=False)
#     mape = (abs((test - predict) / test)).mean() * 100
#     r2 = r2_score(test, predict)
#
#     print("\n=== 预测模型评估指标 ===")
#     print(f"MAE  = {mae:.4f}")
#     print(f"RMSE = {rmse:.4f}")
#     print(f"MAPE = {mape:.2f}%")
#     print(f"R²   = {r2:.4f}")
#
#     # 绘图
#     plt.figure(figsize=(12, 6))
#     plt.plot(train.index, train, label='Train')
#     plt.plot(test.index, test, label='Test', color='orange')
#     plt.plot(predict.index, predict, label='Predict', linestyle='--', color='green')
#
#     plt.legend()
#     plt.xticks(rotation=45)
#     plt.title("ARIMA")
#
#     # 设置 X 轴日期格式
#     plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
#     plt.gcf().autofmt_xdate()
#
#     plt.show()
#
# # 直接运行
# if __name__ == "__main__":
#     generate_plot()
