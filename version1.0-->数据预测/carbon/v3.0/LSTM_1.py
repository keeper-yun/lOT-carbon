import tensorflow as tf
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 设置绘图参数
mpl.rcParams['figure.figsize'] = (8, 6)
mpl.rcParams['axes.grid'] = False

# 数据加载和预处理
df = pd.read_csv(
    r"D:\Project-forecast\carbon\v3.0\factory1.csv",
    parse_dates=['timestamp']  # 将 'timestamp' 转为 DatetimeIndex
)

# 提取目标列并设置索引
uni_data = df['co2_Output']
uni_data.index = df['timestamp']

# 数据标准化
uni_data = uni_data.values  # 转为 NumPy 数组
TRAIN_SPLIT = int(len(uni_data) * 0.5)  # 训练集分割比例，50% 用作训练
uni_train_mean = uni_data[:TRAIN_SPLIT].mean()  # 训练集均值
uni_train_std = uni_data[:TRAIN_SPLIT].std()  # 训练集标准差
uni_data = (uni_data - uni_train_mean) / uni_train_std  # 标准化数据

# 数据生成函数
def univariate_data(dataset, start_index, end_index, history_size, target_size):
    data = []
    labels = []

    start_index += history_size
    if end_index is None:
        end_index = len(dataset)

    for i in range(start_index, end_index - target_size + 1):
        indices = range(i - history_size, i)
        data.append(np.reshape(dataset[indices], (history_size, 1)))  # (history_size, 1)
        labels.append(dataset[i:i + target_size])  # (target_size,)

    return np.array(data), np.array(labels)

# 可视化函数
def create_time_steps(length):
    return list(range(-length, 0))

def show_plot(plot_data, delta, title):
    """
    plot_data: [历史数据, 真实未来值, 预测值]
    """
    labels = ['History', 'True Future', 'Model Prediction']
    marker = ['.-', 'rx', 'go']
    time_steps = create_time_steps(plot_data[0].shape[0])  # 历史时间步
    future_steps = range(delta, delta + len(plot_data[1]))  # 未来时间步

    plt.title(title)

    # 绘制历史数据
    plt.plot(time_steps, plot_data[0].flatten(), marker[0], label=labels[0])

    # 绘制真实未来值
    plt.plot(future_steps, plot_data[1].flatten(), marker[1], markersize=10, label=labels[1])

    # 绘制预测值
    plt.plot(future_steps, plot_data[2].flatten(), marker[2], markersize=10, label=labels[2])

    plt.legend()
    plt.xlabel('Time-Step')
    plt.show()

# 设置历史序列长度和预测目标
univariate_past_history = 5  # 使用过去 5 个时间步的历史数据
univariate_future_target = 2  # 预测未来 2 个时间步的值

# 生成训练和验证数据
x_train_uni, y_train_uni = univariate_data(
    uni_data, 0, TRAIN_SPLIT,
    univariate_past_history,
    univariate_future_target
)

x_val_uni, y_val_uni = univariate_data(
    uni_data, TRAIN_SPLIT, None,
    univariate_past_history,
    univariate_future_target
)

print("训练集形状:", x_train_uni.shape, y_train_uni.shape)
print("验证集形状:", x_val_uni.shape, y_val_uni.shape)

# 数据集转换为 TensorFlow Dataset
BATCH_SIZE = 256
BUFFER_SIZE = 10000

train_univariate = tf.data.Dataset.from_tensor_slices((x_train_uni, y_train_uni))
train_univariate = train_univariate.cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE).repeat()

val_univariate = tf.data.Dataset.from_tensor_slices((x_val_uni, y_val_uni))
val_univariate = val_univariate.batch(BATCH_SIZE).repeat()

# 定义 LSTM 模型
simple_lstm_model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(8, input_shape=(univariate_past_history, 1), return_sequences=False),
    tf.keras.layers.Dense(univariate_future_target)
])

simple_lstm_model.compile(optimizer='adam', loss='mae')

# 模型训练
EVALUATION_INTERVAL = 200
EPOCHS = 10

simple_lstm_model.fit(
    train_univariate,
    epochs=EPOCHS,
    steps_per_epoch=EVALUATION_INTERVAL,
    validation_data=val_univariate,
    validation_steps=50
)

# 使用模型进行预测并可视化结果
for x, y in val_univariate.take(3):
    prediction = simple_lstm_model.predict(x)  # 预测值
    for i in range(min(len(x), 3)):  # 每次绘制 3 个样本
        show_plot(
            [x[i].numpy(), y[i].numpy(), prediction[i]],
            delta=0,
            title='Simple LSTM Model - Multi-step Prediction'
        )
