# -*- coding: UTF-8 -*-
import Tkinter as tk
import tkFileDialog
from PIL import Image
import glob
import os
import tensorflow as tf
import numpy as np
import cv2
import cuhk03_dataset
from operation import *

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.rowconfigure(0, minsize=100)
        self.rowconfigure(1, minsize=248)
        self.rowconfigure(3, minsize=248)
        # self.columnconfigure(3, minsize=100)
        # self.columnconfigure(0, pad=20)
        self.createWidgets()

        self.operator = Operation()
        self.result = []
        self.gifresult = []
        self.similarity = []
        self.gif_file = '/workspace/zyf/Image/resize_gif/'
        self.filetemp = '/workspace/zyf/Image/temp/'

        self.image_show = []


    def createWidgets(self):
        self.resetButton = tk.Button(self, text='SearchInTest_query', command=self.resetImage)
        self.resetButton.grid(row=0,column=0,columnspan = 2)

        self.openfile = tk.Button(self, text='SelectImage', command=self.openFile)
        self.openfile.grid(row=0, column=3)



        file = '/workspace/zyf/Image/'
        self.image_files_gif = sorted(glob.glob(os.path.join(file, '*.gif')))
        self.colcut = 8
        self.labels = []
        self.labels_sim = []
        image_haha = '/workspace/zyf/Image/someuse/bg.gif'

        for i, image_name in enumerate(self.image_files_gif):

            label = int(i/self.colcut);
            if label == 0:
                row_image = 1;
                row_text = 2;
            else :
                row_image = 3;
                row_text = 4;
            bm = tk.PhotoImage(file=image_haha)
            self.labels.append(tk.Label(self, image=bm))
            self.labels[i].bm = bm
            self.labels[i].pack()
            self.labels[i].grid(row=row_image,column=i%self.colcut, sticky=tk.W+tk.E+tk.N+tk.S)

            if i == 0:
                self.labels_sim.append(tk.Label(self, text='SearchImage'))
            else:
                self.labels_sim.append(tk.Label(self, text='Similarity'))
            self.labels_sim[i].grid(row=row_text,column=i%self.colcut, sticky=tk.W+tk.E+tk.N+tk.S)

    def resetImage(self):

        self.result = self.operator.function()
        print self.result
        self.jpg2gif()

        self.image_show = []
        self.sim_show = []
        for i, image_name in enumerate(self.gifresult):
            if(i == 0):
                self.image_show.append(tk.PhotoImage(file=self.path_gif))
                self.labels[i]['image'] = self.image_show[i]

                self.sim_show.append('SearchImage')
                self.labels_sim[i]['text'] = self.sim_show[i]
            else:
                self.image_show.append(tk.PhotoImage(file=image_name))
                self.labels[i]['image'] = self.image_show[i]

                temp_sim = str(round(self.similarity[i-1]*100,4))
                self.sim_show.append('Similarity='+temp_sim+'%')
                self.labels_sim[i]['text'] = self.sim_show[i]


    def openFile(self):
        self.fileName = tkFileDialog.askopenfilename(
            filetypes=[("JPG", ".jpg"), ("GIF", ".gif"), ("PNG", ".png"), ("Python", ".py")])
        self.operator.file_address = self.fileName
        img_tmp = cv2.imread(self.fileName)
        img_tmp = cv2.resize(img_tmp, (120, 248), interpolation=cv2.INTER_CUBIC)
        path_temp = os.path.join(self.filetemp, self.fileName.split('/')[-1])
        cv2.imwrite(path_temp, img_tmp)
        im = Image.open(path_temp)
        self.path_gif = path_temp.split('.')[0] + '.gif'
        im.save(self.path_gif)

        if len(self.image_show)==0:
            self.image_show.append(tk.PhotoImage(file=self.path_gif))
        else:
            self.image_show[0] = tk.PhotoImage(file=self.path_gif)
        self.labels[0]['image'] = self.image_show[0]



    def jpg2gif(self):
        self.gifresult = ['']
        self.similarity = []
        for item in self.result:
            temp_file = item[0].split('/')[-1].split('.')[0]
            temp_file_gif = os.path.join(self.gif_file,temp_file+'.gif')
            self.gifresult.append(temp_file_gif)
            self.similarity.append(item[1])
        print self.gifresult
        print self.similarity




if __name__ == "__main__":

    app = Application()
    app.master.title('Sample application')
    app.mainloop()