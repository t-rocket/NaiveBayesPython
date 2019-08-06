#!/usr/bin/python2

import tkinter
import os
import re

import numpy as np
import pandas as pd

import cv2

from tkinter import ttk
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from os import listdir
from os.path import isfile, join

categories = ["daisy", "dandelion", "rose", "sunflower", "tulip"]
dictionary_flowers = {"daisy": 0, "dandelion": 0, "rose": 0, "sunflower": 0, "tulip": 0}


def openDirectory():
    name = askdirectory()
    return (name)

def OpenFileName():
    name = askopenfilename(initialdir="C:/",
                           filetypes =(("Text File", ".txt"),("All Files",".*")),
                           title = "Choose a file."
                           )
    return (name)

def setModelLocation():
    name = OpenFileName()
    #tf_model.delete(0,'end')
    #tf_model.insert(0,name)

def setUnClassifiedLocation():
    path = openDirectory()
    tf_directoryPath.delete(0,'end')
    tf_directoryPath.insert(0,path)

    train_file_path = path + "/train.csv"
    structure_file_path = path + "/Structure.txt"
    test_file_path = path + "/test.csv"

    if (os.path.exists(test_file_path) == False):
        print "test file not exist"
    if (os.path.exists(structure_file_path) == False):
        print "test file not exist"
    if (os.path.exists(train_file_path) == False):
        print "test file not exist"

    if (os.path.exists(train_file_path) == False or os.path.exists(structure_file_path) == False or os.path.exists(test_file_path) == False):
        btn_Classify.config(state='disabled')
    else:
        btn_Classify.config(state='normal')

def runPredict():
    print("hey");


def write_prediction(file_name, prediction):
    with open("prediction_file.csv", "a") as file:
        file.write(file_name+","+prediction+"\n")

def train_model():
    path = tf_directoryPath.get()
    train_file_path = path + "/train.csv"
    structure_file_path = path + "/Structure.txt"
    test_file_path = path + "/test.csv"

    file = open(structure_file_path, 'r')
    attribute_columns = {}
    for line in file:
        attributes = re.search('^@ATTRIBUTE\s+(.+?)\s+(.*)$', line)
        attribute_name = attributes.group(1)
        if (attributes.group(2)[0] == '{' and attributes.group(2)[-1] == '}'):
            attribute_columns[attribute_name] = attributes.group(2)[1:-1].split(',')
        else:
            attribute_columns[attribute_name] = attributes.group(2)

    df = pd.read_csv(train_file_path)
    df.replace('', np.nan, inplace = True)

    print df.dtypes
    for key in attribute_columns.keys():
        data = attribute_columns[key];
        if (data == 'NUMERIC'):
            print key
            print data
            print pd.cut(df[key].dropna(),3,labels = range(1,4))
        else:
            must_common = df[key].value_counts().argmax()
            df.replace(np.nan, must_common, inplace=True)

#    print df


root = tkinter.Tk()
root.title('Window Name')
root.geometry('600x400')


label1 = ttk.Label(root,text='Directory Path')
label1.place(x=20, y=30)

tf_directoryPath = ttk.Entry(root,width=50)
tf_directoryPath.place(x=20, y=50)



btn_borwseDirectoryPath = ttk.Button(root,text='Browse',command=setUnClassifiedLocation)
btn_borwseDirectoryPath.place(x=350, y=47.5)

label2 = ttk.Label(root,text='Discretization Bins')
label2.place(x=20, y=100)

tf_DiscretizationBins = ttk.Entry(root,width=50)
tf_DiscretizationBins.place(x=20, y=120)

btn_Build = ttk.Button(root,text='Classify',command=runPredict,state='disabled')
btn_Build.place(x=300, y=200)

btn_Classify = ttk.Button(root,text='Build',command=train_model,state='disabled')
btn_Classify.place(x=205, y=200)

root.mainloop()