import cv2 as cv
src = cv.imread("day02\opencv\he.jpg")
cv.namedWindow("input ", cv.WINDOW_AUTOSIZE)
cv.imshow("input ",src)
cv.waitKey()
cv.destoryAllWindows()