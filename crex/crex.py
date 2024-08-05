#“头文件”
import random
import easygui as e
import haha.haha as haha

#加密函数
def encrypt_text():
    try:

        text = e.enterbox("请输入明文：","输入明文")

        code_points = [ord(char) for char in text]

        while True:
            try:
                passwd = int(e.enterbox("请输入密码（1-2位数字）（若出现方块，可调小密码😀）：","输入密码"))
                if 0 < passwd < 100:
                    break
                else:
                    print("密码必须为1-2位数字")
            except ValueError:
                print("密码必须为1-2位数字")

        encrypted_code_points = [code + passwd for code in code_points]

        encrypted_text = ''.join(chr(code) for code in encrypted_code_points)
        e.msgbox(msg="加密后的文本（Ctrl+C复制）：\n" + encrypted_text,title="密文")
    except:
        e.exceptionbox("啊哟，出错啦。","出错啦")

#解密函数
def decrypt_text():

    text=e.enterbox("请输入密文：","输入明文")

    while True:

        try:
            passwd = int(e.enterbox("请输入密码：","输入密码"))
            if 0 < passwd < 100:
                break
            else:
                e.msgbox("密码必须为1-2位数字","出错啦")
        except ValueError:
            e.msgbox("啊哟，出错啦。","出错啦")

    code_points = [ord(char) for char in text]
    encrypted_code_points = [code - passwd for code in code_points]
    encrypted_text = ''.join(chr(code) for code in encrypted_code_points)

    e.msgbox(msg='解密后的文本（Ctrl+C复制）：' + encrypted_text,title="明文")
    #by 辞.

#生成随机密码函数
def generate_password():

    passwd = random.randint(1,99)
    e.msgbox("随机密码为（若出现方块，可重新生成😀）："+str(passwd),"随机密码")
    inpt = e.buttonbox("是否直接用于生成密文？","生成密文",("好","不要"))

    if inpt == "好":
        
        text = e.enterbox("请输入明文中文文本：","明文")

        code_points = [ord(char) for char in text]

        while True:
            try:
                if 0 < passwd < 100:
                    break
                else:
                    e.msgbox("密码必须为1-2位数字","出错啦")
            except ValueError:
                e.msgbox("密码必须为1-2位数字","出错啦")

        encrypted_code_points = [code + passwd for code in code_points]

        encrypted_text = ''.join(chr(code) for code in encrypted_code_points)
        e.msgbox(msg="加密后的文本：" + encrypted_text,title="密文")
    elif inpt == "不要":
        pass
    else:
        pass

#主函数
def main():  

        inppt = e.buttonbox("警告：这只是一个编码器，开发者对任何安全问题不负责。","警告",("OK","不想用了"))

        if inppt == "OK":

            while 666:

                selected_option = e.buttonbox("请选择：","选择",("加密","解密","生成密码","不要点我","退出"))

                if selected_option == "加密":
                    encrypt_text()

                elif selected_option == "解密":
                    decrypt_text()

                elif selected_option == "生成密码":
                    generate_password()
                    
                elif selected_option == "不要点我":
                    haha.main()

                else:
                    if e.buttonbox("确定要退出吗？", "退出确认", ["是", "否"]) == "是":
                        break
                    else:
                        continue
        else:
            if e.buttonbox("确定要退出吗？", "退出确认", ["是", "否"]) == "是":
                pass
            else:
                main()

if __name__ == "__main__":
    
    main()
