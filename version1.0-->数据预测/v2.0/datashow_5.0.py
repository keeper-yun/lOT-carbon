import csv

import matplotlib
import requests
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import io
from flask import Flask, send_file
from apscheduler.schedulers.background import BackgroundScheduler

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
        parse_dates=['timestamp']  # 将 'timestamp' 转为 DatetimeIndex
    )
    # 确保索引单调递增并设置频率
    data_df = data_df.sort_index()
    data_df.index.freq = pd.infer_freq(data_df.index)

    # 数据切片
    train = data_df.iloc[:-3]['co2_Output']
    test = data_df.iloc[-3:]['co2_Output']

    # 拟合 ARIMA 模型
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
        history.append(obs)  # 滚动预测

    # 生成预测结果
    predict = pd.Series(forecast, index=test.index)

    # 绘图
    buf = io.BytesIO()
    plt.figure(figsize=(12, 6))
    plt.plot(train.index, train, label='Train')
    plt.plot(test.index, test, label='Test', color='orange')
    plt.plot(predict.index, predict, label='Predict', linestyle='--', color='green')
    plt.legend()
    plt.xticks(rotation=45)
    plt.title("Prediction vs Test Data")
    plt.savefig(buf, format='png')  # 保存图像到内存
    plt.close()  # 关闭图表，释放内存
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
