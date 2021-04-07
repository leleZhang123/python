from PIL import Image
img = Image.open("E:\python\day01\pillow\insert.jpg")
img.show()#将图片展示出来
print('图片格式',img.format)
print('图片大小',img.size)
print('高度',img.height,'宽度',img.width)
print('图片的像素值',img.getpixel((100,100)))#得到某位置的像素值的rgb值