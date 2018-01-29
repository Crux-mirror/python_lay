#code=utf-8

from PIL import Image
im = Image.open('C:\\Users\\30\\Desktop\\emoji.jpg')
print im.format,im.size,im.mode
print dir(im)

