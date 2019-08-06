#!/usr/bin/python2

import tkinter
import os
import re
import tkMessageBox


import numpy as np
import pandas as pd



from tkinter import ttk
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from os.path import isfile, join

data_structure = {}
df_train = ""
df_test = ""

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
        btn_Build.config(state='disabled')
    else:
        btn_Build.config(state='normal')

def runPredict():

    try:
        num_of_bins = int(tf_DiscretizationBins.get())
        if num_of_bins < 0:
            raise ValueError("Negative integer")
    except ValueError:
        tkMessageBox.showerror("Naive Bayes Classifier","Please enter a positive integer")


    path = tf_directoryPath.get()
    test_file_path = path + "/train.csv"

    df_test = prepare_data(test_file_path,num_of_bins)


    NaiveBayesClassifier()


def write_prediction(file_name, prediction):
    with open("prediction_file.csv", "a") as file:
        file.write(file_name+","+prediction+"\n")

def NaiveBayesClassifier():
    global df_train
    global df_test
    global data_structure

    print data_structure
    class_probabilities = {}
  #  for classification in data_structure['class']:
  #      print df_train.loc[(df_train['class'] == classification)]


def load_structure(structure_file_path):
    file = open(structure_file_path, 'r')
    data_structure = {}

    for line in file:
        attributes = re.search('^@ATTRIBUTE\s+(.+?)\s+(.*)$', line)
        attribute_name = attributes.group(1)
        if (attributes.group(2)[0] == '{' and attributes.group(2)[-1] == '}'):
            data_structure[attribute_name] = attributes.group(2)[1:-1].split(',')
        else:
            data_structure[attribute_name] = attributes.group(2)

    return data_structure

def prepare_data(data_path,num_of_bins):
    df = pd.read_csv(data_path)

    for key in data_structure.keys():
        data = data_structure[key]
        df[key].replace('', np.nan, inplace=True)
        if (data == 'NUMERIC'):
            key_mean_value = df.pivot_table(key, columns='class', aggfunc='mean')
            for classification in data_structure['class']:
                df.loc[(df['class'] == classification) & (np.isnan(df[key])), key] = key_mean_value[classification][key]

            df[key] = pd.cut(df[key], bins=num_of_bins, labels=range(1, num_of_bins + 1), include_lowest=True)
        else:
            must_common = df[key].value_counts().argmax()
            df[key].replace(np.nan, must_common, inplace=True)



    return df

def train_model():
    global df_train
    global data_structure
    try:
        num_of_bins = int(tf_DiscretizationBins.get())
        if num_of_bins < 0:
            raise ValueError("Negative integer")
    except ValueError:
        tkMessageBox.showerror("Naive Bayes Classifier","Please enter a positive integer")

    path = tf_directoryPath.get()

    train_file_path = path + "/train.csv"
    structure_file_path = path + "/Structure.txt"
    data_structure = load_structure(structure_file_path)
    df_train = prepare_data(train_file_path,num_of_bins)
    btn_Classify.config(state='normal')


root = tkinter.Tk()
root.title('Naive Bayes Classifier')
root.geometry('600x400')

label1 = ttk.Label(root, text='Directory Path')
label1.place(x=20, y=30)

tf_directoryPath = ttk.Entry(root, width=50)
tf_directoryPath.place(x=20, y=50)
tf_directoryPath.insert(0, "d:/documents/users/talmalu/Documents/Work")

btn_borwseDirectoryPath = ttk.Button(root, text='Browse', command=setUnClassifiedLocation)
btn_borwseDirectoryPath.place(x=350, y=47.5)

label2 = ttk.Label(root, text='Discretization Bins')
label2.place(x=20, y=100)

tf_DiscretizationBins = ttk.Entry(root, width=50)
tf_DiscretizationBins.place(x=20, y=120)
tf_DiscretizationBins.insert(0, "3")

btn_Build = ttk.Button(root, text='Build', command=train_model, state='normal')
btn_Build.place(x=205, y=200)

btn_Classify = ttk.Button(root,text='Classify',command=runPredict,state='disabled')
btn_Classify.place(x=300, y=200)

root.mainloop()