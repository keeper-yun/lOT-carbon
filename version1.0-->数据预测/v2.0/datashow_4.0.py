

from flask import Flask, send_file
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller as ADF
import io

# Flask 应用
app = Flask(__name__)

# 数据处理和预测绘图功能
def generate_plot(i):
    # 读取数据
    data_df = pd.read_csv(
        fr"D:\Project-forecast\carbon\v2.0\factory{i}.csv",
        index_col="timestamp",
        parse_dates=['timestamp']  # 将 'timestamp' 转为 DatetimeIndex
    )

    # 确保索引单调递增并设置频率
    data_df = data_df.sort_index()
    data_df.index.freq = pd.infer_freq(data_df.index)  # 自动推断频率

    df = pd.read_csv(fr"D:\Project-forecast\carbon\v2.0\factory{i}.csv")

    # 数据切片
    sub = data_df.loc[ str(df.loc[df.index.min() ,'timestamp']) : str(df.loc[df.index.max() ,'timestamp']) ]

    # 提取训练集和测试集
    train = sub.loc[ str(df.loc[df.index.min() ,'timestamp']) : str(df.loc[df.index.max()-3 ,'timestamp']) ]['co2_Output']
    test = sub.loc[ str(df.loc[df.index.max()-2 ,'timestamp']) : str(df.loc[df.index.max() ,'timestamp']) ]['co2_Output']

    # 拟合 ARIMA 模型
    p, d, q = 1, 1, 0
    model = sm.tsa.ARIMA(train, order=(p, d, q))
    results = model.fit()

    # 预测测试集
    history = list(train.values)
    forecast = []
    for t in range(len(test.values)):
        model = sm.tsa.ARIMA(history, order=(p, d, q))
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        forecast.append(yhat)
        obs = test[t]
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


# Flask 路由返回图像
@app.route('/predict/<int:i>', methods=['GET'])
def plot(i):
    try:
        buf = generate_plot(i)
        return send_file(buf, mimetype='image/png')
    except FileNotFoundError:
        return f"Factory {i} data not found!", 404
    except Exception as e:
        return f"Error: {str(e)}", 500


# 运行 Flask 应用
if __name__ == '__main__':
    app.run(debug=True)
