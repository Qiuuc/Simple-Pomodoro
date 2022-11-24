import sys
import time
import tkinter
import tkinter.messagebox
import Pomo
import os

if __name__ == '__main__':
    # ini、ico配置文件检测
    Pomo.ini_check()
    # 实例化Pomo.PCount类
    tomato = Pomo.PCount()
    # 界面初始化
    window = tkinter.Tk()
    window.title("Pomodoro")
    width = 250
    height = 350
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    window.geometry('%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2))
    # 设置窗口不可缩放
    window.resizable(width=False, height=False)
    window.iconbitmap(os.getenv('APPDATA') + "\\TomatoIni\\tomato.ico")

    # 累计时长
    total_count = tomato.total_time
    # 默认计时时间
    default_time = tomato.default_time
    # 计时显示变量，初始值为default_time
    time_var = tkinter.StringVar()
    time_var.set(Pomo.time2txt(default_time))
    # 设置初始计时状态为关闭
    on_running = False
    # 一些初始值
    current_total = 0.0
    start_time = 0
    timer = None


    def update():
        global on_running
        global current_total
        global time_var
        global timer
        # 计算经过时长
        current_total = int(time.time() - start_time)
        tmp_time = default_time - current_total
        # 检测时间是否为0
        if tmp_time == 0:
            stop()
            tkinter.messagebox.showinfo(title="恭喜！", message="时间到！休息一下吧~")
        # 正常执行
        else:
            # 打印时间
            time_var.set(Pomo.time2txt(tmp_time))
            # 50微秒执行一次update函数，实现update计时循环
            timer = window.after(50, update)

    # 检测输入正确与否
    def pre_start():
        global default_time
        try:
            if text_entry.get() == "":
                start()
            # 存了浮点数的字符串不能直接转换为int，强行转换并判断范围会报Value错误
            elif 0 < int((text_entry.get())) <= 60:
                default_time = int((text_entry.get()))*60
                time_var.set(Pomo.time2txt(default_time))
                start()
            else:
                tkinter.messagebox.showwarning(title="输入错误", message="请输入0-61之间的整数哦。")
                sys.exit()
        except ValueError:
            tkinter.messagebox.showwarning(title="输入错误", message="请输入0-61之间的整数哦。")
            sys.exit()


    def start():
        global on_running
        global start_time
        global default_time
        if not on_running:
            # 更改按钮，并使command指向stop()
            change_button.configure(text="结束", command=stop)
            # 设置计时开始时间
            start_time = time.time()
            # 更改计时状态为开
            on_running = True
            update()


    def stop():
        global current_total
        global on_running
        global timer
        global total_count
        global start_time
        if on_running:
            # 更改按钮，并使command指向pre_start()
            change_button.configure(text="开始", command=pre_start)
            # 停止after函数
            window.after_cancel(str(timer))
            # 计算番茄时间
            current_total = int(time.time() - start_time)
            total_count += current_total
            # 计算总番茄时间，并传入ini文件
            tomato.total_time = total_count
            tomato.update_ini()
            # 更改总番茄时间显示
            total_time.configure(text=Pomo.time2txt2(total_count))
            # 番茄钟初始化
            current_total = 0
            start_time = 0
            # 显示时间为设置的时间
            time_var.set(Pomo.time2txt(default_time))
            # 计时状态调为关闭
            on_running = False


    # 标题
    title_label = tkinter.Label(window, text="简单番茄钟", font=('宋体', 32))
    title_label.place(x=15, y=0, anchor='nw')
    # 计时显示
    time_label = tkinter.Label(window, textvariable=time_var, font=("微软雅黑", 48))
    time_label.place(x=40, y=55, anchor='nw')
    # 设定时间
    title4_label = tkinter.Label(window, text="设置时间:", font=('宋体', 15))
    title4_label.place(x=10, y=160, anchor='nw')
    text_entry = tkinter.Entry(window, font=('宋体', 15), width=6)
    text_entry.place(x=116, y=162, anchor='nw')
    title5_label = tkinter.Label(window, text="分钟", font=('宋体', 15))
    title5_label.place(x=185, y=160, anchor='nw')
    # 按钮
    change_button = tkinter.Button(window, text="开始", font=('宋体', 16), command=pre_start)
    change_button.place(x=95, y=230, anchor='nw')
    # 总时长
    title2_label = tkinter.Label(window, text="累计番茄: ", font=('宋体', 15))
    title2_label.place(x=10, y=300, anchor='nw')
    total_time = tkinter.Label(window, text=Pomo.time2txt2(total_count), font=('宋体', 15))
    total_time.place(x=115, y=300, anchor='nw')

    try:
        window.mainloop()
    except KeyboardInterrupt:
        sys.exit()
