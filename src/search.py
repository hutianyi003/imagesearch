'''
find top ten most similar pictures of the input
'''

import src.label_image as label_image
import numpy as np
import os
import cv2
import json
from datasketch import MinHashLSHForest, MinHash

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
    
def get_prefilename(label):
    with open(datapath+'label.json', 'r') as f:
        data = json.load(f)
        return data['label_to_filepre'][label]
    return ''
    
def search(path,searchfile):
    ans = label_image.getlabel(searchfile)
    inputfeature = label_image.computefeature(searchfile)
    '''
    m_input = MinHash()
    m_input.update()
    '''

    prefilename = get_prefilename(ans)

    candidate = []
    
    files = os.listdir(datapath+'bottleneck/')
    for i in files:
        sl = i.split('_')
        if sl[0] == prefilename:
            candidate.append(
                (sl[0] + '_' + sl[1], getfeature(datapath + 'bottleneck/' + i)))
    
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
