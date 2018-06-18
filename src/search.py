'''
find top ten most similar pictures of the input
'''

import label_image
import numpy as np
import os
import cv2

feature_list = dict()
imagepath = './image/'
datapath = './data/'

def config(input_imagepath,input_datapath):
    global imagepath
    global datapath
    imagepath = input_imagepath
    datapath = input_datapath
    label_image.set_path(datapath)
    
def getfeature(filename):
    global feature_list
    if filename in feature_list:
        return feature_list[filename]
    f = open(filename,'r')
    feature = np.array([])
    l = f.readline().split(",")
    for i in range(2048):
        feature = np.append(feature,[float(l[i])])
    feature_list[filename] = feature
    return feature

def distance(v1, v2):
    return np.linalg.norm(v1-v2)
    
class_feature = dict()
def search(path,filename):
    global class_feature
    ans = label_image.getlabel(path+filename)
    inputfeature = label_image.computefeature(path+filename)
    path = imagepath+ans+"/"
    result = []
    for file in class_feature[ans]:
        feature = class_feature[ans][file]
        result.append([file, distance(feature, inputfeature)])
    result = sorted(result, key = lambda x: x[1])
    return result[0:10],ans
    
def load_features(path,filelist):
    global class_feature
    for i in filelist:
        feature = label_image.computefeature(path+i)
        label = label_image.getlabel(path+i)
        if label not in class_feature:
            class_feature[label] = dict()
        class_feature[label][i] = feature
        

if __name__ == '__main__':
    path ='tf_files/ProjectTestData/ir/' 
    output_path = 'tf_files/queryresult.txt'
    o = open(output_path,"w")
    limit = 0
    search_list = []
    for file in os.listdir(path):
        search_list.append((file,int(file.split(".")[0])))
    search_list = sorted(search_list, key = lambda x: x[1])
    load_features(path,search_list)
    for file in search_list:
        file = file[0]
        r,c = search(path, file)
        temp = ''
        temp += file + ':'
        for i in range(10):
            temp+= r[i][0]
            if i == 9:
                temp+='\n'
            else:
                temp+=','
        #o.write(temp)
        print(temp)
        print(limit)
        if limit > 10:
            break
        limit+=1