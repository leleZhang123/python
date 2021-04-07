from PIL import Image

img =  Image.open('day01\pillow\insert.jpg')
#按像素放大二倍
Image.eval(img,lambda x: x*1.2).show()


#按尺寸进行缩放
img2 = img.copy()
#img2.show()
img2.thumbnail((200,160))
img2.show()