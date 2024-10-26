# -*- coding: utf-8 -*-

import pandas as pd
from prophet import Prophet
import requests
import json
import matplotlib.pyplot as plt


headers = {
    'User-Agent': ')Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0\
     Safari/537.36 Edg/120.0.0.0'
}

listdata = []
url = f'http://localhost:8181/monitoring/findAll'
req = requests.get(url, headers=headers).text


data = json.loads(req)

for i in data:
    # print(i["co2_Level"])
    listdata.append(i["co2_Level"])
print(listdata)
# print(len(listdata))

# 创建示例数据
data = {
    'ds': pd.date_range(start='2024-10-24', periods=57, freq='D'),  # 日期
    'y': listdata        # CO2浓度
}

df = pd.DataFrame(data)

# print(df)
print("----------------")
model = Prophet(changepoint_prior_scale=0.01)

model.fit(df)

future = model.make_future_dataframe(periods=5)

forecast = model.predict(future)

print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])  # yhat 是预测值

show = model.plot(forecast)

# show2 = model.plot_components(forecast)

plt.show()

