重要：使用前务必修改当前目录下config.json中imagedir的值，将其改为图片库的路径（包含末尾的分隔符），在windows下也请使用/分隔符，例如"C:/image/"
在查询某个类别的第一张图片时由于需要读入数据，速度较慢，再次查找同类图片速度即恢复正常。
config.json中的fastmode选项用于开启哈希查找，设置为true则速度更快，但是精确度下降。

运行环境：
python 3.6 64-bit

python库(均可使用pip安装)：
tensorflow
numpy(tensorflow安装时会作为依赖安装)
opencv-python
Pillow
tkinter(python默认安装)

使用方式：
windows：py gui.py
linux/mac: python3 gui.py