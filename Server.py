# -*- coding: UTF-8 -*-
# filename: ShowImage date: 2017/12/26 19:13
# author: FD
# Putting a gif image on a canvas with Tkinter
from PIL import Image as pilImage
from Tkinter import *
from  datetime import *
import socket
import threading
from Config import *

actions = ["up", "down", "right", "left", "1", "2", "3", "4"]
client = None
buttons=[]

# 发送消息
def sendMessage(message):
    global client
    client.send(message)  # 发送消息


# 建立socket连接
def setupSocket():
    global client
    # 创建socket
    s = socket.socket()
    # 监听端口
    s.bind((SERSER_IP, PORT))
    s.listen(5)
    sock, addr = s.accept()
    print "a client come ", str(addr)
    client = sock

def buttonClick(event):
    button=event.widget
    buttonIndex=buttons.index(button)
    sendMessage(str(buttonIndex))
    pass

root = Tk()
for i in range(actions.__len__()):
    action = actions[i]
    button = Button(master=root, text=action)
    button.pack(side=LEFT)
    button.bind("<Button-1>",buttonClick)
    buttons.append(button)


thread = threading.Thread(target=setupSocket)
thread.start()
root.mainloop()
