
import csv
import io
import requests
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense
from flask import Flask, send_file
from apscheduler.schedulers.background import BackgroundScheduler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

matplotlib.use("Agg")
app = Flask(__name__)

# 配置参数
LOOK_BACK = 3  # 时间窗口长度
EPOCHS = 100  # 训练轮数
BATCH_SIZE = 2  # 批处理大小

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
}
url = 'http://localhost:8181/monitoring/find'


def writedata(num, data):
    with open(f'factory{num}.csv', 'w', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([
            'recordId', 'co2_Level', 'n2o_Level', 'ch4_Level', 'co2_Flow',
            'co2_Output', 'n2o_Output', 'ch4_Output', 'factoryId', 'timestamp'
        ])
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


def fetch_and_write():
    print("Fetching data from API...")
    resp = requests.get(url, headers=headers)
    data = resp.json()
    for factory_id in range(1, 5):
        writedata(factory_id, data)
    print("Data fetched and written successfully.")


def create_dataset(data, look_back=3):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back)])
        y.append(data[i + look_back])
    return np.array(X), np.array(y)


def build_gru_model(input_shape):
    model = Sequential([
        GRU(64, activation='relu', input_shape=input_shape),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model


def generate_plot(factory_id):
    try:
        # 数据加载与分割
        df = pd.read_csv(f'factory{factory_id}.csv', parse_dates=['timestamp'])
        full_series = df['co2_Output'].dropna()

        split_idx = int(len(full_series) * 0.8)
        train_series = full_series.iloc[:split_idx]
        test_series = full_series.iloc[split_idx:]  # 测试集（后20%数据）

        # 标准化处理
        scaler = StandardScaler()
        train_scaled = scaler.fit_transform(train_series.values.reshape(-1, 1))
        test_scaled = scaler.transform(test_series.values.reshape(-1, 1))

        # 创建训练集窗口
        X_train, y_train = create_dataset(train_scaled, LOOK_BACK)
        X_train = X_train.reshape(-1, LOOK_BACK, 1)

        # 创建测试集窗口
        combined_scaled = np.concatenate([train_scaled[-LOOK_BACK:], test_scaled])
        X_test, y_test_scaled = create_dataset(combined_scaled, LOOK_BACK)
        X_test = X_test.reshape(-1, LOOK_BACK, 1)

        # 模型训练
        model = build_gru_model((LOOK_BACK, 1))
        model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=0)

        # 生成预测
        y_pred_scaled = model.predict(X_test)
        y_pred = scaler.inverse_transform(y_pred_scaled)
        y_test = scaler.inverse_transform(y_test_scaled)

        # 计算评估指标
        mae = mean_absolute_error(y_test, y_pred)
        rmse = mean_squared_error(y_test, y_pred, squared=False)  # RMSE
        mape = (abs((y_test - y_pred) / y_test)).mean() * 100  # MAPE 百分比误差
        r2 = r2_score(y_test, y_pred)  # R²

        # 打印指标
        print(f"Factory {factory_id} Evaluation Metrics:")
        print(f"MAE  = {mae:.4f}")
        print(f"RMSE = {rmse:.4f}")
        print(f"MAPE = {mape:.2f}%")
        print(f"R²   = {r2:.4f}")

        # 可视化对比
        plt.figure(figsize=(12, 6))
        plt.plot(full_series.index, full_series, 'gray', alpha=0.3, label='Full Data')
        plt.plot(test_series.index, test_series, 'bo-', label='Actual (Test)')
        plt.plot(test_series.index, y_pred, 'rs--', label='GRU Forecast (Test)')
        plt.title(f'Factory {factory_id} CO2 Output Prediction')
        plt.legend()
        plt.grid(True)

        # 保存图像到字节流
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()
        return img

    except Exception as e:
        print(f"Error generating plot for factory {factory_id}: {str(e)}")
        return None


@app.route('/predict/<int:factory_id>')
def get_plot(factory_id):
    img = generate_plot(factory_id)
    return send_file(img, mimetype='image/png') if img else ("Error generating plot", 500)


scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_write, 'interval', hours=24)
scheduler.start()

if __name__ == '__main__':
    app.run(port=5000)



# MAE、RMSE、MAPE、R²
#
# MAE和RMSE都是误差指标，越小越好
# MAPE是百分比误差，适用于不同量纲的数据，但真实值不能为零
# R²接近1表示模型解释能力强，越接近1越好
