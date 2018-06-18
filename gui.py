from tkinter import *
import cv2
from PIL import Image, ImageTk
from tkinter import filedialog
import src.search
import json

datapath = './data/'
imagepath = './image/' 
needtosearch = ''
fastmode = True

def imageShow():
    default_dir = r'/Users/'
    fname = filedialog.askopenfilename(initialdir = (default_dir))
    global needtosearch
    needtosearch = fname
    img=Image.open(fname)
    if img is None:
        return
    nheight=img.height
    if nheight>200:
        nheight=200
    nwidth=int(nheight*img.width/img.height)
    if nwidth>200:
        nheight=int(200*nheight/nwidth)
        nwidth=200
    img=img.resize((nwidth,nheight),Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
    imageCanvas.image=photo
    imageCanvas.create_image(100,100,image=photo)

def search():
    #将查询图片名保存在filename里
    filename = src.search.search(imagepath,needtosearch)
    path = imagepath
   
    for index in range(len(filename)):
        img=Image.open(path+filename[index][0])
        if img is None:
            continue
        nheight=img.height
        if nheight>100:
            nheight=100
        nwidth=int(nheight*img.width/img.height)
        if nwidth>80:
            nheight=int(80*nheight/nwidth)
            nwidth=80
        img=img.resize((nwidth,nheight),Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
        imageMatrix[index].image=photo
        imageMatrix[index].create_image(50,40,image=photo)


#get config
with open("config.json", "r") as f:
    config = json.load(f)
    if "imagedir" not in config:
        print("No imagedir!")
        exit()
    if "datadir" not in config:
        print("No datadir!")
        exit()
    imagepath = config["imagedir"]
    datapath = config["datadir"]
    fastmode = config["fastmode"]
    src.search.config(imagepath, datapath, fastmode)

root=Tk(className="图像检索")


imageCanvas = Canvas(root,width=200,height=200)
imageCanvas.grid(row=0,column=3,columnspan=2)
Button(root,text='choice',command=imageShow,width=5).grid(row=0,column=0)#选择查询图片
Button(root,text='search',command=search,width=5).grid(row=0,column=1)#查询
Button(root,text='exit',command=quit,width=5).grid(row=0,column=2)#退出

imageMatrix=[]
for row in range(1,3):
    for col in range(5):
        canvas=Canvas(root,width=100,height=80)
       # canvas.create_rectangle(2,2,101,80,outline='black')
        imageMatrix.append(canvas)
        canvas.grid(row=row,column=col)


root.mainloop()
