import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 读取数据并设置索引
data = pd.read_csv(
    r"D:\Project-forecast\carbon\testdata\air-quality-data.csv",
    index_col="Date",  # 设置时间为索引
    parse_dates=['Date']  # 解析时间戳
)

# 数据清理：筛选合理范围
data = data[(data['PT08.S1(CO)'] > 750) & (data['PT08.S1(CO)'] < 1800)]

# 确保索引去重
data = data[~data.index.duplicated(keep='first')]

# 只保留日期（去掉具体时间）
data.index = data.index.normalize()

# 统一时间频率并填充缺失值
data = data.asfreq('D').interpolate()

# 提取输出列并归一化
output = data['PT08.S1(CO)']
max_output = max(output)
output_norm = output / max_output

# 定义时间步
def extract_data(data, time_step):
    x, y = [], []
    for i in range(len(data) - time_step):
        x.append([a for a in data[i:i + time_step]])
        y.append(data[i + time_step])
    x = np.array(x).reshape(len(x), time_step, 1)  # 调整形状
    y = np.array(y)
    return x, y

time_step = 5
x, y = extract_data(output_norm, time_step)

# 转换为Tensor
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
x = torch.tensor(x, dtype=torch.float32).to(device)
y = torch.tensor(y, dtype=torch.float32).to(device)

# 训练测试集划分
train_size = int(len(x) * 0.8)
train_x, test_x = x[:train_size], x[train_size:]
train_y, test_y = y[:train_size], y[train_size:]

# 训练和测试时间戳
train_timestamps = data.index[:train_size + time_step]
test_timestamps = data.index[train_size + time_step:train_size + time_step + len(test_y)]

# 数据加载器
train_loader = DataLoader(TensorDataset(train_x, train_y), batch_size=64, shuffle=True)

# 定义 LSTM 模型
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
        return self.fc(out[:, -1, :])

# 超参数
input_size = 1
hidden_size = 32
num_layers = 2
output_size = 1
learning_rate = 0.005
epochs = 100

# 实例化模型
model = LSTM(input_size, hidden_size, num_layers, output_size).to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# 训练模型
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

# 预测
model.eval()
with torch.no_grad():
    pred_y = model(test_x).cpu().numpy()
    true_y = test_y.cpu().numpy()

# 反归一化
pred_y = pred_y * max_output
true_y = true_y * max_output

# 计算误差指标
mae = mean_absolute_error(true_y, pred_y)
rmse = mean_squared_error(true_y, pred_y, squared=False)
mape = (abs((true_y - pred_y) / true_y)).mean() * 100
r2 = r2_score(true_y, pred_y)

# 打印评估结果
print("\n=== 预测模型评估指标 ===")
print(f"MAE  = {mae:.4f}")
print(f"RMSE = {rmse:.4f}")
print(f"MAPE = {mape:.2f}%")
print(f"R²   = {r2:.4f}")

# 绘制预测结果
plt.figure(figsize=(12, 6))
plt.plot(data.index, output, label='Original Data')
plt.plot(test_timestamps, pred_y, label='Predicted Data', color='red')
plt.xlabel('Date')
plt.ylabel('CO2 Output')
plt.title('LSTM')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
