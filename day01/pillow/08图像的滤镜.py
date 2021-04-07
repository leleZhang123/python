from PIL import Image,ImageFilter

img = Image.open("pillow\he.jpg")
w,h = img.size
img_output = Image.new('RGB',(2*w,h))
img_output.paste(img,(0,0))

img_filter1 = img.filter(ImageFilter.GaussianBlur)
img_output.paste(img_filter1,(w,0))
img_output.show()