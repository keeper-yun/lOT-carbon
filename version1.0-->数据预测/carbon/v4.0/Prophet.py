

import csv

import matplotlib
import requests
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
import io
from flask import Flask, send_file
from apscheduler.schedulers.background import BackgroundScheduler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

matplotlib.use("Agg")

# Flask 应用
app = Flask(__name__)

# 定义请求头
headers = {
    'User-Agent': ')Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0\
     Safari/537.36 Edg/120.0.0.0'
}

# API 数据地址
url = f'http://localhost:8181/monitoring/find'


# 数据写入功能
def writedata(num, data):
    with open(f'factory{num}.csv', 'w', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(
            [u'recordId', u'co2_Level', u'n2o_Level', u'ch4_Level', u'co2_Flow',
             u'co2_Output', u'n2o_Output', u'ch4_Output', u'factoryId', u'timestamp']
        )
        for i in data:
            if i.get('factoryId') == num:
                csv_writer.writerow([
                    i.get('recordId'),
                    i.get('co2_Level'),
                    i.get('n2o_Level'),
                    i.get('ch4_Level'),
                    i.get('co2_Flow'),
                    i.get('co2_Output'),
                    i.get('n2o_Output'),
                    i.get('ch4_Output'),
                    i.get('factoryId'),
                    i.get('timestamp')
                ])


# 定时任务：数据获取并写入
def fetch_and_write():
    print("Fetching data from API...")
    resp = requests.get(url, headers=headers)
    data = resp.json()
    for factory_id in range(1, 5):
        writedata(factory_id, data)
    print("Data fetched and written successfully.")


# 绘图功能
def generate_plot(i):
    # 读取数据
    data_df = pd.read_csv(
        f"factory{i}.csv",
        index_col="timestamp",
        parse_dates=['timestamp']
    )
    data_df = data_df.sort_index()

    # 适配 Prophet 格式
    df = data_df.reset_index()[['timestamp', 'co2_Output']]
    df.columns = ['ds', 'y']

    # 划分训练集和测试集（前 90% 作为训练集，后 10% 作为测试集）
    split_index = int(len(df) * 0.9)
    train = df.iloc[:split_index]
    test = df.iloc[split_index:]

    # 初始化 Prophet 模型
    model = Prophet()
    model.fit(train)

    # 预测未来 test.shape[0] 天的数据
    future = model.make_future_dataframe(periods=len(test), freq='D')
    forecast = model.predict(future)

    # 只取测试集对应的预测部分进行对比
    forecast_test = forecast.iloc[-len(test):][['ds', 'yhat']]

    # 计算评估指标
    y_test = test['y'].values
    y_pred = forecast_test['yhat'].values

    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)  # RMSE
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100  # MAPE 百分比误差
    r2 = r2_score(y_test, y_pred)  # R²

    # 打印指标
    print(f"Factory {i} Evaluation Metrics:")
    print(f"MAE  = {mae:.4f}")
    print(f"RMSE = {rmse:.4f}")
    print(f"MAPE = {mape:.2f}%")
    print(f"R²   = {r2:.4f}")

    # 绘图
    buf = io.BytesIO()
    plt.figure(figsize=(12, 6))
    plt.plot(train['ds'], train['y'], label='Train', color='blue')
    plt.plot(test['ds'], test['y'], label='Test', color='orange')
    plt.plot(forecast_test['ds'], forecast_test['yhat'], label='Predict', linestyle='--', color='green')
    plt.legend()
    plt.xticks(rotation=45)
    plt.title(f"Prediction vs Test Data (Factory {i}) - Prophet")
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return buf


# Flask 路由
@app.route('/predict/<int:i>', methods=['GET'])
def plot(i):
    try:
        buf = generate_plot(i)
        return send_file(buf, mimetype='image/png')
    except FileNotFoundError:
        return f"Factory {i} data not found!", 404
    except Exception as e:
        return f"Error: {str(e)}", 500


# 启动 Flask 和定时任务
if __name__ == "__main__":
    # 创建定时任务
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_write, 'interval', hours=24)
    scheduler.start()

    # 保证 Flask 和定时任务可以同时运行
    # threading.Thread(target=lambda: app.run(debug=True, use_reloader=False)).start()
    app.run(debug=True, use_reloader=False)
