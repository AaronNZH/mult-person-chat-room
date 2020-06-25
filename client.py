import socket
import threading
import sys

from tkinter import messagebox
from tkinter import *


def recv_data():  # 接收并显示服务端发送的信息
    global usr_name_list
    global txt_msglist
    while True:
        data = client.recv(1024).decode().split("&")
        tmp = data[1].split(" ")
        if len(tmp) == 3 and tmp[2] == "登录" and tmp[1] != usr:
            usr_name_list.append(tmp[1])
            user_listbox.delete(0, "end")
            for item in usr_name_list:
                user_listbox.insert("end", item)
        elif len(tmp) == 3 and tmp[2] == "退出":
            usr_name_list.remove(tmp[1])

        if data[0] == usr:
            txt_msglist.insert("end", data[1] + "\n", "usr")
        else:
            txt_msglist.insert("end", data[1] + "\n", "un-usr")

        print(data[1])


def login(username):
    global usr
    global back_message
    global usr_name_list
    global login_success
    global client

    client.connect(('127.0.0.1', 8088))
    client.send(username.encode())
    back_message = client.recv(1024).decode().split("&")
    messagebox.showinfo("服务器返回信息", back_message[0])
    if back_message[0] == "连接服务器成功~":
        login_success = True
        usr_name_list = ["在线用户："] + usr_name_list + back_message[1].split("|")
        usr = username
        top.destroy()
    else:
        client.close()
        client = socket.socket()


login_success = False
usr_name_list = []
usr = ""
back_message = ""
client = socket.socket()
top = Tk()
L1 = Label(top, text="请输入用户名").grid(row=0, sticky='W')
E1 = Entry(top, bd=5)
E1.grid(row=0, column=1, sticky='E')
B1 = Button(top, text="登录", command=lambda: login(E1.get()))
B1.grid(row=0, column=2)
top.mainloop()

if not login_success:
    sys.exit()

thread = threading.Thread(target=recv_data, daemon=True)
thread.start()


# 登录后摧毁原先的登录窗口，新建聊天室窗口
def msgsend():
    global usr
    global txt_msgsend

    msg = txt_msgsend.get('0.0', END)
    client.send(msg.encode())
    txt_msgsend.delete('0.0', END)  # 清空发送消息

def cancel():
    txt_msgsend.delete('0.0', END)  # 取消发送消息，即清空发送消息


root = Tk()
root.title('振华的聊天室')

# 聊天框
msg_list = Frame(height=320, width=500)
txt_msglist = Text(msg_list)  # 消息列表分区中创建文本控件
txt_msglist.tag_config("usr", foreground="green")
txt_msglist.tag_config("un-usr", foreground="black")
msg_list.grid(row=0, column=0)  # 消息列表分区
txt_msglist.grid()  # 消息列表文本控件加载
msg_list.grid_propagate(0)

# 编辑框
msg_send = Frame(height=150, width=500)
send_button = Frame(height=30, width=500)
txt_msgsend = Text(msg_send)  # 发送消息分区中创建文本控件
button_send = Button(send_button, text='Send', command=msgsend)  # 按钮分区中创建按钮并绑定发送消息函数
button_cancel = Button(send_button, text='Clear', command=cancel)  # 分区中创建取消按钮并绑定取消函数
msg_send.grid(row=1, column=0)  # 发送消息分区
send_button.grid(row=2, column=0)  # 按钮分区
txt_msgsend.grid()  # 消息发送文本控件加载
button_send.grid(sticky=W)  # 发送按钮控件加载
button_cancel.grid(row=0, column=1, sticky=W)  # 取消按钮控件加载
msg_send.grid_propagate(0)

# 在线用户框
usr_list_frame = Frame(height=500, width=200, bg="white")
user_listbox = Listbox(usr_list_frame)
for item in usr_name_list:
    user_listbox.insert(END, item)
usr_list_frame.grid(row=0, column=1, rowspan=3, padx=3)
user_listbox.place(x=5, y=0, relwidth=0.9, relheight=1)
yscrollbar = Scrollbar(user_listbox, command=user_listbox.yview)
yscrollbar.pack(side="right", fill="y")
user_listbox.config(yscrollcommand=yscrollbar.set)
usr_list_frame.grid_propagate(0)

root.mainloop()