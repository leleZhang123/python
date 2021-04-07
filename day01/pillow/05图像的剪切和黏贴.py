from PIL import Image
img1 = Image.open('day01\pillow\he.jpg') 
 #复制
imgb = img1.copy()
imgc = img1.copy()
#剪切
img_2 = imgb.crop((50,50,120,120))
img_2.show()
#黏贴
imgc.paste(img_2,(30,30))
imgc.show()





