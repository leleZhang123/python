from PIL import Image

img1 = Image.open('pillow\he.jpg')
img2 = Image.open('pillow\insert.jpg')
img2 = img2.resize(img1.size)
#分离
r2,g2,b2 = img1.split()
r1,g1,b1 = img2.split()
tem=[r1,g2,b1]
img = Image.merge('RGB',tem)
img.show()