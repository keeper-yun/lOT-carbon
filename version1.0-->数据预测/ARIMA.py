import io

# 网页呈现效果
# import io
# import pandas as pd
# import matplotlib.pyplot as plt
# import statsmodels.api as sm
# import matplotlib.dates as dates
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# from flask import Flask, send_file
#
# def generate_plot(i):
#     # 读取数据
#     data_df = pd.read_csv(
#         r"D:\Project-forecast\carbon\testdata\air-quality-data.csv",
#         index_col="Date",
#         parse_dates=['Date']  # 解析时间
#     )
#
#     # 设定合理的数值范围
#     if i == 1:
#         filtered_data = data_df[(data_df['NO2(GT)'] > 200) & (data_df['NO2(GT)'] < 650)]
#     elif i == 2:
#         filtered_data = data_df[(data_df['PT08.S1(CO)'] > 750) & (data_df['PT08.S1(CO)'] < 1400)]
#     elif i ==3:
#         filtered_data = data_df[(data_df['PT08.S5(O3)'] > 750) & (data_df['PT08.S5(O3)'] < 1400)]
#     elif i ==4:
#         filtered_data = data_df[(data_df['PT08.S4(NO2)'] > 1250) & (data_df['PT08.S4(NO2)'] < 2000)]
#     else:
#         return False
#
#     # 确保索引去重
#     filtered_data = filtered_data[~filtered_data.index.duplicated(keep='first')]
#
#     # 确保时间索引只保留日期（去掉具体时间）
#     filtered_data.index = filtered_data.index.normalize()
#
#     # 设置日期频率，并填充缺失值
#     filtered_data = filtered_data.asfreq('D').interpolate()
#
#     # 按 80% 训练集，20% 测试集 划分
#     train_size = int(len(filtered_data) * 0.8)
#
#     if i == 1:
#         train = filtered_data.iloc[:train_size]['NO2(GT)']
#         test = filtered_data.iloc[train_size:]['NO2(GT)']
#     elif i == 2:
#         train = filtered_data.iloc[:train_size]['PT08.S1(CO)']
#         test = filtered_data.iloc[train_size:]['PT08.S1(CO)']
#     elif i ==3:
#         train = filtered_data.iloc[:train_size]['PT08.S5(O3)']
#         test = filtered_data.iloc[train_size:]['PT08.S5(O3)']
#     elif i ==4:
#         train = filtered_data.iloc[:train_size]['PT08.S4(NO2)']
#         test = filtered_data.iloc[train_size:]['PT08.S4(NO2)']
#     else:
#         return False
#
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
#     train_plot = train.iloc[int(len(train) ):]
#     plt.plot(train_plot.index, train_plot, label='Train')
#     plt.plot(test.index, test, label='Test Data', color='orange')
#     plt.plot(predict.index, predict, label='Predicted Data', linestyle='--', color='green')
#
#     plt.legend()
#     plt.xticks(rotation=45)
#     plt.title("ARIMA")
#
#     # 设置 X 轴日期格式
#     plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
#     plt.gcf().autofmt_xdate()
#
#     # plt.show()
#     buf = io.BytesIO()
#     plt.savefig(buf, format='png')  # 保存图像到内存
#     plt.close()  # 关闭图表，释放内存
#     buf.seek(0)
#     return buf
#
#
# # Flask 应用
# app = Flask(__name__)
# @app.route('/predict/<int:i>', methods=['GET'])
# def plot(i):
#     try:
#         buf = generate_plot(i)
#         return send_file(buf, mimetype='image/png')
#     except FileNotFoundError:
#         return f"Factory data not found!", 404
#     except Exception as e:
#         return f"Error: {str(e)}", 500
#
# import matplotlib
# matplotlib.use('Agg')
#
# # 直接运行
# if __name__ == "__main__":
#     app.run(debug=True, use_reloader=False)





# 几个月预测
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import statsmodels.api as sm
from flask import Flask, send_file
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def generate_plot(i):
    # 读取数据
    data_df = pd.read_csv(
        r"D:\Project-forecast\carbon\testdata\air-data.csv",
        index_col="Date",
        parse_dates=['Date']  # 解析时间
    )

    # 设定合理的数值范围
    # filtered_data = data_df[(data_df['PT08.S1(CO)'] > 750) & (data_df['PT08.S1(CO)'] < 1400)]
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
    # 确保索引去重
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
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf

    # plt.show()
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




# 48小时预测
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.dates as dates
# import statsmodels.api as sm
# from sklearn.metrics import mean_absolute_error, mean_squared_error
#
# def generate_future_forecast():
#     # 读取数据
#     data_df = pd.read_csv(
#         r"D:\Project-forecast\carbon\testdata\air-data.csv",
#         index_col="Date",
#         parse_dates=['Date']  # 解析时间
#     )
#
#     # 设定合理的数值范围
#     filtered_data = data_df[(data_df['PT08.S1(CO)'] > 750) & (data_df['PT08.S1(CO)'] < 1400)]
#
#     # 确保索引去重
#     filtered_data = filtered_data[~filtered_data.index.duplicated(keep='first')]
#
#     # **保持小时级时间索引**
#     filtered_data = filtered_data.asfreq('H').interpolate()
#
#     # **数据划分**
#     steps = 48  # 未来 48 小时
#     train_series = filtered_data.iloc[:-steps]['PT08.S1(CO)']  # 训练集
#     test_series = filtered_data.iloc[-steps:]['PT08.S1(CO)']  # 真实的 48 小时数据（测试集）
#
#     # 设定 ARIMA 参数
#     p, d, q = 1, 1, 0
#
#     # 训练 ARIMA 模型
#     model = sm.tsa.ARIMA(train_series, order=(p, d, q))
#     model_fit = model.fit()
#
#     # 预测未来 48 小时
#     forecast = model_fit.forecast(steps=steps)
#
#     # 生成未来 48 小时时间索引
#     future_dates = test_series.index  # 直接使用测试集的时间索引
#
#     # 创建预测数据表
#     future_forecast = pd.Series(forecast, index=future_dates)
#
#     # 计算误差指标
#     mae = mean_absolute_error(test_series, future_forecast)
#     rmse = mean_squared_error(test_series, future_forecast, squared=False)
#
#     print("\n=== 预测模型评估 ===")
#     print(f"MAE  = {mae:.4f}")
#     print(f"RMSE = {rmse:.4f}")
#
#     # **修复 train_plot**
#     train_plot = train_series.iloc[int(len(train_series) * 0.998):]
#
#     # 绘图
#     plt.figure(figsize=(12, 6))
#     # plt.plot(train_plot.index, train_plot, label='Data', color='blue')
#     plt.plot(test_series.index, test_series, label='Test', color='orange')
#     plt.plot(future_forecast.index, future_forecast, label='Predict', linestyle='--', color='green')
#
#     plt.legend()
#     plt.xticks(rotation=45)
#     plt.title("ARIMA")
#
#     # **设置 X 轴单位为小时**
#     plt.gca().xaxis.set_major_locator(dates.HourLocator(interval=6))  # 每 6 小时一个刻度
#     plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d %H:%M'))
#
#     plt.grid(True)
#     plt.gcf().autofmt_xdate()
#
#     plt.show()
#
# # 直接运行
# if __name__ == "__main__":
#     generate_future_forecast()

#
# # 小时预测网页呈现
# from flask import Flask, send_file
# import io
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.dates as dates
# import statsmodels.api as sm
#
# def generate_plot(i):
#     # 读取数据
#     data_df = pd.read_csv(
#         r"D:\Project-forecast\carbon\testdata\air-data.csv",
#         index_col="Date",
#         parse_dates=['Date']  # 解析时间
#     )
#
#     # 根据 i 的值选择不同的列进行预测
#     if i == 1:
#         filtered_data = data_df[(data_df['NO2(GT)'] > 200) & (data_df['NO2(GT)'] < 650)]
#     elif i == 2:
#         filtered_data = data_df[(data_df['PT08.S1(CO)'] > 750) & (data_df['PT08.S1(CO)'] < 1400)]
#     elif i == 3:
#         filtered_data = data_df[(data_df['PT08.S5(O3)'] > 750) & (data_df['PT08.S5(O3)'] < 1400)]
#     elif i == 4:
#         filtered_data = data_df[(data_df['PT08.S4(NO2)'] > 1250) & (data_df['PT08.S4(NO2)'] < 2000)]
#     else:
#         return False
#
#     # 确保索引去重并进行数据预处理
#     filtered_data = filtered_data[~filtered_data.index.duplicated(keep='first')]
#     filtered_data = filtered_data.infer_objects()
#     filtered_data = filtered_data.asfreq('h').interpolate()
#
#     # 确保数据集非空
#     if filtered_data.empty:
#         return False
#
#     # 数据划分
#     steps = 48  # 预测48小时
#     if i == 1:
#         train_series = filtered_data.iloc[:-steps]['NO2(GT)']
#         test_series = filtered_data.iloc[-steps:]['NO2(GT)']
#     elif i == 2:
#         train_series = filtered_data.iloc[:-steps]['PT08.S1(CO)']
#         test_series = filtered_data.iloc[-steps:]['PT08.S1(CO)']
#     elif i == 3:
#         train_series = filtered_data.iloc[:-steps]['PT08.S5(O3)']
#         test_series = filtered_data.iloc[-steps:]['PT08.S5(O3)']
#     elif i == 4:
#         train_series = filtered_data.iloc[:-steps]['PT08.S4(NO2)']
#         test_series = filtered_data.iloc[-steps:]['PT08.S4(NO2)']
#     else:
#         return False
#
#     # 设定 ARIMA 参数
#     p, d, q = 1, 1, 0
#
#     # 训练 ARIMA 模型
#     model = sm.tsa.ARIMA(train_series, order=(p, d, q))
#     model_fit = model.fit()
#
#     # 预测未来 48 小时
#     forecast = model_fit.forecast(steps=steps)
#
#     # 生成未来 48 小时的时间索引
#     future_dates = test_series.index
#
#     # 创建预测数据表
#     future_forecast = pd.Series(forecast, index=future_dates)
#
#     # 绘图
#     plt.figure(figsize=(12, 6))
#     # plt.plot(train_series.index, train_series, label='Train', color='blue')
#     plt.plot(test_series.index, test_series, label='Test', color='orange')
#     plt.plot(future_forecast.index, future_forecast, label='Predict', linestyle='--', color='green')
#
#     plt.legend()
#     plt.xticks(rotation=45)
#     plt.title("ARIMA")
#
#     # 设置 X 轴单位为小时
#     plt.gca().xaxis.set_major_locator(dates.HourLocator(interval=6))
#     plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%m-%d %H:%M'))
#
#     plt.grid(True)
#     plt.gcf().autofmt_xdate()
#
#     buf = io.BytesIO()
#     plt.savefig(buf, format='png')
#     plt.close()
#     buf.seek(0)
#     return buf
#
# # Flask 应用
# app = Flask(__name__)
#
# @app.route('/predict/<int:i>', methods=['GET'])
# def plot(i):
#     try:
#         buf = generate_plot(i)
#         return send_file(buf, mimetype='image/png')
#     except Exception as e:
#         return f"Error: {str(e)}", 500
#
# import matplotlib
# matplotlib.use('Agg')
#
# # 直接运行
# if __name__ == "__main__":
#     app.run(debug=True, use_reloader=False)
#
