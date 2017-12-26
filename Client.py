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

actionsFrames = []
imageDirectory = "image/"
actions = ["up", "down", "right", "left", "1", "2", "3", "4", "5"]
operations = ["向上", "向下", "向右", "向左", "按下1按钮", "按下2按钮", "按下3按钮", "按下4按钮"]


# 计算gif图的帧数
def getGIFFrameCount(filepath):
    im = pilImage.open(filepath)
    frameCount = 1
    # To iterate through the entire gif
    try:
        while 1:
            im.seek(im.tell() + 1)
            frameCount += 1
            # do something to im
    except EOFError:
        pass  # end of sequence
    return frameCount


def init():
    # 设置每个gif图的帧数
    for action in actions:
        actionImagePath = "".join([imageDirectory, action, ".gif"])
        frameCount = getGIFFrameCount(actionImagePath)
        print "frameCount=", str(frameCount)
        frames = [PhotoImage(file=actionImagePath, format='gif -index %i' % (i)) for i in range(frameCount)]
        actionsFrames.append(frames)


# 显示gif动图
def showGIF(gifName, frameIndex):
    index = actions.index(gifName)
    frames = actionsFrames[index]
    label.update_idletasks()
    root.update_idletasks()
    if frameIndex < frames.__len__():
        label.configure(image=frames[frameIndex])
        label.update_idletasks()
        root.update_idletasks()
        print "frameIndex=" + str(frameIndex)
        root.after(100, showGIF, gifName, frameIndex + 1)


# 开始
def start():
    global button
    button.destroy()
    T.insert(END, timestamp() + " " + "started" + "\n")
    T.see(END)
    button = Button(master=root, text="结束", command=end)
    button.pack()


# 结束
def end():
    global button
    button.destroy()
    T.insert(END, timestamp() + " " + "ended" + "\n")
    T.see(END)
    button = Button(master=root, text="开始", command=start)
    button.pack()


# 获得时间戳
def timestamp():
    dt = datetime.now()
    dateStr = dt.strftime('%Y-%m-%d %H:%M:%S')
    return dateStr


# 接受tcp消息
def receiveMessage():
    global T
    s = socket.socket()
    s.connect((SERSER_IP, PORT))
    print "connect success"
    while True:
        message = int(s.recv(1))
        print "recv message=", str(message)
        action = actions[message]
        dateStr = timestamp()
        T.insert(END, dateStr + " " + operations[message] + "\n")
        T.see(END)
        root.after(0, showGIF, action, 0)
        if message in [1, 2, 3, 4]:
            root.after(1500, showGIF, "5", 0)


root = Tk()
init()  # 初始化frames
# 加载组件
label = Label(root)
label.pack()
root.title("手柄实时系统")
showGIF("up", 14)
S = Scrollbar(root)
T = Text(root)
S.pack(side=RIGHT, fill=Y)
T.pack(fill=BOTH)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
button = Button(master=root, text="开始", command=start)
button.pack()
thread = threading.Thread(target=receiveMessage)
thread.start()
root.mainloop()
