

import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams
from flask import Flask, send_file
import io
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score




app = Flask(__name__)


rcParams['font.sans-serif'] = ['Microsoft YaHei']  # Windows下使用“Microsoft YaHei”
rcParams['axes.unicode_minus'] = False

headers = {
    'User-Agent': ')Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0\
     Safari/537.36 Edg/120.0.0.0'
}
factory = ["A","B","C","D"]
data_co2_A = []
data_co2_B = []
data_co2_C = []
data_co2_D = []
data_n2o_A = []
data_n2o_B = []
data_n2o_C = []
data_n2o_D = []
data_ch4_A = []
data_ch4_B = []
data_ch4_C = []
data_ch4_D = []
url = f'http://localhost:8181/monitoring/findAll'
req = requests.get(url, headers=headers).text


data = json.loads(req)

for i in data:
    if i["factoryName"] == "工厂A":
        data_co2_A.append(i["co2_Level"])
        data_n2o_A.append(i["n2o_Output"])
        data_ch4_A.append(i["ch4_Output"])

    if i["factoryName"] == "工厂B":
        data_co2_B.append(i["co2_Level"])
        data_n2o_B.append(i["n2o_Output"])
        data_ch4_B.append(i["ch4_Output"])

    if i["factoryName"] == "工厂C":
        data_co2_C.append(i["co2_Level"])
        data_n2o_C.append(i["n2o_Output"])
        data_ch4_C.append(i["ch4_Output"])

    if i["factoryName"] == "工厂D":
        data_co2_D.append(i["co2_Level"])
        data_n2o_D.append(i["n2o_Output"])
        data_ch4_D.append(i["ch4_Output"])



# 数据准备
data_dict = {
    "A": {"co2": data_co2_A, "n2o": data_n2o_A, "ch4": data_ch4_A},
    "B": {"co2": data_co2_B, "n2o": data_n2o_B, "ch4": data_ch4_B},
    "C": {"co2": data_co2_C, "n2o": data_n2o_C, "ch4": data_ch4_C},
    "D": {"co2": data_co2_D, "n2o": data_n2o_D, "ch4": data_ch4_D}
}


# 拆分数据为训练集和测试集
def train_test_split(data, train_size=0.8):
    """
    将数据分为训练集和测试集
    :param data: 输入的历史数据
    :param train_size: 训练集的比例（默认80%）
    :return: 训练集和测试集
    """
    split_point = int(len(data) * train_size)
    return data[:split_point], data[split_point:]


# 计算预测误差
def evaluate_forecast(actual, forecast):
    """
    计算预测误差，包括 MSE, RMSE, MAE 和 R²
    :param actual: 实际值
    :param forecast: 预测值
    :return: 各种评估指标
    """
    mse = mean_squared_error(actual, forecast)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(actual, forecast)
    r2 = r2_score(actual, forecast)
    return mse, rmse, mae, r2


# 数据预测函数
def forecast_data_with_evaluation(data, steps=2, train_size=0.8):
    """
    使用 ARIMA 模型对数据进行预测，并计算预测误差
    :param data: 输入的历史数据
    :param steps: 预测的步长，默认为100小时
    :param train_size: 训练集比例
    :return: 预测结果及误差评估
    """
    # 拆分训练集和测试集
    train_data, test_data = train_test_split(data, train_size)

    # 使用训练集进行 ARIMA 模型训练
    model = ARIMA(train_data, order=(5, 1, 0))
    model_fit = model.fit()

    # 用测试集进行预测
    forecast = model_fit.forecast(steps=len(test_data))

    # 计算预测误差
    mse, rmse, mae, r2 = evaluate_forecast(test_data, forecast)

    return forecast, mse, rmse, mae, r2


# 示例：预测工厂A的 CO2 数据
forecast_A_co2, mse_A, rmse_A, mae_A, r2_A = forecast_data_with_evaluation(data_dict["A"]["co2"])
print(f"工厂A CO2预测误差评估:")
print(f"MSE: {mse_A}, RMSE: {rmse_A}, MAE: {mae_A}, R²: {r2_A}")
