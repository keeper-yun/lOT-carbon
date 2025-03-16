import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, GRU, Dense
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# 配置参数
LOOK_BACK = 3  # 时间窗口长度
EPOCHS = 100  # 训练轮数
BATCH_SIZE = 20  # 批处理大小

def create_dataset(data, look_back=3):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back)])
        y.append(data[i + look_back])
    return np.array(X), np.array(y)

def build_gru_model(input_shape):
    model = Sequential([
        Input(shape=input_shape),  # 使用 Input 层明确指定输入形状
        GRU(64, activation='relu'),  # GRU 层
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def generate_plot():
    # 从文件加载数据
    df = pd.read_csv(
        r"D:\Project-forecast\carbon\testdata\air-quality-data.csv",
        index_col="Date",  # 设置时间为索引
        parse_dates=['Date']  # 解析时间戳
    )

    # 数据过滤
    filtered_data = df[(df['PT08.S1(CO)'] > 750) & (df['PT08.S1(CO)'] < 1800)]
    full_series = filtered_data['PT08.S1(CO)'].dropna()

    # 标准化处理
    scaler = StandardScaler()
    scaled_series = scaler.fit_transform(full_series.values.reshape(-1, 1))

    # 划分训练集和测试集
    split_idx = int(len(scaled_series) * 0.8)
    train_scaled = scaled_series[:split_idx]
    test_scaled = scaled_series[split_idx:]

    # 创建训练集和测试集窗口
    X_train, y_train = create_dataset(train_scaled, LOOK_BACK)
    X_train = X_train.reshape(-1, LOOK_BACK, 1)

    X_test, y_test_scaled = create_dataset(test_scaled, LOOK_BACK)
    X_test = X_test.reshape(-1, LOOK_BACK, 1)

    # 训练 GRU 模型
    model = build_gru_model((LOOK_BACK, 1))
    model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=0)

    # 预测
    y_pred_scaled = model.predict(X_test)

    # 逆标准化
    y_pred_inverse = scaler.inverse_transform(y_pred_scaled)

    # 获取真实值（y_true）
    y_true = full_series.iloc[split_idx + LOOK_BACK:split_idx + LOOK_BACK + len(y_pred_inverse)].values.reshape(-1, 1)

    # ** 计算训练集的最后 20% 索引 **
    train_timestamps = full_series.index[:split_idx + LOOK_BACK]
    train_last_20_idx = int(len(train_timestamps) * 0.95)
    train_timestamps_partial = train_timestamps[train_last_20_idx+3:]  # 只取后 20% 时间索引
    train_data_partial = full_series.iloc[train_last_20_idx:split_idx]  # 只取后 20% 训练数据

    # ** 计算误差指标 **
    mae = mean_absolute_error(y_true, y_pred_inverse)
    rmse = mean_squared_error(y_true, y_pred_inverse, squared=False)
    mape = (abs((y_true - y_pred_inverse) / y_true)).mean() * 100
    r2 = r2_score(y_true, y_pred_inverse)

    # 打印评估结果
    print("\n=== 预测模型评估指标 ===")
    print(f"MAE  = {mae:.4f}")
    print(f"RMSE = {rmse:.4f}")
    print(f"MAPE = {mape:.2f}%")
    print(f"R²   = {r2:.4f}")

    # ** 绘图 **
    plt.figure(figsize=(12, 6))
    plt.plot(train_timestamps_partial, train_data_partial, alpha=0.3, label='Train', color='blue')
    plt.plot(full_series.index[split_idx + LOOK_BACK:], y_true, color='red', label='Test Data')
    plt.plot(full_series.index[split_idx + LOOK_BACK:], y_pred_inverse, color='green', linestyle='--', label='Predicted Data)')

    plt.title(f'GRU')
    plt.legend()
    plt.grid(True)

    plt.show()

if __name__ == '__main__':
    generate_plot()
