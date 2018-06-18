'''
find top ten most similar pictures of the input
'''

import src.label_image as label_image
import numpy as np
import os
import cv2
import json
from src.lshash import LSHash

feature_list = dict()
imagepath = './image/'
datapath = './data/'
fastmode = True
file_by_class = dict()
hash_by_class = dict()

def config(input_imagepath,input_datapath,input_fastmode):
    global imagepath
    global datapath
    global fastmode
    imagepath = input_imagepath
    datapath = input_datapath
    fastmode = input_fastmode
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
    
def get_prefilename(label):
    with open(datapath+'label.json', 'r') as f:
        data = json.load(f)
        return data['label_to_filepre'][label]
    return ''
    
def load_filelists():
    global file_by_class
    with open(datapath + 'imagelist.txt','r') as f:
        files = f.readlines()
        files = [x.strip() for x in files]
        for file in files:
            pre = file.split('_')[0]
            if pre not in file_by_class:
                file_by_class[pre] = []
            file_by_class[pre].append(file)

def load_hash(tag):
    files = file_by_class[get_prefilename(tag)]
    hash_by_class[tag] = LSHash(6, 2048)
    table = hash_by_class[tag]
    for i in files:
        table.index(getfeature(datapath+'bottleneck/'+i+'_inception_v3.txt'),i)
    
have_load_file = False
def search(path,searchfile):
    global have_load_file
    if have_load_file == False:
        load_filelists()
        have_load_file = True
    ans = label_image.getlabel(searchfile)
    inputfeature = label_image.computefeature(searchfile)

    candidate = []
    
    if fastmode:
        if ans not in hash_by_class:
            load_hash(ans)
        temp = hash_by_class[ans].query(inputfeature, num_results = 500)
        for i in temp:
            candidate.append((i[0][1], getfeature(datapath + 'bottleneck/' + i[0][1]+'_inception_v3.txt')))

    else:
        files = file_by_class[get_prefilename(ans)]
        for i in files:
            candidate.append((i, getfeature(datapath + 'bottleneck/' + i+'_inception_v3.txt')))
    
    result=[]

    for i in candidate:
        result.append([i[0], distance(i[1], inputfeature)])
    result = sorted(result, key = lambda x: x[1])
    return result[0:10]
    
if __name__ == '__main__':
    path ='tf_files/ProjectTestData/ir/' 
    output_path = 'tf_files/queryresult.txt'
    o = open(output_path,"w")
    limit = 0
    search_list = []
    for file in os.listdir(path):
        search_list.append((file,int(file.split(".")[0])))
    search_list = sorted(search_list, key = lambda x: x[1])
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
