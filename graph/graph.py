import tkinter as tk
import easygui as eg
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re

# 设置matplotlib以使用支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号'-'显示为方块的问题

def plot_functions():
    def draw_plot():
        functions_str = function_entry.get("1.0", tk.END).strip()

        # 清空之前的图形
        for widget in frame.winfo_children():
            widget.destroy()

        # 创建Matplotlib图形
        fig = plt.figure()
        ax = fig.add_subplot(111)  # 仅创建2D子图

        try:
            # 按行分割函数表达式
            functions = functions_str.splitlines()

            labels = []  # 用于存储艺术家的标签
            for func_str in functions:
                func_str = func_str.strip()
                if not func_str:
                    continue

                # 提取函数的左侧和右侧
                match = re.match(r"y\s*=\s*(.*)", func_str)
                if match:
                    expression = match.group(1)
                    x = np.linspace(-10, 10, 100)
                    y = eval(expression, {'__builtins__': None}, {'x': x})
                    line, = ax.plot(x, y, label=expression)  # 指定标签为函数表达式
                    labels.append(line.get_label())  # 将标签添加到列表中

            if labels:  # 如果有艺术家具有标签，则生成图例
                ax.legend()
            else:
                ax.set_title('2D函数图像')  # 如果没有艺术家具有标签，则不生成图例

            ax.grid(True)
            ax.set_xlabel('X轴')
            ax.set_ylabel('Y轴')

        except Exception as e:
            eg.exceptionbox("输入的表达式有误，请重新输入。\错误信息：{str(e)}")

        # 将Matplotlib图形嵌入到Tkinter窗口中
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # 创建Tkinter窗口
    root = tk.Tk()
    root.title("绘制函数图像")

    # 创建顶层框架
    frame = tk.Frame(root)
    frame.pack(expand=True, fill=tk.BOTH)

    # 创建函数输入框
    function_label = tk.Label(frame, text="请输入函数表达式(每行一个，例如 y = x**2)：")
    function_label.pack(pady=10)
    function_entry = tk.Text(frame, width=50, height=10)
    function_entry.pack(pady=10)

    # 创建绘制按钮
    draw_button = tk.Button(frame, text="绘制图像", command=draw_plot)
    draw_button.pack(pady=10)

    root.mainloop()

def plot_3d_function():
    try:
        # 获取用户输入的函数表达式
        func_expr = eg.enterbox("请输入一个函数表达式（例如：Z = X**2 + Y**2）：")

        # 确保输入的表达式包含'Z ='
        if not func_expr.startswith('Z ='):
            eg.msgbox("函数表达式必须以'Z ='开头。")
            return

        # 解析函数表达式以获取Z的表达式
        z_expr = func_expr[3:].strip()

        plt.figure()
        ax = plt.axes(projection="3d")

        x = np.arange(-5, 5, 0.1)
        y = np.arange(-5, 5, 0.1)
        X, Y = np.meshgrid(x, y)  # 生成绘制3D图形所需的网络数据

        # 使用用户输入的表达式计算Z值
        Z = eval(z_expr, {'X': X, 'Y': Y})

        ax.plot_surface(X, Y, Z, alpha=0.5, cmap="winter")  # 生成表面，alpha用于控制透明度
        ax.set_xlabel("X")  # 设置X、Y、Z 坐标范围
        ax.set_xlim(-6, 6)   # 设置X、Y、Z 轴
        ax.set_ylabel("Y")
        ax.set_ylim(-6, 6)
        ax.set_zlabel("Z")
        plt.show()
    
    except Exception as e:
        eg.exceptionbox("出错啦！\错误信息：{str(e)}")

def main():
    while True:
        choice = eg.buttonbox("请选择您要进行的操作：", choices=["绘制2D函数图像", "绘制3D函数图像", "退出"])
        if choice == "绘制3D函数图像":
            plot_3d_function()
        elif choice == "绘制2D函数图像":
            plot_functions()
        else:
            inpt = eg.buttonbox("确定要退出吗？", title="退出", choices=["是", "否"])
            if inpt == "是":
                break

if __name__ == "__main__":
    main()
