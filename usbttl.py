#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import serial
import serial.tools.list_ports
from tkinter import messagebox
import time

window = tk.Tk()


# window.iconbitmap('@./logo.ico')
sw = window.winfo_screenwidth()
sh = window.winfo_screenheight()
ww = 800
wh = 490
x = (sw-ww) / 2
y = (sh-wh) / 2
# window.geometry('800x500')
window.geometry("%dx%d+%d+%d" %(ww,wh,x,y))

window.resizable(width=False, height=False)
window.title('串口调试')
#window.call('wm', 'iconphoto', window._w, tk.PhotoImage(file='./logo.png'))


# 面板1 左侧
fm1 = tk.Frame()
# fm1.pack(side='left', fill='both', expand='yes')
fm1.place(width=200,height=500,x=10,y=10)

# 面板2 右侧
fm2 = tk.Frame()
# fm2.pack(side='left', padx=10,fill='both',expand='yes')
fm2.place(width=600,height=500,x=220,y=10)

# 串口名称
comname = tk.StringVar()
# 波特率
buad = tk.IntVar()
# 串口开关的文本
button_switch_text = tk.StringVar()
button_switch_text.set('closed')
# 串口状态
is_open=tk.BooleanVar()
is_open.set(False)
# 发送按钮的文本
button_send_text = tk.StringVar()
button_send_text.set('发送')

# tx,rx
tx_text = tk.StringVar()
rx_text = tk.StringVar()

# 事件
# 发送

def send():
    try:
        ser.write((tx_text.get()+'\r\n').encode('utf8'))
    except Exception as err:
        messagebox.showerror('发送数据 失败',err)
        print(err)
    else:
        tx_text.set("")
    # rx.insert(tk.END,tx_text.get())

# 串口按钮事件
def switch():
    if is_open.get():
        button_switch_text.set('closed')
        button_switch.configure(bg = "red")
        is_open.set(False)
    else:
        print('COM:{},buad:{}'.format(comname.get(),buad.get()))
        try:
            global ser
            ser=serial.Serial(comname.get(),buad.get(),timeout=5000)
        except Exception as err:                                 
            messagebox.showerror('打开串口失败',err)
            print(err)
        else:
            button_switch_text.set('opened')
            button_switch.configure(bg = "green")
            is_open.set(True)

# 定时器
def clock():
    t=time.strftime('%I:%M:%S',time.localtime())
    if t!='':
        # label1.config(text=t,font='times 25')
        # 获得串口输入
        try:
            num = ser.inWaiting()
        except:
            print('none data')
        else:
            if num > 0:
                data = ser.read(num)
                # print( type(data))
                # rx.insert(tk.END,tx_text.get()+'\r\n')
                text = str(data, encoding = "utf8")  
                rx.insert(tk.END,text+'\r\n')
                rx.see(tk.END)
        print('time')
    window.after(100,clock)

# 标签文字
tk.Label(fm1,text='串口选择',justify='left').place(width=50,height=30,x=0,y=10) 

# 串口列表

ports = serial.tools.list_ports.comports()
port_list=[]
for port, desc, hwid in sorted(ports):
    port_list.append(port)
    print("{}: {} [{}]".format(port, desc, hwid))

# port_list = list(serial.tools.list_ports.comports())
# print(port_list)
com_list = ttk.Combobox(fm1,textvariable=comname,state='readonly')
com_list.grid(column=1,row=1)
com_list['values']=port_list
if len(port_list) == 0:
    print('没有串口')
    messagebox.showerror('错误','没有串口')
else:
    com_list.current(0)
com_list.place(width=130,height=30,x=70,y=10)

# 标签文字
tk.Label(fm1,text='速度选择',justify='left').place(width=50,height=30,x=0,y=50) 

# 波特率列表
baud_list = ttk.Combobox(fm1,textvariable=buad,state='readonly')
baud_list.grid(column=1,row=1)
baud_list['values']=('9600','19200','115200')
baud_list.current(0)
baud_list.place(width=130,height=30,x=70,y=50)

# 标签文字
tk.Label(fm1,text='串口状态',justify='left').place(width=50,height=30,x=0,y=90) 
# 串口开关
button_switch = tk.Button(fm1, 
    textvariable=button_switch_text,
    width=15, height=2, 
    bg='red',
    command=switch)
button_switch.place(width=130,height=30,x=70,y=90)

# e = tk.Entry(window, show='*') #输入框，输入时显示*

# 标签文字
tk.Label(fm2,text='收到内容',justify='left').place(width=50,height=30,x=10,y=10) 
# 读串口文本框
# rx = tk.Entry(fm2,textvariable=rx_text,font='large_font')
# rx.place(width=480,height=200,x=80,y=10)
rx = scrolledtext.ScrolledText(fm2,wrap=tk.WORD)
rx.place(width=480,height=400,x=80,y=10)

# 标签文字
tk.Label(fm2,text='输入内容').place(width=50,height=30,x=10,y=420) 
# 写串口文本框
# tx = tk.Entry(fm2)
tx = tk.Entry(fm2,width=50,textvariable=tx_text)
# tx = tk.Text(fm2,width=50,height=10,textvariable=tx_text)
tx.place(width=390,height=40,x=80,y=420)

# 发送按钮
button_send = tk.Button(fm2, 
    textvariable=button_send_text,
    width=15, height=2, 
    command=send)
button_send.place(width=80,height=40,x=480,y=420)

clock() # 执行定时器
window.mainloop()
