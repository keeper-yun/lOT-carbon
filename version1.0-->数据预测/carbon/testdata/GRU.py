import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, GRU, Dense
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import io

# 配置参数
LOOK_BACK = 3  # 时间窗口长度
EPOCHS = 100  # 训练轮数
BATCH_SIZE = 2  # 批处理大小


def create_dataset(data, look_back=3):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back)])
        y.append(data[i + look_back])
    return np.array(X), np.array(y)


def build_gru_model(input_shape):
    model = Sequential([
        Input(shape=input_shape),  # 使用 Input 层明确指定输入形状
        GRU(64, activation='relu'),  # GRU 层不再需要 input_shape 参数
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model


def generate_plot():
    # 数据加载与分割
    df = pd.read_csv(
        r"D:\Project-forecast\carbon\testdata\air-quality-data.csv",
        index_col="Date",  # 设置时间为索引
        parse_dates=['Date']  # 解析时间戳
    )

    filtered_data = df[(df['PT08.S1(CO)'] > 750) & (df['PT08.S1(CO)'] < 1800)]

    full_series = filtered_data['PT08.S1(CO)'].dropna()

    # 对数据进行差分处理（与ARIMA相似）
    diff_series = full_series.diff().dropna()

    # 划分训练集和测试集
    split_idx = int(len(diff_series) * 0.8)
    train_series = diff_series.iloc[:split_idx]
    test_series = diff_series.iloc[split_idx:]  # 测试集（后20%数据）

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

    # 将预测值逆变换，并加回差分
    y_pred = scaler.inverse_transform(y_pred_scaled) + full_series.iloc[split_idx - LOOK_BACK:].values.reshape(-1, 1)

    # 计算评估指标
    mae = mean_absolute_error(test_series[LOOK_BACK:], y_pred)
    rmse = mean_squared_error(test_series[LOOK_BACK:], y_pred, squared=False)  # RMSE
    mape = (abs((test_series[LOOK_BACK:] - y_pred) / test_series[LOOK_BACK:])).mean() * 100  # MAPE 百分比误差
    r2 = r2_score(test_series[LOOK_BACK:], y_pred)  # R²

    # 打印评估指标
    print(f"MAE  = {mae:.4f}")
    print(f"RMSE = {rmse:.4f}")
    print(f"MAPE = {mape:.2f}%")
    print(f"R²   = {r2:.4f}")

    # 可视化对比
    plt.figure(figsize=(12, 6))
    plt.plot(full_series.index, full_series, 'gray', alpha=0.3, label='Full Data')
    plt.plot(test_series.index[LOOK_BACK:], test_series[LOOK_BACK:], 'bo-', label='Actual (Test)')
    plt.plot(test_series.index[LOOK_BACK:], y_pred, 'rs--', label='GRU Forecast (Test)')
    plt.title(f'GRU')
    plt.legend()
    plt.grid(True)

    # 保存图像到字节流
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img


if __name__ == '__main__':
    generate_plot()
