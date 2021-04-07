from PIL import Image
img1  = Image.open("pillow\insert.jpg")
#img1.rotate(90).show()
#格式转换
#img1.transpose(Image.FLIP_TOP_BOTTOM).show()#上下执行滤镜
#img1.transpose(Image.FLIP_LEFT_RIGHT).show()#左右执行滤镜
img1.transpose(Image.ROTATE_90).show()#90 度的旋转