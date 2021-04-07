from PIL import Image
img1 = Image.open('day01\pillow\insert.jpg')
img2 = Image.open('day01\pillow\he.jpg')
img2 = img2.resize(img1.size)#将img2 的图片大小设为img 的大小
r,g,b = img2.split()#将img2 的管道切分为rgb
Image.composite(img2,img1,g).show()#图片遮罩img在img2的b管道