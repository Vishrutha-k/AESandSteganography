# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 22:36:04 2019

@author: vishr
"""

import sys
from Crypto import Random
from Crypto.Cipher import AES
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QComboBox, QWidget,QApplication,QDesktopWidget, QTabWidget, QVBoxLayout, QLabel, QTextEdit,QHBoxLayout,QPushButton, QFileDialog, QDialog
import collections
import os
import os.path
from os import listdir
from os.path import isfile,join
import hashlib
import time
from zipfile import ZipFile
import zipfile
import PyPDF2
import docx2txt
import binascii
import random
import cv2
#from string2binary import stringtochartobinarytoimage
class Encryptor:
    def __init__(self, key):
        self.key = key
    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)
    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)
    def encrypt_file(self, file_name):
        global data
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        self.data=enc
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
            print(enc)
        os.remove(file_name)
    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")
    def decrypt_file(self, file_name):
        global data1
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        self.data1=dec
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)
    def imagetobinarytochartostring(self,image):
        str = ''
        for pixel in image:
            i=0
            char=0;
            for bits in pixel:
                char = char | bits<<(i*(2))
                i=i+1
            if(char==3):
                break
            str = str + chr(char)
        return str
    def d1arraytod2array(self,array):        
        length = len(array)
        sr = length**(0.5)
        print(sr)
        print(int(sr))
        if(sr>int(sr)):
            sr  = int(sr)+1
        print(sr)
        numberofzeropadding = (sr*sr) - length
        paddedarray = self.paddingzeroesattheend(array, numberofzeropadding)
        new2darray = self.converter1dto2d(paddedarray, sr)
        return new2darray
    def paddingzeroesattheend(self,array,no):
        i = 0
        while(i<=no):
            array.append([0,0,0,0])
            i=i+1
        return array
    def converter1dto2d(self,array,no):
        new2darray = []
        i =0
        start = 0
        end = no-1
        while(i<no):
            temp = []
            j = start
            while(j<=end):
                temp.append(array[j])
                j=j+1
            new2darray.append(temp)
            start = start+no
            end = end+no
            i=i+1
        return new2darray

    def stringtochartobinarytoimage(self,str):
        binaryimg = []
        for letter in str:
            #print ("."+letter+".")
            #print (ord(letter))
            a = ord(letter)
        #print(bin(a))
            pixel = []
            i =0
            while(i<4):
                last2 = a & 3
                pixel.append(last2)
                binlast2 = bin(last2)
                #print (binlast2)
                a = a>>2
                i=i+1
            binaryimg.append(pixel)
        return binaryimg
    def encode(self,image,message,filename):
        key = []
        hidingarray = message
        # print(len(hidingarray))
        # print(len(image))
        # print(len(hidingarray[0]))
        # print(len(image[0]))
        if(len(image)>len(hidingarray) and len(image[0])>len(hidingarray[0])):
            y = random.randrange(0, len(image) - len(hidingarray))
            x = random.randrange(0,len(image[0])-len(hidingarray[0]))
            # print(y)
            # print(x)
            key.append(y)
            key.append(x)
            key.append(len(hidingarray))
            key.append(len(hidingarray[0]))
            height = y
            i = 0
            while(i<len(hidingarray)):
                width = x
                j = 0
                while(j<len(hidingarray[0])):
                    pixel = image[height][width]
                    hidingpixel  = hidingarray[i][j]
                    indexs = [0,1,2,3]
                    for index in indexs:
                        last2zero = pixel[index] & 0b11111100
                        pixel[index] = last2zero | hidingpixel[index]
                    image[height][width] = pixel
                    j = j+1
                    width  = width +1
                i=i+1
                height = height+1
        # print('yes')
        cv2.imwrite(filename+".png", image)
        return key    
    def decode(self,image , key):
        hidearray = []
        y  =key[0]
        x  =key[1]
        height_encode_img  = key[2]
        width_encode_img  = key[3]
        # print(height_encode_img)
        # print(width_encode_img)
        height = y
        i = 0
        while (i < height_encode_img):
            width = x
            j = 0
            while (j < width_encode_img):
                pixel  = image[height][width]
                hiddenpixel = []
                indexs = [0, 1, 2, 3]
                for index in indexs:
                    hiddenpixel.append(pixel[index]& 0b00000011)
                hidearray.append(hiddenpixel)
                j = j + 1
                width = width + 1
            i = i + 1
            height = height + 1
            # print('decoded')
        print(hidearray)
        return hidearray
class MainWindow(Encryptor,QWidget):
    fname=''
    data=''
    p=''
    key=''
    start_time=0
    start_time1=0
    img=cv2.imread("C:/Users/vishr/Desktop/final/Cyberp")
    mat=[]
    res1=''
    ans=''
    def __init__(self):
        QWidget.__init__(self)
        global start_time
        self.setGeometry(0,0,700,700)
        self.setWindowTitle("Implementation of a file encryption system")
        self.setWindowIcon(QtGui.QIcon("key.png"))
        self.resize(600,550)
        self.setMinimumSize(600,550)
        self.center()
        self.tab_widget=QTabWidget()
        tab1=QWidget()
        tab2=QWidget()
        tab3=QWidget()
        tab4=QWidget()
        l1=QVBoxLayout(tab1)
        l2=QVBoxLayout(tab2)
        l3=QVBoxLayout(tab3)
        l4=QVBoxLayout(tab4)
        #declarations for gui
        self.tab_widget.addTab(tab1,"Encryption using AES(256 bit)")
        self.tab_widget.addTab(tab2,"Decryption using AES(256 bit)")
        self.tab_widget.addTab(tab3,"Steganography module")
        self.tab_widget.addTab(tab4,"AES and Steganography")
        label1=QLabel("Implementation of File Encryption")
        label1.setStyleSheet("font-size:13pt")
        label1.setAlignment(QtCore.Qt.AlignCenter)
        dd1=QComboBox(self)
        dd1.addItem("Text file")
        dd1.addItem("Zip file")
        dd1.addItem("Pdf file")
        dd1.addItem("Word document")
        dd1.activated[str].connect(self.onActivated)
        self.button_file=QPushButton("Import source",self)
        label2=QLabel("Enter password")
        label2.setStyleSheet("font-size:11pt")
        self.button_encrypt=QPushButton("Encrypt",self)
        #button_file.clicked.connect(self.importfile)
        label3=QLabel("Time")
        label3.setStyleSheet("font-size:11pt")
        self.text1=QTextEdit()
        self.time1=QTextEdit()
        #self.time1.setMaximumHeight(label3.sizeHint().height()*10)
        hbox=QHBoxLayout()
        #button_encrypt.clicked.connect(self.ans_file)
        l1.addWidget(label1)
        l1.addWidget(dd1)
        l1.addWidget(self.button_file)
        l1.addWidget(label2)
        l1.addWidget(self.text1)
        l1.addWidget(self.button_encrypt)
        l1.addStretch(1)
        l1.addLayout(hbox)
        l1.addWidget(label3)
        l1.addWidget(self.time1)
        vbox=QVBoxLayout()  
        vbox.addWidget(self.tab_widget)
        self.setLayout(vbox)
        
        #DECRYPTION
        label4=QLabel("Implementation of File Decryption")
        label4.setStyleSheet("font-size:13pt")
        label4.setAlignment(QtCore.Qt.AlignCenter)
        self.button_file1=QPushButton("Import Source",self)
        label5=QLabel("Please confirm your password")
        label5.setStyleSheet("font-size:11pt")
        self.button_decrypt=QPushButton("Decrypt",self)
        #button_file1.clicked.connect(self.importfile1)
        label6=QLabel("Time")
        label6.setStyleSheet("font-size:11pt")
        self.text2=QTextEdit()
        self.time2=QTextEdit()
        #self.time2.setMaximumHeight(label6.sizeHint().height()*10)
        hbox1=QHBoxLayout()
        #button_decrypt.clicked.connect(self.ans_file1)
        dd2=QComboBox(self)
        dd2.addItem("Text .enc file")
        dd2.addItem("Zip .enc file")
        dd2.addItem("Pdf .enc file")
        dd2.addItem("Word .enc document")
        l2.addWidget(label4)
        l2.addWidget(dd2)
        l2.addWidget(self.button_file1)
        l2.addWidget(label5)
        l2.addWidget(self.text2)
        l2.addWidget(self.button_decrypt)
        l2.addStretch(1)
        l2.addLayout(hbox1)
        l2.addWidget(label6)
        l2.addWidget(self.time2)
        dd2.activated[str].connect(self.onActivated1)
        '''vbox1=QVBoxLayout()
        vbox1.addWidget(self.tab_widget)
        self.setLayout(vbox1)
        '''
        label7=QLabel("Steganography")
        label7.setStyleSheet("font-size:13pt")
        label7.setAlignment(QtCore.Qt.AlignCenter)
        label8=QLabel("Enter the text to be encrypted")
        label8.setStyleSheet("font-size:11pt")
        label9=QLabel("Please select an image")
        label9.setStyleSheet("font-size:11pt")
        label10=QLabel("Encrypt the image")
        label10.setStyleSheet("font-size:11pt")
        label11=QLabel("Dencrypt the image")
        label11.setStyleSheet("font-size:11pt")
        
        self.button_img=QPushButton("Import Image",self)
        self.button_encrypt_i=QPushButton("Encrypt image with text",self)
        self.button_decrypt_i=QPushButton("Decrypt image with text",self)
        self.text3=QTextEdit()
        self.time3=QTextEdit()
        label10=QLabel("Time")
        label10.setStyleSheet("font-size:11pt")
        hbox2=QHBoxLayout()
        dd3=QComboBox(self)
        dd3.addItem(".PNG Image")
        #dd3.addItem(".JPG Image")
        l3.addWidget(label7)
        l3.addWidget(label9)
        l3.addWidget(dd3)
        l3.addWidget(self.button_img)
        l3.addWidget(label10)
        l3.addWidget(label8)
        l3.addWidget(self.text3)
        l3.addWidget(self.button_encrypt_i)
        l3.addWidget(label11)
        l3.addWidget(self.button_decrypt_i)
        l3.addStretch(1)
        l3.addLayout(hbox2)
        l3.addWidget(label10)
        l3.addWidget(self.time3)
        dd3.activated[str].connect(self.onActivated2)
        #l3.addLayout(hbox2)
        label13=QLabel("Cryptography and Steganography")
        label13.setStyleSheet("font-size:13pt")
        label13.setAlignment(QtCore.Qt.AlignCenter)
        label14=QLabel("Enter the text to be encrypted")
        label14.setStyleSheet("font-size:11pt")
        label15=QLabel("Please select an image")
        label15.setStyleSheet("font-size:11pt")
        label15=QLabel("Encrypt the image")
        label15.setStyleSheet("font-size:11pt")
        label16=QLabel("Dencrypt the image")
        label16.setStyleSheet("font-size:11pt")
        self.button_img1=QPushButton("Import Image",self)
        self.button_encrypt_i1=QPushButton("Encrypt image with text",self)
        self.button_decrypt_i1=QPushButton("Decrypt image with text",self)
        self.text4=QTextEdit()
        self.time4=QTextEdit()
        self.pass4=QTextEdit()
        label12=QLabel("Time")
        label12.setStyleSheet("font-size:11pt")
        hbox3=QHBoxLayout()
        dd4=QComboBox(self)
        dd4.addItem(".PNG Image")
        label17=QLabel("Password")
        label17.setStyleSheet("font-size:11pt")
        #dd3.addItem(".JPG Image")
        l4.addWidget(label13)
        l4.addWidget(label15)
        l4.addWidget(dd4)
        l4.addWidget(self.button_img1)
        l4.addWidget(label12)
        l4.addWidget(label14)
        l4.addWidget(self.text4)
        l4.addWidget(label17)
        l4.addWidget(self.pass4)
        l4.addWidget(self.button_encrypt_i1)
        l4.addWidget(label12)
        l4.addWidget(self.button_decrypt_i1)
        l4.addStretch(1)
        l4.addLayout(hbox3)
        l4.addWidget(label12)
        l4.addWidget(self.time4)
        dd4.activated[str].connect(self.onActivated3)
        
    def onActivated(self,text):
        print(text)
        if text=="Text file":
            self.button_file.clicked.connect(self.importfile)
            self.button_encrypt.clicked.connect(self.ans_file)
        if text=="Zip file":
            self.button_file.clicked.connect(self.importfile)
            self.button_encrypt.clicked.connect(self.ans_z_file)
        if text=="Pdf file":
            self.button_file.clicked.connect(self.importfile)
            self.button_encrypt.clicked.connect(self.ans_p_file)
        if text=="Word document":
            self.button_file.clicked.connect(self.importfile)
            self.button_encrypt.clicked.connect(self.ans_d_file)
    
    def onActivated1(self,text):
        print(text)
        if text=="Text .enc file":
            self.button_file1.clicked.connect(self.importfile1)
            self.button_decrypt.clicked.connect(self.ans_file1)
        if text=="Zip .enc file":
            self.button_file1.clicked.connect(self.importfile_z1)
            self.button_decrypt.clicked.connect(self.ans_z_file1)
        if text=="Pdf .enc file":
            self.button_file1.clicked.connect(self.importfile1)
            self.button_decrypt.clicked.connect(self.ans_p_file1)
        if text=="Word .enc document":
            self.button_file1.clicked.connect(self.importfile1)
            self.button_decrypt.clicked.connect(self.ans_p_file1)
            
    def onActivated2(self,text):
        print(text)
        if text==".PNG Image":
            self.button_img.clicked.connect(self.importfile_i)
            self.button_encrypt_i.clicked.connect(self.ans_image)
            self.button_decrypt_i.clicked.connect(self.ans_image_d)
    def onActivated3(self,text):
        print(text)
        if text==".PNG Image":
            self.button_img1.clicked.connect(self.importfile_i)
            self.button_encrypt_i1.clicked.connect(self.ans_image1)
            self.button_decrypt_i1.clicked.connect(self.ans_image_d1)
        
    def center(self):
        screen=QDesktopWidget().screenGeometry()
        size=self.geometry()
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)
    def importfile(self):
        global start_time,fname
        self.fname,_=QFileDialog.getOpenFileName(self,"Open File","C:/Users/vishr/Desktop/final/Cyberp")
        if self.fname:
            print(self.fname)
        else:
            print("No such file exists")
    
    def importfile_i(self):
        global start_time,fname,img
        self.fname,_=QFileDialog.getOpenFileName(self,"Open File","C:/Users/vishr/Desktop/final/Cyberp")
        print(self.fname[-4:])
        if self.fname[-4:]==".png" or self.fname[-4:]==".PNG":
            print(self.fname)
            print(self.fname)
            self.img=cv2.imread(self.fname)
            self.img=cv2.cvtColor(self.img,cv2.COLOR_RGB2RGBA)
        else:
            print("No such file exists")
            
    def importfile1(self):
        global start_time,fname
        self.fname,_=QFileDialog.getOpenFileName(self,"Open File","C:/Users/vishr/Desktop/final/Cyberp")
        if self.fname:
            print(self.fname)
        else:
            print("No such file exists")
    def importfile_z1(self):
        global start_time,fname
        self.fname=QFileDialog.getExistingDirectory(self,"Select the directory")
                #self,"Open File","C:/Users/vishr/Desktop/final/Cyberp")
        if self.fname:
            print(self.fname)
        else:
            print("No such file exists")
    
    def ans_file(self):
        global p,fname,start_time,key,mat,data,data1,res,ans
        print(self.fname)
        self.p=self.text1.toPlainText()
        print("The password is:"+str(self.p))
        k=self.fname+" "+self.p
        self.mat.append(k)
        print(self.mat)
        self.start_time=time.time()
        self.key=hashlib.sha256(str(self.p).encode("utf-8")).digest()
        self.encrypt_file(self.fname)
        t=time.time()-self.start_time
        self.time1.insertPlainText(str(t))
        '''
        res=""
        for b in self.data:
            res += "%02x" % b
        print(res)
        '''
        res=self.data.hex()
        print(res)
        ans=bytearray.fromhex(res)
        print(ans)
        #print(binascii.decode(self.data).decode("ascii"))
        #print(self.data.decode("utf-8"))
    
    def ans_z_file(self):
        global p,fname, start_time,key,mat
        print(self.fname)
        self.p=self.text1.toPlainText()
        print("The password is:"+str(self.p))
        t=0
        k=self.fname[:-4]
        x=self.fname+" "+self.p
        self.mat.append(x)
        os.mkdir(k)
        with ZipFile(self.fname,'r') as zip:
            zip.printdir()
            zip.extractall(k)
        #DIR="C:/Users/vishr/Desktop/final/Cyberp/answer"
        self.l=len([name for name in os.listdir(k) if os.path.isfile(os.path.join(k,name))])
        print(self.l)
        self.key=hashlib.sha256(str(self.p).encode("utf-8")).digest()
        for name in os.listdir(k):
            if os.path.isfile(os.path.join(k,name)):
                self.start_time=time.time()
                self.encrypt_file(os.path.join(k,name))
                t+=time.time()-self.start_time
        self.time1.insertPlainText(str(t))
        #os.rename(k,k+".enc")
        
    def ans_p_file(self):
        global p,fname,start_time,key,mat
        print(self.fname)
        self.p=self.text1.toPlainText()
        print("The password is:"+str(self.p))
        t=0
        eg=self.fname+" "+self.p
        self.mat.append(eg)
        pd=open(self.fname,'rb')
        reader=PyPDF2.PdfFileReader(pd)
        print("The number of pages are:"+str(reader.numPages))
        self.key=hashlib.sha256(str(self.p).encode("utf-8")).digest()
        t=0
        for i in range(reader.numPages):
            pi=reader.getPage(i)
            pt=pi.extractText()
            pt=pt.encode("utf-8")
            self.start_time=time.time()
            enc=self.encrypt(pt,self.key) 
            with open(self.fname+".enc",'wb') as fo:
                fo.write(enc)
                print(enc)
            t+=time.time()-self.start_time
        #os.remove(self.fname)
        self.time1.insertPlainText(str(t))
    
    def ans_d_file(self):
        global p,fname,start_time,key,mat
        print(self.fname)
        self.p=self.text1.toPlainText()
        print("The password is"+str(self.p))
        t=0
        eg=self.fname+" "+self.p
        self.mat.append(eg)
        text=docx2txt.process(self.fname)
        self.key=hashlib.sha256(str(self.p).encode("utf-8")).digest()
        text=text.encode("utf-8")
        self.start_time=time.time()
        enc=self.encrypt(text,self.key)
        with open(self.fname+".enc",'wb') as fo:
            fo.write(enc)
            print(enc)
        t=time.time()-self.start_time
        self.time1.insertPlainText(str(t))
    
            
    def ans_file1(self):
        global cp,fname,start_time1,key,mat,data1
        print(self.fname)
        self.cp=self.text2.toPlainText()
        print("The entered password is"+str(self.cp))
        y=self.fname
        y=y[:-4]
        print(y)
        for i in range(len(self.mat)):
            if y in self.mat[i]:
                a1=self.mat[i]
                arr=a1.split(" ")
                print(arr)
                if self.cp==arr[1]:
                    print("Password match")
                    self.key=hashlib.sha256(str(self.p).encode("utf-8")).digest()
                    start_time1=time.time()
                    self.decrypt_file(self.fname)
                    t=time.time()-self.start_time1
                    self.time2.insertPlainText(str(t))
        print(self.data1.decode("utf-8"))
    
    def ans_z_file1(self):
        global cp,fname,start_time1,key,mat
        print(self.fname)
        self.cp=self.text2.toPlainText()
        print("The entered password is:"+str(self.cp))
        y=self.fname
        #y=y[:-8]+".zip"+" "+self.cp
        print(y)
        print(self.mat)
        for i in range(len(self.mat)):
            if y in self.mat[i]:
                a1=self.mat[i]
                arr=a1.split(" ")
                print(arr)
                t=0
                if self.cp==arr[1]:
                    print("Password match")
                    self.key=hashlib.sha256(str(self.p).encode("utf-8")).digest()
                    #step 1 decrypt all the files"
                    k=self.fname
                    '''
                    k=self.fname[:-6]
                    os.mkdir(k)
                    with ZipFile(self.fname,'r') as zip:
                        zip.printdir()
                        zip.extractall(k)
                    '''
                    for name in os.listdir(k):
                        self.start_time1=time.time()
                        self.decrypt_file(os.path.join(self.fname,name))
                        t+=time.time()-self.start_time1
                    self.time2.insertPlainText(str(t))
    def ans_p_file1(self):
        global cp,fname,start_time1,mat
        print(self.fname)
        self.cp=self.text2.toPlainText()
        print("The entered password is"+str(self.p))
        y=self.fname[:-4]+" "+self.cp
        print(y)
        print(self.mat)
        t=0
        for i in range(len(self.mat)):
            if y in self.mat[i]:
                a1=self.mat[i]
                arr=a1.split(" ")
                print(arr)
                t=0
                if self.cp==arr[1]:
                    print("Password match")
                    self.key=hashlib.sha256(str(self.p).encode("utf-8")).digest()
                    self.start_time1=time.time()
                    self.decrypt_file(self.fname)
                    t+=time.time()-self.start_time1
                    self.time2.insertPlainText(str(t))
    
    def ans_image(self):
        global fname,img,start_time1,enc,key
        textimage=self.text3.toPlainText()
        d1 = self.stringtochartobinarytoimage(textimage+chr(3))
        print(d1)
        d2 = self.d1arraytod2array(d1)
        print(d2)
        t=0
        self.start_time1=time.time()
        self.key = self.encode(self.img,d2,"encode")
        t+=time.time()-self.start_time1
        self.time3.insertPlainText(str(t))
        print("The encrypted message is"+str(self.key))
        self.enc = cv2.imread("encode.png",cv2.IMREAD_UNCHANGED)
    def ans_image_d(self):
        global fname,img,start_time1,enc
        t=0
        self.start_time1=time.time()
        ki=self.decode(self.enc,self.key)
        t+=time.time()-self.start_time1
        self.time3.insertPlainText(str(t))
        dec=self.imagetobinarytochartostring(ki)
        print("The decrypted message is"+str(dec))
    
    def ans_image1(self):
        global fname,img,start_time1,enc,key,data,data1,res1
        textp=self.text4.toPlainText()
        textp=textp.encode("utf-8")
        p4=self.pass4.toPlainText()
        t=0
        self.start_time1=time.time()
        key1=hashlib.sha256(str(p4).encode("utf-8")).digest()
        self.data=self.encrypt(textp,key1)
        self.res1=self.data.hex()
        #this text has to be encrypted into the image
        self.res1=str(self.res1)
        print(self.res1)
        d1 = self.stringtochartobinarytoimage(self.res1+chr(3))
        print(d1)
        d2 = self.d1arraytod2array(d1)
        print(d2)
        self.key = self.encode(self.img,d2,"encode")
        t+=time.time()-self.start_time1
        self.time4.insertPlainText(str(t))
        print("The encrypted message is"+str(self.key))
        self.enc=cv2.imread("encode.png",cv2.IMREAD_UNCHANGED)
    def ans_image_d1(self):
        global fname,img,start_time1,enc,key
        t=0
        self.start_time1=time.time()
        p5=self.pass4.toPlainText()
        ki=self.decode(self.enc,self.key)
        dec=self.imagetobinarytochartostring(ki)
        print("The decrypted message is"+str(dec))
        key1=hashlib.sha256(str(p5).encode("utf-8")).digest()
        ans1=bytes.fromhex(self.res1)
        #ans1=bytearray.fromhex(self.res1)
        print(ans1)
        dat=self.decrypt(ans1,key1)
        print(dat)
        t+=time.time()-self.start_time1
        self.time3.insertPlainText(str(t))

        
        #ans1=bytearray.fromhex(res1)
        #print(ans1)
        

                
app=QApplication(sys.argv)
frame=MainWindow()
frame.show()
sys.exit(app.exec_())
        
