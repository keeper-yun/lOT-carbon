import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 读取数据并解析时间戳
data = pd.read_csv(r"D:\Project-forecast\carbon\v2.0\factory3.csv", parse_dates=['timestamp'])

# 提取输出列并归一化
output = data.loc[:, 'co2_Output']
output_norm = output / max(output)

# 提取时间戳
timestamps = data['timestamp']


def extract_data(data, time_step):
    x, y = [], []
    for i in range(len(data) - time_step):
        x.append([a for a in data[i:i + time_step]])
        y.append(data[i + time_step])
    x = np.array(x)
    y = np.array(y)
    x = x.reshape(x.shape[0], x.shape[1], 1)
    return x, y


# 定义时间步
time_step = 5
x, y = extract_data(output_norm, time_step)

# 转换为Tensor
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
x = torch.tensor(x, dtype=torch.float32).to(device)
y = torch.tensor(y, dtype=torch.float32).to(device)

# 数据划分
train_size = int(len(x) * 0.8)
train_x, test_x = x[:train_size], x[train_size:]
train_y, test_y = y[:train_size], y[train_size:]

# 提取训练和测试时间戳
train_timestamps = timestamps[:train_size + time_step]
test_timestamps = timestamps[train_size + time_step:train_size + time_step + len(test_y)]

# 数据加载器
train_loader = DataLoader(TensorDataset(train_x, train_y), batch_size=64, shuffle=True)


# 定义LSTM模型
class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])  # 取最后一个时间步的输出
        return out


# 超参数设置
input_size = 1
hidden_size = 32
num_layers = 2
output_size = 1
learning_rate = 0.05
epochs = 100

# 实例化模型
model = LSTM(input_size, hidden_size, num_layers, output_size).to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# 模型训练
losses = []
for epoch in range(epochs):
    model.train()
    for batch_x, batch_y in train_loader:
        outputs = model(batch_x)
        loss = criterion(outputs.squeeze(), batch_y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    losses.append(loss.item())
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}')

# 模型评估
model.eval()
with torch.no_grad():
    pred_y = model(test_x).cpu().numpy()
    true_y = test_y.cpu().numpy()

# 反归一化
max_output = max(output)
pred_y = pred_y * max_output
true_y = true_y * max_output

# 计算评估指标
mae = mean_absolute_error(true_y, pred_y)
rmse = mean_squared_error(true_y, pred_y, squared=False)  # RMSE 是 MSE 的平方根
mape = (abs((true_y - pred_y) / true_y)).mean() * 100  # 百分比误差
r2 = r2_score(true_y, pred_y)

# 打印指标
print("Evaluation Metrics:")
print(f"MAE  = {mae:.4f}")
print(f"RMSE = {rmse:.4f}")
print(f"MAPE = {mape:.2f}%")
print(f"R²   = {r2:.4f}")

# 可视化结果
plt.figure(figsize=(12, 6))

# 原始数据用完整时间轴
plt.plot(timestamps, output, label='Original Data')

# 预测数据用测试时间轴
plt.plot(test_timestamps, pred_y, label='Predicted Data', color='red')

plt.xlabel('Time (Hourly)')
plt.ylabel('CO2 Output (Normalized)')
plt.title('LSTM CO2 Output Prediction with Time Axis')
plt.legend()
plt.xticks(rotation=45)  # 旋转 x 轴刻度，便于阅读
plt.tight_layout()  # 自动调整布局防止遮挡
plt.show()
