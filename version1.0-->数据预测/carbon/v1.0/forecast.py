

import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams
from flask import Flask, send_file, jsonify
import io

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

# print("工厂A CO2,N2O,CH4浓度:")
# print(data_co2_A)
# print(data_n2o_A)
# print(data_ch4_A)
# print("工厂B CO2,N2O,CH4浓度:")
# print(data_co2_B)
# print(data_n2o_B)
# print(data_ch4_B)
# print("工厂C CO2,N2O,CH4浓度:")
# print(data_co2_C)
# print(data_n2o_C)
# print(data_ch4_C)
# print("工厂D CO2,N2O,CH4浓度:")
# print(data_co2_D)
# print(data_n2o_D)
# print(data_ch4_D)



# 数据准备
data_dict = {
    "A": {"co2": data_co2_A, "n2o": data_n2o_A, "ch4": data_ch4_A},
    "B": {"co2": data_co2_B, "n2o": data_n2o_B, "ch4": data_ch4_B},
    "C": {"co2": data_co2_C, "n2o": data_n2o_C, "ch4": data_ch4_C},
    "D": {"co2": data_co2_D, "n2o": data_n2o_D, "ch4": data_ch4_D}
}
print()
#
#
#
# # 绘制每个工厂的CO2、N2O、CH4浓度
# # for factory, gases in data_dict.items():
# #     plt.figure(figsize=(12, 6))
# #     plt.plot(gases["co2"], label="CO2", color='r')
# #     plt.plot(gases["n2o"], label="N2O", color='g')
# #     plt.plot(gases["ch4"], label="CH4", color='b')
# #     plt.title(f"工厂{factory}")
# #     plt.xlabel("时间 (小时)")
# #     plt.ylabel("浓度")
# #     plt.legend()
# #     plt.grid(True)
# #     plt.show()
#
#
#
# # 创建并返回图像的方法
# def create_chart(factory, gases):
#     img_buf = io.BytesIO()  # 创建一个字节流（Memory buffer）
#
#     # 绘制该工厂的 CO2、N2O 和 CH4 浓度
#     plt.figure(figsize=(12, 6))
#     plt.plot(gases["co2"], label="CO2", color='r')
#     plt.plot(gases["n2o"], label="N2O", color='g')
#     plt.plot(gases["ch4"], label="CH4", color='b')
#
#     # 设置标题和标签
#     plt.title(f"工厂{factory}")
#     plt.xlabel("时间 (小时)")
#     plt.ylabel("浓度")
#     plt.legend()
#     plt.grid(True)
#
#     # 保存图像到字节流
#     plt.savefig(img_buf, format='png')
#     img_buf.seek(0)  # 重置指针位置
#
#     return img_buf
#
# # 每个工厂独立的图像路由
# @app.route('/data_A', methods=['GET'])
# def get_chart_A():
#     img_buf = create_chart("A", data_dict["A"])
#     return send_file(img_buf, mimetype='image/png')
#
# @app.route('/data_B', methods=['GET'])
# def get_chart_B():
#     img_buf = create_chart("B", data_dict["B"])
#     return send_file(img_buf, mimetype='image/png')
#
# @app.route('/data_C', methods=['GET'])
# def get_chart_C():
#     img_buf = create_chart("C", data_dict["C"])
#     return send_file(img_buf, mimetype='image/png')
#
# @app.route('/data_D', methods=['GET'])
# def get_chart_D():
#     img_buf = create_chart("D", data_dict["D"])
#     return send_file(img_buf, mimetype='image/png')
#
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
#
#
# # -------------------------------------------------------


