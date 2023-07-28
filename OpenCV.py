import numpy as np
import cv2
import dlib
import os
import sys
import random
import pandas as pd
from BCH import BCH
from KDF import KDF
import hashlib
import time
import pickle
import base64
# 存储位置
class OpenCV(object):
    def __init__(self,  **locker_args):
        self.output_dir = './faces'
        self.fv_file='fv.csv'
        self.w0_file = 'w0.csv'
        self.w1_file = 'w1.csv'
        self.pd_file='pd.csv'
        self.hash_file = 'HR0.csv'
        self.data_file = 'database.csv'
        self.bch=BCH()
        self.kdf=KDF()
        self.md5 = hashlib.md5()
        self.PhotoName = []

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)



    def recognizewithkey(self,img_path):
        feature_test = self.return_128d_features(img_path)
        #mean_arr = np.zeros(128)
        w1=self.PreProcess(feature_test)
        print("%s:w1:%s" % (img_path[-8:-4],w1))


        with open(self.data_file, 'r') as file:
            for line in file:

                line = line.rstrip()
                print("line:%s" % line)
                record = line.split(',')
                #print("pd:%s" % record[1])
                R1_1=self.GetXOR(w1,record[1])
                #print("R1_1:%s" % R1_1)
                R1=self.GetR1(R1_1)
                print("R1:%s" % R1)
                #self.md5.update(R1.encode('utf-8'))
                R1_hash = hashlib.sha1(R1.encode('utf-8'))
                print("R1hash:%s" % R1_hash.hexdigest())
                if R1_hash.hexdigest()== record[2]:
                    return record[0]

        return 'None'



    # 改变图片的亮度与对比度
    def relight(self,img, light=1, bias=0):
        w = img.shape[1]
        h = img.shape[0]
        # image = []
        for i in range(0, w):
            for j in range(0, h):
                for c in range(3):
                    tmp = int(img[j, i, c] * light + bias)
                    if tmp > 255:
                        tmp = 255
                    elif tmp < 0:
                        tmp = 0
                    img[j, i, c] = tmp
        return img

    def BinaryCode(self,x):
        if x < 0:
            return int(0)
        else:
            return int(1)
    def Filter(self,txt):
        txt.replace(" ", "")
        txt.replace("[", "")
        txt.replace("]", "")
        return txt

    def createDatabase(self,path):


        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

        EigenFace=[]
        files = os.listdir(path)
        with open(self.data_file, 'w') as file:
            file.truncate(0)
        for file in files:
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                print(file)

            elif os.path.isdir(file_path):
                self.PhotoName.append(file)
                #f.write(file+",")
                #eigenvalue=GetEigen(file_path)
                eigenvalue=self.Get_128d_features(file_path)
                #print("eigenvalue:%s" % eigenvalue)
                w0=self.PreProcess(eigenvalue)
                print("w0:%s" % w0)
                R0 = self.GetR0(w0)
                #print("R0:%s" % R0)
                R0_1 = self.GetR0_1(R0)
                #print("R0_1:%s" % R0_1)
                PublicData = self.GetXOR(w0,R0_1)
                print("PublicData:%s" % PublicData)
                #self.md5.update(R0.encode('utf-8'))
                R0_hash=hashlib.sha1(R0.encode('utf-8'))
                record=file+','+PublicData+','+R0_hash.hexdigest()+','+w0+','+R0
                with open(self.data_file, "a") as file:
                    # 将字符串写入文件
                    file.write(record)
                    file.write("\n")









    def Get_128d_features(self,path):

        files = os.listdir(path)
        index_f=0
        face_person=[]
        for file in files:
            index_f+=1
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                face_descriptor = self.return_128d_features(file_path)
                face_person.append(face_descriptor)



        data_np = np.array(face_person)
        data = pd.DataFrame(data_np)
        data_mean=data.mean(0)
        data_var = data.var(0)
        #v_r_mean = np.array(data_mean).reshape(1, -1)
        #v_r_var = np.array(data_var).reshape(1, -1)
        #v_r_mean=np.mean(v_r)
        #v_r_var=np.var(v_r)
        #print('Mean:',v_r_mean,'Variance:',v_r_var)
        #data_v = pd.DataFrame(v_r)
        #data_v.to_csv('person_mean.csv', mode='a',header=None, index=None)
        return data_mean





    # 返回单张图像的 128D 特征
    def return_128d_features(self,path_img):
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        img_rd = cv2.imread(path_img)
        img_gray = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
        faces = detector(img_gray, 1)
        face_rec = dlib.face_recognition_model_v1(
            "dlib_face_recognition_resnet_model_v1.dat")
        #print("%-2s %-2s" % ("正在检测图像 :", path_img), '/n')
        print("Extracting:", path_img)

        # 因为有可能截下来的人脸再去检测，检测不出来人脸了
        # 所以要确保是 检测到人脸的人脸图像 拿去算特征
        if len(faces) != 0:
            shape = predictor(img_gray, faces[0])
            face_descriptor = face_rec.compute_face_descriptor(img_gray, shape)
        else:
            face_descriptor = 0
            print("no face")

        return face_descriptor


    def PreProcess(self,fv):
        percentile25 = np.percentile(fv, 25)
        percentile50 = np.percentile(fv, 50)
        percentile75 = np.percentile(fv, 75)
        binary_string = ""
        for i in range(0,128):
            #print("fv-mean:%s:%s:%s"%(fv[i],mean[i],type(fv[i])))
            mean = np.mean(fv)
            #print("mean:%s" % mean)
            if fv[i] < 0:
                binary_string += '0'
            else:
                binary_string += '1'
        return binary_string

    def GetR0(self,w0):
        #ascii_string=self.kdf.BinaryToStr(w0)
        btarr_w0 = self.kdf.BinaryToByteArray(w0)
        str_R0=self.kdf.Key_Derive(btarr_w0,10)
        binary_string = ''.join([bin(byte)[2:].zfill(8) for byte in str_R0])
        return binary_string
    def GetR0_1(self,R0):
        #str_R0 = self.kdf.BinaryToStr(R0)
        btarr_R0 = self.kdf.BinaryToByteArray(R0)
        R0_1=self.bch.do_encode(btarr_R0)
        R0_1_binary_string = ''.join([bin(byte)[2:].zfill(8) for byte in R0_1])

        return R0_1_binary_string
    def GetR1(self,R1_1):
        #str_R1_1 = self.kdf.BinaryToStr(R1_1)
        #print("str_R1_1:%s"%str_R1_1)

        btarr_R1_1 = self.kdf.BinaryToByteArray(R1_1)
        R1=self.bch.do_decode(btarr_R1_1)
        R1_binary_string = ''.join([bin(byte)[2:].zfill(8) for byte in R1])

        return R1_binary_string
    def GetXOR(self,w0,R0_1):
        num1 = int(w0, 2)
        num2 = int(R0_1, 2)

        # 对十进制整数进行异或操作
        pd = num1 ^ num2
        result_binary_str = bin(pd)[2:].zfill(len(w0))
        return result_binary_str