from tkinter import *
from PIL import Image, ImageTk

from PIL import ImageDraw , ImageFont
import tkinter
import os
import sys
import pandas as pd
from tkinter import filedialog, dialog, messagebox
from OpenCV import OpenCV
from KDF import KDF
from BCH import BCH
from datetime import datetime
import time

opencv=OpenCV()

img_wid=142
img_height=172
global train_forder
train_forder='D:/Python/Python36-64/MachineLearning/Face/image/opencv/train'
global img_test
def ReadFile():
    global file_path
    global file_text
    global img_test

    file_path = filedialog.askopenfilename(title=u'select file', initialdir=(train_forder))
    img_test = file_path

    #path.set(file_path)
    #img = root.PhotoImage(file=file_path)
    #img = ImageTk.PhotoImage(file=file_path)
    img = Image.open(file_path)

    img = img.resize([img_wid, img_height])
    ph = ImageTk.PhotoImage(img)
    ReadImage.configure(image=ph,height=img_height,width=img_wid)
    ReadImage.image = ph  # 刷新一下（重点）


    #messagebox.showinfo('提示', '统计成功')

def EnrollUser():
    global train_forder
    dir_path = filedialog.askdirectory(title=u'select folder', initialdir=(os.path.expanduser('H:/')))
    train_forder=dir_path
    opencv.createDatabase(dir_path)
    messagebox.showinfo('Info', 'User enrollment is completed')

def RecognizeUser():
    global train_forder
    global img_test

    user_name=opencv.recognize(img_test)
    print(train_forder)
    result_file_path=os.path.join(train_forder, user_name)
    print(result_file_path)
    files = os.listdir(result_file_path)
    for file in files:
        file_path = os.path.join(result_file_path, file)
        if os.path.isfile(file_path):
            img = Image.open(file_path)
            img = img.resize([img_wid, img_height])
            font = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf', 25)
            w, h = font.getsize(user_name)
            draw = ImageDraw.Draw(img)
            draw.text(((img_wid-w)/2, img_height*3/4), user_name, fill='red',font = font)
            ph = ImageTk.PhotoImage(img)
            ShowImage.configure(image=ph, height=img_height, width=img_wid)
            ShowImage.image = ph  # 刷新一下（重点）
        break

    #messagebox.showinfo('提示', '识别结果：'+user_name)
    ShowImage.configure(text="user_name")
    root.update_idletasks()
    #ShowImage.update()
def Batch():

    img_test_path="D:\\Python\\Python36-64\\MachineLearning\\Face\\image\\opencv\\test"
    files = os.listdir(img_test_path)

    logfile='log'+datetime.now().strftime('%Y%m%d%H%M%S')+'.txt'
    non=0
    for file in files:
        file_path = os.path.join(img_test_path, file)
        if os.path.isfile(file_path):
            print('img_test:'+file)
            result=opencv.recognizewithkey(file_path)
            if result=='None':
                non=non+1
            record='['+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+']:'+file[:-4]+'::'+result
            with open(logfile, "a") as txtfile:
                # 将字符串写入文件
                txtfile.write(record)
                txtfile.write("\n")
    record = '[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']:' + 'non::' + str(non)
    with open(logfile, "a") as txtfile:
        txtfile.write(record)
        txtfile.write("\n")
    messagebox.showinfo('info', 'Batch is completed')

def RecognizeUserWithKey():
    global train_forder
    global img_test

    print("img_test:%sok" % img_test)
    user_name=opencv.recognizewithkey(img_test)
    '''
    print(train_forder)
    result_file_path=os.path.join(train_forder, user_name)
    print(result_file_path)
    files = os.listdir(result_file_path)
    for file in files:
        file_path = os.path.join(result_file_path, file)
        if os.path.isfile(file_path):
            img = Image.open(file_path)
            img = img.resize([img_wid, img_height])
            font = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf', 25)
            w, h = font.getsize(user_name)
            draw = ImageDraw.Draw(img)
            draw.text(((img_wid-w)/2, img_height*3/4), user_name, fill='red',font = font)
            ph = ImageTk.PhotoImage(img)
            ShowImage.configure(image=ph, height=img_height, width=img_wid)
            ShowImage.image = ph  # 刷新一下（重点）
        break
    '''
    messagebox.showinfo('提示', '识别结果：'+user_name)
    ShowImage.configure(text="user_name")
    root.update_idletasks()
    #ShowImage.update()

if __name__ == "__main__":
    root = Tk()
    root.title('Facial Biometric Authentication System V2.0')
    root.iconbitmap('secret.ico')
    #root.iconphoto(False, PhotoImage(file='secret.ico'))
    screen_width, screen_height = root.maxsize()  # 获取屏幕最大长宽
    w = int((screen_width - 530) / 2)
    h = int((screen_height - 300) / 2)
    # 对应的格式为宽乘以高加上水平偏移量加上垂直偏移量
    # root.geometry("600x400+200+200")
    root.geometry(f'530x300+{w}+{h}')  # 设置窗口大小为240x480，调整位置
    # label = Label(root, text="人脸识别认证系统V1.0", font=("微软雅黑", 18), fg="black")
    frame1 = Frame(highlightthickness=3)
    frame1.grid(row=0, column=0)
    readf = LabelFrame(frame1, text='Read image', padx=5, pady=5)
    readf.grid(row=0, column=0)
    ReadImage = Label(readf, borderwidth = 1,
         relief="sunken",
         text="",height=10, width=20)
    ReadImage.grid(row=1, column=1, sticky=W)


    showf = LabelFrame(frame1, text='Recognize image', padx=5, pady=5)
    showf.grid(row=0, column=1)
    ShowImage = Label(showf, borderwidth = 1,
         relief="sunken",
         text="",height=10, width=20)
    ShowImage.grid(row=1, column=1, sticky=W)

    frame3 = Frame(highlightthickness=3)
    frame3.grid(row=0, column=2)

    opf1 = LabelFrame(frame3, text='Enrollment', padx=5, pady=5)
    opf1.grid(row=0, column=0)
    b1 = Button(opf1, text='Enroll', command=EnrollUser, font=("微软雅黑", 12))
    b1.grid(row=0, column=1, sticky=E,padx=2, pady=5)
    b4 = Button(opf1, text='Batch', command=Batch, font=("微软雅黑", 12))
    b4.grid(row=0, column=2, sticky=W,padx=0, pady=5)

    opf2 = LabelFrame(frame3, text='Authentication', padx=5, pady=5)
    opf2.grid(row=1, column=0)
    b2 = Button(opf2, text='Open image', command=ReadFile, font=("微软雅黑", 12))
    b2.grid(row=1, column=1, sticky=E,padx=50, pady=5)

    b3 = Button(opf2, text='Authticate', command=RecognizeUserWithKey, font=("微软雅黑", 12))
    b3.grid(row=2, column=1, sticky=W,padx=50, pady=5)

    frame4 = Frame(highlightthickness=3)
    frame4.grid(row=1, column=0)

    label1 = Label(frame4, text="Copyright：SUT 2023.4.10", font=("微软雅黑", 10),
                  fg="black")
    label1.grid(row=0, column=0, sticky=W, columnspan=4)
    #label1.place(relx=0.5,rely=0.5,anchor='center')

    root.mainloop()
