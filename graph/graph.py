import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sympy as sp
import re

# 设置matplotlib以使用支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号'-'显示为方块的问题

def main():
    def draw_plot():
        plot_type = plot_type_var.get()
        functions_str = function_entry.get("1.0", tk.END).strip()

        # 清空之前的图形
        for widget in plot_frame.winfo_children():
            widget.destroy()

        # 创建Matplotlib图形
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d' if plot_type == "3D" else None)

        try:
            functions = functions_str.splitlines()
            
            if plot_type == "2D":
                for func_str in functions:
                    func_str = func_str.strip()
                    if not func_str:
                        continue
                    match = re.match(r"y\s*=\s*(.*)", func_str)
                    if match:
                        expression = match.group(1)
                        x = np.linspace(-10, 10, 100)
                        y = eval(expression, {'__builtins__': None}, {'x': x})
                        ax.plot(x, y, label=expression)

                ax.grid(True)
                ax.legend()
                ax.set_xlabel('X轴')
                ax.set_ylabel('Y轴')
                ax.set_title('2D函数图像')

            elif plot_type == "3D":
                x = np.arange(-5, 5, 0.1)
                y = np.arange(-5, 5, 0.1)
                X, Y = np.meshgrid(x, y)

                for func_str in functions:
                    func_str = func_str.strip()
                    if not func_str:
                        continue
                    match = re.match(r"z\s*=\s*(.*)", func_str)
                    if match:
                        z_expr = match.group(1)
                        z_sympy = sp.sympify(z_expr)
                        Z = sp.lambdify((sp.symbols('x y')), z_sympy)(X, Y)
                        if Z.ndim != 2:
                            raise ValueError(f"函数表达式 '{z_expr}' 计算结果 Z 的维度不符合要求。")
                        ax.plot_surface(X, Y, Z, alpha=0.5, cmap="winter")

                ax.set_xlabel("x")
                ax.set_ylabel("y")
                ax.set_zlabel("z")
                ax.set_title("3D 函数图像")

        except Exception as e:
            ax.text(0.5, 0.5, f"错误：{e}", ha='center', va='center', transform=ax.transAxes)

        # 将Matplotlib图形嵌入到Tkinter窗口中
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # 创建主窗口
    root = tk.Tk()
    root.title("函数图像绘制")

    # 创建顶层框架
    main_frame = ttk.Frame(root, padding="3")
    main_frame.pack(expand=True, fill=tk.BOTH)

    # 输入函数表达式
    function_label = ttk.Label(main_frame, text="请输入函数表达式（每行一个）:")
    function_label.pack(pady=10)
    function_entry = scrolledtext.ScrolledText(main_frame, width=60, height=10)
    function_entry.pack(pady=10)

    # 绘图类型选择
    plot_type_var = tk.StringVar(value="2D")
    plot_type_label = ttk.Label(main_frame, text="请选择绘制类型：")
    plot_type_label.pack(pady=10)
    plot_type_2d = ttk.Radiobutton(main_frame, text="2D", variable=plot_type_var, value="2D")
    plot_type_2d.pack(anchor=tk.W)
    plot_type_3d = ttk.Radiobutton(main_frame, text="3D", variable=plot_type_var, value="3D")
    plot_type_3d.pack(anchor=tk.W)

    # 绘图按钮
    plot_button = ttk.Button(main_frame, text="绘制图像", command=draw_plot)
    plot_button.pack(pady=10)

    # 图形绘制区域
    plot_frame = ttk.Frame(main_frame)
    plot_frame.pack(expand=True, fill=tk.BOTH)

    # 运行主循环
    root.mainloop()
if __name__ == "__main__": 
    main()
