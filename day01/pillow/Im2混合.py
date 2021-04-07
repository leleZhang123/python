from PIL import Image
img  = Image.open('day01\pillow\insert.jpg').convert(mode='RGB')#将图片的模型设置为rgb
img2 =Image.new('RGB',img.size,'#09e568')#图像新建一的类型为rgb的图片，图片的大小，图片的颜色
Image.blend(img,img2,alpha=0.5).show()#将img2和img混合起来并且透明度为0.5