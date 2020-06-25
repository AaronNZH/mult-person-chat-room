import time
from tkinter import *


def msgsend():
    msg = '我' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n'
    txt_msglist.insert(END, msg, 'green')
    txt_msglist.insert(END, txt_msgsend.get('0.0', END))  # 获取发送消息，添加文本到消息列表
    txt_msgsend.delete('0.0', END)  # 清空发送消息


def cancel():
    txt_msgsend.delete('0.0', END)  # 取消发送消息，即清空发送消息


def msgsendEvent(event):
    if event.keysym == 'Up':
        msgsend()


root = Tk()
root.title('振华的聊天室')

# 聊天框
msg_list = Frame(height=320, width=500)
txt_msglist = Text(msg_list)  # 消息列表分区中创建文本控件
txt_msglist.tag_config('green', foreground='blue')  # 消息列表分区中创建标签
msg_list.grid(row=0, column=0)  # 消息列表分区
txt_msglist.grid()  # 消息列表文本控件加载
msg_list.grid_propagate(0)

# 编辑框
msg_send = Frame(height=150, width=500)
send_button = Frame(height=30, width=500)
txt_msgsend = Text(msg_send)  # 发送消息分区中创建文本控件
txt_msgsend.bind('<KeyPress-Up>', msgsendEvent)  # 发送消息分区中，绑定‘UP’键与消息发送
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
for item in ["在线用户：", "nzh", "aaron"]:
    user_listbox.insert(END, item)
usr_list_frame.grid(row=0, column=1, rowspan=3, padx=3)
user_listbox.place(x=5, y=0, relwidth=0.9, relheight=1)
yscrollbar = Scrollbar(user_listbox, command=user_listbox.yview)
yscrollbar.pack(side="right", fill="y")
user_listbox.config(yscrollcommand=yscrollbar.set)
usr_list_frame.grid_propagate(0)

root.mainloop()
