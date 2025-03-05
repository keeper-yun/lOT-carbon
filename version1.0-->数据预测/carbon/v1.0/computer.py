#
#
# while 1:
#
#     ppm,ppb,ppmj,speed = eval(input("输入CO2,N2O,CH4,流速 值分别是多少?"))
#
#     if ppm == ppb == ppmj == speed == 0:
#         break
#
#     ppm = ppm * speed * 1.183
#     ppb = ppb * speed * 0.044
#     ppmj = ppmj * speed * 0.717
#     print(f"co2_output:{ppm} ,n2o_output:{ppb} ,ch4_output:{ppmj}")
#


import tkinter as tk

def calculate():
    try:
        ppm = float(ppm_entry.get())
        ppb = float(ppb_entry.get())
        ppmj = float(ppmj_entry.get())
        speed = float(speed_entry.get())

        if ppm == ppb == ppmj == speed == 0:
            result_label.config(text="输入值不能全为零")
            return

        # 计算输出
        ppm_output = round(ppm * speed * 1.183, 2)
        ppb_output = round(ppb * speed * 0.044, 2)
        ppmj_output = round(ppmj * speed * 0.717, 2)

        # 显示结果
        result_label.config(text=f"CO2 输出: {ppm_output} , N2O 输出: {ppb_output} , CH4 输出: {ppmj_output}")
    except ValueError:
        result_label.config(text="请输入有效的数字")

# 创建主窗口
root = tk.Tk()
root.title("气体浓度计算器")

# 创建标签和输入框
ppm_label = tk.Label(root, text="CO2 浓度 (ppm):")
ppm_label.grid(row=0, column=0, padx=10, pady=5)
ppm_entry = tk.Entry(root)
ppm_entry.grid(row=0, column=1, padx=10, pady=5)

ppb_label = tk.Label(root, text="N2O 浓度 (ppb):")
ppb_label.grid(row=1, column=0, padx=10, pady=5)
ppb_entry = tk.Entry(root)
ppb_entry.grid(row=1, column=1, padx=10, pady=5)

ppmj_label = tk.Label(root, text="CH4 浓度 (ppm):")
ppmj_label.grid(row=2, column=0, padx=10, pady=5)
ppmj_entry = tk.Entry(root)
ppmj_entry.grid(row=2, column=1, padx=10, pady=5)

speed_label = tk.Label(root, text="流速 (单位: m/s):")
speed_label.grid(row=3, column=0, padx=10, pady=5)
speed_entry = tk.Entry(root)
speed_entry.grid(row=3, column=1, padx=10, pady=5)

# 计算按钮
calculate_button = tk.Button(root, text="计算", command=calculate)
calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

# 显示结果的标签
result_label = tk.Label(root, text="")
result_label.grid(row=5, column=0, columnspan=2, pady=10)

# 启动主循环
root.mainloop()
