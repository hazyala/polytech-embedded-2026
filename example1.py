# import cv2
# frame = cv2.imread("example.jpg",1)
# cv2.imshow("example image", frame)
# cv2.waitKey(0)
# cv2.destoryAllwindows()

import cv2
original=cv2.imread("example.jpg",1)
gray=cv2.imread("example.jpg",0)
unchange = cv2.imread("example.jpg",-1)
dx = cv2.Sobel(original, -1,1,0)
dy = cv2.Sobel(original, -1,0,1)

cv2.imshow("original", original)
cv2.imshow("dx", dx)
cv2.imshow("dy", dy)

cv2.waitKey(0)
cv2.destroyAllWindows()
