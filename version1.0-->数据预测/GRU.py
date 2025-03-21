

import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from flask import Flask, send_file
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, GRU, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

# Flask 服务器
app = Flask(__name__)

def create_dataset(data, look_back):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:i + look_back])
        y.append(data[i + look_back])
    return np.array(X), np.array(y)


def build_gru_model(input_shape):
    model = Sequential([
        Input(shape=input_shape),
        GRU(128, return_sequences=True, activation='relu'),
        GRU(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model


# 预测函数
def generate_future_forecast(i):
    df = pd.read_csv(
        r"D:\Project-forecast\carbon\testdata\air-data.csv",
        index_col="Date",
        parse_dates=['Date']
    )

    # **数据清洗**
    if i == 1:
        filtered_data = df[(df['NO2(GT)'] > 200) & (df['NO2(GT)'] < 650)]
    elif i == 2:
        filtered_data = df[(df['PT08.S1(CO)'] > 750) & (df['PT08.S1(CO)'] < 1400)]
    elif i == 3:
        filtered_data = df[(df['PT08.S5(O3)'] > 750) & (df['PT08.S5(O3)'] < 1400)]
    elif i == 4:
        filtered_data = df[(df['PT08.S4(NO2)'] > 1250) & (df['PT08.S4(NO2)'] < 2000)]
    else:
        raise ValueError("Invalid parameter i. Must be 1, 2, 3, or 4")

    if filtered_data.empty:
        raise ValueError(f"No data available for the selected filter i={i}")

    # 确保数据格式正确
    filtered_data = filtered_data[~filtered_data.index.duplicated(keep='first')]
    filtered_data = filtered_data.infer_objects(copy=False)
    filtered_data = filtered_data.asfreq('h').interpolate()

    # **归一化**
    scaler = MinMaxScaler()
    feature_name = ['NO2(GT)', 'PT08.S1(CO)', 'PT08.S5(O3)', 'PT08.S4(NO2)'][i - 1]
    scaled_series = scaler.fit_transform(filtered_data[feature_name].values.reshape(-1, 1))

    # **构造训练集**
    LOOK_BACK, STEPS = 3, 48
    X_train, y_train = create_dataset(scaled_series[:-STEPS], LOOK_BACK)
    X_test, y_test = create_dataset(scaled_series[-STEPS - LOOK_BACK:], LOOK_BACK)
    X_train = X_train.reshape(-1, LOOK_BACK, 1)
    X_test = X_test.reshape(-1, LOOK_BACK, 1)


    # **训练模型**
    model = build_gru_model((LOOK_BACK, 1))
    early_stopping = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
    model.fit(X_train, y_train, epochs=500, batch_size=64, verbose=1, callbacks=[early_stopping])

    # **预测**
    y_pred_inverse = scaler.inverse_transform(model.predict(X_test))
    y_true = scaler.inverse_transform(y_test.reshape(-1, 1))

    # **绘图**
    future_dates = filtered_data.index[-STEPS:]
    plt.figure(figsize=(12, 6))
    plt.plot(future_dates, y_true, label='Test', color='orange')
    plt.plot(future_dates, y_pred_inverse, label='Predict', linestyle='--', color='green')
    plt.legend()
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(dates.HourLocator(interval=6))
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.grid(True)
    plt.gcf().autofmt_xdate()

    # **返回图片**
    buf = io.BytesIO()
    try:
        plt.savefig(buf, format='png')
        buf.seek(0)
    except Exception as e:
        raise RuntimeError(f"Failed to generate plot: {e}")

    return buf

@app.route('/predict/<int:i>', methods=['GET'])
def plot(i):
    try:
        buf = generate_future_forecast(i)
        return send_file(buf, mimetype='image/png')
    except ValueError as e:
        return f"Error: {str(e)}", 400
    except RuntimeError as e:
        return f"Error: {str(e)}", 500
    except Exception as e:
        return f"Unexpected Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)




# 小时预测
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.dates as dates
# from sklearn.preprocessing import MinMaxScaler
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Input, GRU, Dense, Dropout
# from tensorflow.keras.callbacks import EarlyStopping
# from sklearn.metrics import mean_absolute_error, mean_squared_error
#
# # 配置参数
# LOOK_BACK = 3  # 时间窗口
# EPOCHS = 500   # 训练轮数
# BATCH_SIZE = 64  # 批处理大小
# STEPS = 48  # 预测未来 48 小时
#
# # 创建数据集
# def create_dataset(data, look_back):
#     X, y = [], []
#     for i in range(len(data) - look_back):
#         X.append(data[i:i + look_back])
#         y.append(data[i + look_back])
#     return np.array(X), np.array(y)
#
# # 构建 GRU 模型
# def build_gru_model(input_shape):
#     model = Sequential([
#         Input(shape=input_shape),
#         GRU(128, return_sequences=True, activation='relu'),
#         GRU(64, activation='relu'),
#         Dense(32, activation='relu'),
#         Dense(1)
#     ])
#     model.compile(optimizer='adam', loss='mse')
#     return model
#
# # 生成预测
# def generate_future_forecast():
#     # 读取数据
#     df = pd.read_csv(
#         r"D:\Project-forecast\carbon\testdata\air-data.csv",
#         index_col="Date",
#         parse_dates=['Date']
#     )
#
#     # 数据清洗
#     filtered_data = df[(df['PT08.S1(CO)'] > 750) & (df['PT08.S1(CO)'] < 1400)]
#     filtered_data = filtered_data[~filtered_data.index.duplicated(keep='first')]
#     filtered_data = filtered_data.asfreq('H').interpolate()  # 保持小时级时间索引
#
#     # 归一化
#     scaler = MinMaxScaler()
#     scaled_series = scaler.fit_transform(filtered_data['PT08.S1(CO)'].values.reshape(-1, 1))
#
#     # 训练集、测试集划分
#     train_series = scaled_series[:-STEPS]
#     test_series = scaled_series[-STEPS - LOOK_BACK:]
#
#     # 构造数据集
#     X_train, y_train = create_dataset(train_series, LOOK_BACK)
#     X_train = X_train.reshape(-1, LOOK_BACK, 1)
#
#     X_test, y_test = create_dataset(test_series, LOOK_BACK)
#     X_test = X_test.reshape(-1, LOOK_BACK, 1)
#
#     # 构建 & 训练 GRU
#     model = build_gru_model((LOOK_BACK, 1))
#     early_stopping = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
#     model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1, callbacks=[early_stopping])
#
#     # 预测
#     y_pred_scaled = model.predict(X_test)
#
#     # 逆归一化
#     y_pred_inverse = scaler.inverse_transform(y_pred_scaled)
#     y_true = scaler.inverse_transform(y_test.reshape(-1, 1))
#
#     # 误差计算
#     mae = mean_absolute_error(y_true, y_pred_inverse)
#     rmse = mean_squared_error(y_true, y_pred_inverse, squared=False)
#
#     print("\n=== 预测模型评估 ===")
#     print(f"MAE  = {mae:.4f}")
#     print(f"RMSE = {rmse:.4f}")
#
#     # 获取未来时间索引
#     future_dates = filtered_data.index[-STEPS:]
#
#     # **绘图**
#     plt.figure(figsize=(12, 6))
#     plt.plot(future_dates, y_true, label='Test', color='orange')
#     plt.plot(future_dates, y_pred_inverse, label='Predict', linestyle='--', color='green')
#
#     plt.legend()
#     plt.xticks(rotation=45)
#     plt.title("GRU")
#
#     # **设置 X 轴单位**
#     plt.gca().xaxis.set_major_locator(dates.HourLocator(interval=6))
#     plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d %H:%M'))
#
#     plt.grid(True)
#     plt.gcf().autofmt_xdate()
#     plt.show()
#
# if __name__ == '__main__':
#     generate_future_forecast()





# v2.0月份预测
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.preprocessing import MinMaxScaler
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Input, GRU, Dense,Dropout
# from tensorflow.keras.callbacks import EarlyStopping
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
#
#
# # 配置参数
# LOOK_BACK = 3      # 时间窗口长度
# EPOCHS = 1000       # 训练轮数（可调节）
# BATCH_SIZE = 300    # 批处理大小
#
# # 创建数据集
# def create_dataset(data, look_back=3):
#     X, y = [], []
#     for i in range(len(data) - look_back):
#         X.append(data[i:(i + look_back)])
#         y.append(data[i + look_back])
#     return np.array(X), np.array(y)
#
# # 构建 GRU 模型
# def build_gru_model(input_shape):
#     model = Sequential([
#         Input(shape=input_shape),
#         GRU(128, return_sequences=True, activation='relu'),  # 第一层 GRU
#         GRU(64, activation='relu'),  # 第二层 GRU
#         Dense(64, activation='relu'),  # 全连接层
#         Dense(1)  # 输出层
#     ])
#     model.compile(optimizer='adam', loss='mse')
#     return model
#
# # 生成预测结果并绘图
# def generate_plot():
#     # 读取 CSV 文件
#     df = pd.read_csv(
#         r"D:\Project-forecast\carbon\testdata\air-data.csv",
#         index_col="Date",  # 设置时间为索引
#         parse_dates=['Date']  # 解析时间格式
#     )
#
#     # 数据过滤
#     filtered_data = df[(df['PT08.S1(CO)'] > 750) & (df['PT08.S1(CO)'] < 1800)]
#     full_series = filtered_data['PT08.S1(CO)'].dropna()
#
#     # 数据归一化（MinMaxScaler）
#     scaler = MinMaxScaler()
#     scaled_series = scaler.fit_transform(full_series.values.reshape(-1, 1))
#
#     # 划分训练集和测试集（80% 训练，20% 测试）
#     split_idx = int(len(scaled_series) * 0.8)
#     train_scaled = scaled_series[:split_idx]
#     test_scaled = scaled_series[split_idx:]
#
#     # 创建训练集和测试集
#     X_train, y_train = create_dataset(train_scaled, LOOK_BACK)
#     X_train = X_train.reshape(-1, LOOK_BACK, 1)
#
#     X_test, y_test_scaled = create_dataset(test_scaled, LOOK_BACK)
#     X_test = X_test.reshape(-1, LOOK_BACK, 1)
#
#     # 构建并训练 GRU 模型
#     model = build_gru_model((LOOK_BACK, 1))
#     early_stopping = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
#     model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1, callbacks=[early_stopping])
#
#     # 预测
#     y_pred_scaled = model.predict(X_test)
#
#     # 逆归一化
#     y_pred_inverse = scaler.inverse_transform(y_pred_scaled)
#
#     # 获取真实值（y_true）
#     y_true = full_series.iloc[split_idx + LOOK_BACK:split_idx + LOOK_BACK + len(y_pred_inverse)].values.reshape(-1, 1)
#
#     # **平滑预测曲线（滑动平均）**
#     window_size = 5  # 窗口大小
#     y_pred_smooth = pd.Series(y_pred_inverse.flatten()).rolling(window=window_size, center=True).mean()
#
#     # **计算误差指标**
#     mae = mean_absolute_error(y_true, y_pred_inverse)
#     rmse = mean_squared_error(y_true, y_pred_inverse, squared=False)
#     mape = (abs((y_true - y_pred_inverse) / y_true)).mean() * 100
#     r2 = r2_score(y_true, y_pred_inverse)
#
#     # **打印模型评估结果**
#     print("\n=== 预测模型评估指标 ===")
#     print(f"MAE  = {mae:.4f}")
#     print(f"RMSE = {rmse:.4f}")
#     print(f"MAPE = {mape:.2f}%")
#     print(f"R²   = {r2:.4f}")
#
#     # **绘图优化**
#     plt.figure(figsize=(12, 6))
#
#     # 真实值（测试集）
#     plt.plot(full_series.index[split_idx + LOOK_BACK:], y_true, color='red', label='Test', alpha=0.7, linewidth=2)
#
#     # 平滑后的预测值
#     plt.plot(full_series.index[split_idx + LOOK_BACK:], y_pred_smooth, color='green', linestyle='--', label='Predict', linewidth=2)
#
#     plt.title('GRU')
#     plt.xlabel('Date')
#     plt.ylabel('CO2')
#     plt.legend()
#     plt.grid(True, linestyle='--', alpha=0.6)
#     plt.show()
#
# if __name__ == '__main__':
#     generate_plot()




# v1.0预测
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.preprocessing import StandardScaler
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Input, GRU, Dense
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
#
#
# # 配置参数
# LOOK_BACK = 3  # 时间窗口长度
# EPOCHS = 100  # 训练轮数
# BATCH_SIZE = 20  # 批处理大小
#
# def create_dataset(data, look_back=3):
#     X, y = [], []
#     for i in range(len(data) - look_back):
#         X.append(data[i:(i + look_back)])
#         y.append(data[i + look_back])
#     return np.array(X), np.array(y)
#
# def build_gru_model(input_shape):
#     model = Sequential([
#         Input(shape=input_shape),  # 使用 Input 层明确指定输入形状
#         GRU(64, activation='relu'),  # GRU 层
#         Dense(1)
#     ])
#     model.compile(optimizer='adam', loss='mse')
#     return model
#
# def generate_plot():
#     # 从文件加载数据
#     df = pd.read_csv(
#         r"D:\Project-forecast\carbon\testdata\air-data.csv",
#         index_col="Date",  # 设置时间为索引
#         parse_dates=['Date']  # 解析时间戳
#     )
#
#     # 数据过滤
#     filtered_data = df[(df['PT08.S1(CO)'] > 750) & (df['PT08.S1(CO)'] < 1800)]
#     full_series = filtered_data['PT08.S1(CO)'].dropna()
#
#     # 标准化处理
#     scaler = StandardScaler()
#     scaled_series = scaler.fit_transform(full_series.values.reshape(-1, 1))
#
#     # 划分训练集和测试集
#     split_idx = int(len(scaled_series) * 0.8)
#     train_scaled = scaled_series[:split_idx]
#     test_scaled = scaled_series[split_idx:]
#
#     # 创建训练集和测试集窗口
#     X_train, y_train = create_dataset(train_scaled, LOOK_BACK)
#     X_train = X_train.reshape(-1, LOOK_BACK, 1)
#
#     X_test, y_test_scaled = create_dataset(test_scaled, LOOK_BACK)
#     X_test = X_test.reshape(-1, LOOK_BACK, 1)
#
#     # 训练 GRU 模型
#     model = build_gru_model((LOOK_BACK, 1))
#     model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=0)
#
#     # 预测
#     y_pred_scaled = model.predict(X_test)
#
#     # 逆标准化
#     y_pred_inverse = scaler.inverse_transform(y_pred_scaled)
#
#     # 获取真实值（y_true）
#     y_true = full_series.iloc[split_idx + LOOK_BACK:split_idx + LOOK_BACK + len(y_pred_inverse)].values.reshape(-1, 1)
#
#     # ** 计算训练集的最后 20% 索引 **
#     train_timestamps = full_series.index[:split_idx + LOOK_BACK]
#     train_last_20_idx = int(len(train_timestamps) )
#     train_timestamps_partial = train_timestamps[train_last_20_idx+3:]  # 只取后 20% 时间索引
#     train_data_partial = full_series.iloc[train_last_20_idx:split_idx]  # 只取后 20% 训练数据
#
#     # ** 计算误差指标 **
#     mae = mean_absolute_error(y_true, y_pred_inverse)
#     rmse = mean_squared_error(y_true, y_pred_inverse, squared=False)
#     mape = (abs((y_true - y_pred_inverse) / y_true)).mean() * 100
#     r2 = r2_score(y_true, y_pred_inverse)
#
#     # 打印评估结果
#     print("\n=== 预测模型评估指标 ===")
#     print(f"MAE  = {mae:.4f}")
#     print(f"RMSE = {rmse:.4f}")
#     print(f"MAPE = {mape:.2f}%")
#     print(f"R²   = {r2:.4f}")
#
#     # ** 绘图 **
#     plt.figure(figsize=(12, 6))
#     # plt.plot(train_timestamps_partial, train_data_partial, alpha=0.3, label='Train', color='blue')
#     plt.plot(full_series.index[split_idx + LOOK_BACK:], y_true, color='red', label='Test Data')
#     plt.plot(full_series.index[split_idx + LOOK_BACK:], y_pred_inverse, color='green', linestyle='--', label='Predicted Data)')
#
#     plt.title(f'GRU')
#     plt.legend()
#     plt.grid(True)
#
#     plt.show()
#
# if __name__ == '__main__':
#     generate_plot()
