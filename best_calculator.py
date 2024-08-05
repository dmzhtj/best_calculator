import easygui as eg
from sympy import *
import sys
import numpy as np
import matplotlib.pyplot as plt

def classify_equation(equation_input):
    """
    对单个方程进行分类，判断其类型。
    :param equation_input: 用户输入的方程字符串
    :return: 方程类型和Sympy方程对象，若无法分类则返回None
    """
    try:
        left_side, right_side = equation_input.split('=')
        left_expr = sympify(left_side)
        right_expr = sympify(right_side)
        sympy_eq = Eq(left_expr, right_expr)
        
        # 判断方程类型
        if sympy_eq.lhs.is_polynomial():
            degree = sympy_eq.lhs.as_poly().degree()
            return {1: "线性方程", 2: "二次方程", 3: "三次方程"}.get(degree, "高次多项式方程"), sympy_eq
        elif any(func in sympy_eq.lhs.free_symbols for func in [sin, cos, exp, log]):
            return "超越方程", sympy_eq
        
        return "其他类型方程", sympy_eq
    except Exception as e:
        eg.exceptionbox(f"在处理方程时发生错误: {e}")

def solve_mixed_system(equations):
    """
    求解混合类型方程组。
    :param equations: 方程组列表
    :return: 方程组的解，若求解失败则返回空列表
    """
    try:
        eqs = []
        for eq in equations:
            eq_type, eq_obj = classify_equation(eq)
            if eq_type:
                eqs.append(eq_obj)
        
        variables = list(set(var for eq in eqs for var in eq.free_symbols))
        solutions = solve(eqs, variables, dict=True)
        return solutions or []  # 返回空列表而非None
    except Exception as e:
        eg.exceptionbox(f"在求解方程组时发生错误: {e}")

def calculate(expression):
    try:
        # 使用 sympy 库来处理复杂的数学表达式并返回结果
        return eval(expression)
    except Exception as e:
        eg.exceptionbox(f"输入错误: {e}")

def main():
    sys.set_int_max_str_digits(666666)
    while True:
        choice = eg.choicebox("请选择你要使用的功能", "功能选择", ["基本运算","解方程","开方", "绘制函数图像（线性）","历史记录","删除历史记录","退出"])

        if choice == "基本运算":
            while True:
                try:
                    expression = eg.enterbox("请输入表达式（例如：1 + 2 * (3 - 4) / 5 ** 2），ps：乘号是*，除号是/，乘方是**，点击'cancel'退出", "基本运算")
                    if expression is None or expression.strip() == '':
                        if eg.buttonbox("退出基本运算？", "退出", ["是", "否"]) == "是":
                            break
                        continue
                    
                    result = calculate(expression)
                    eg.textbox(f"结果是（结果太长会死机，请打开calculator_history.cht文件查看）：", "结果",str(result))
                    f = open("calculator_history.cht", "a")
                    f.write(expression + "=" + str(result)+"\n")
                    f.close()
                except:
                    eg.exceptionbox("有错误发生了，请输入有效的数字。")


        elif choice == "解方程":
            while True:
                try:
                    n = int(eg.enterbox("说说你有几个方程吧~（请输入数字）", "方程个数"))
                    equations_input = [eg.enterbox(f"请输入第 {i + 1} 个方程: ", "方程输入") for i in range(n)]
                    
                    solutions = solve_mixed_system(equations_input)
                    
                    # 输出方程类型和解
                    eq_types_info = [f"方程 {i + 1} 类型: {classify_equation(eq)[0]}" for i, eq in enumerate(equations_input)]
                    solutions_info = [", ".join(f"{var} = {sol[var]}" for var in sol) for sol in solutions]
                    
                    eq_types_str = "\n".join(eq_types_info)
                    solutions_str = "\n".join(solutions_info)

                    eg.textbox("解方程结果：","解方程",f"方程类型:\n{eq_types_str}\n\n方程组的解:\n{solutions_str}")
                    with open("calculator_history.cht", "a") as f:
                        f.write("方程：" + "，".join(equations_input) + "；"+"方程组的解：" + "，".join(solutions_info) + "\n")
                except ValueError:
                    eg.exceptionbox("有错误发生了，请输入有效的数字。")
                except Exception as e:
                    if str(e) == "int() argument must be a string, a bytes-like object or a real number, not 'NoneType'":
                        if eg.buttonbox("确定要退出解方程吗？", "退出确认", ["是", "否"]) == "是":
                            break
                    else:
                        eg.exceptionbox(f"发生错误: {e}")

        elif choice == "开方":
            try:
                number = float(eg.enterbox("请输入你要开方的数:", "开方"))
                root = float(eg.enterbox("请输入你要开几次方:", "开几次方"))
                result = pow(number, 1/root)
                eg.textbox("开放结果：", "开方结果", f"{result}")
                f = open("calculator_history.cht", "a")
                f.write("开方："+str(number)+"；"+"开几次方："+str(root)+"；"+"开方结果为："+str(result)+"\n")
                f.close()
            except ValueError:
                eg.exceptionbox("输入错误，请输入有效的数字。")

        elif choice == "绘制函数图像（线性）":
            x = np.linspace(-10, 10, 100)  # 定义x轴上的数据点
            try:
                k = float(eg.enterbox("请输入你要绘制的线性函数的k（格式为y=kx+b）：", "线性函数图像"))
                b = float(eg.enterbox("请输入你要绘制的线性函数的b（格式为y=kx+b）：", "线性函数图像"))
            except ValueError:
                eg.exceptionbox("输入错误，请输入有效的数字。")
                continue
            y = k*x+b
            plt.plot(x, y)  # 绘制函数图像
            plt.title('Linear Function Graph')  # 添加标题
            plt.xlabel('x')  # 添加x轴标签
            plt.ylabel('y')  # 添加y轴标签

            plt.show()  # 显示图像
        elif choice == "历史记录":
            try:
                f = open("calculator_history.cht", "r")
                eg.textbox("历史纪录如下：(超过十位，历史记录会死机，请打开calculator_history.cht文件查看)", "历史记录", f.read())
                f.close()
            except:
                eg.exceptionbox("历史记录出问题啦~(也能是没有。。。)")
        else:
            if eg.buttonbox("确定要退出吗？", "退出确认", ["是", "否"]) == "是":
                break

if __name__ == '__main__':
    main()

