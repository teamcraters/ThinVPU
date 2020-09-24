import numpy as np
import cv2


path ='Resources/moon22.png'

img =cv2.imread(path)

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur3 = cv2.medianBlur(imgGray, 5)
# imgBlur =  cv2.GaussianBlur(imgGray, (3,3), 3)
# imgBlur2 =  cv2.GaussianBlur(imgGray, (7,7), 2)
imgCanny = cv2.Canny(imgBlur3,70, 50 )

circles = cv2.HoughCircles(imgBlur3, cv2.HOUGH_GRADIENT, 1, 20,
                          param1=50, param2=20, minRadius=1, maxRadius=30)


# output = img.copy()
# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# gray = cv.medianBlur(gray, 5)
# circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 20,
#                           param1=50, param2=30, minRadius=0, maxRadius=0)
detected_circles = np.uint16(np.around(circles))
for (x, y ,r) in detected_circles[0, :]:
    cv2.circle(img, (x, y), r, (0, 0, 255), 3)
    cv2.circle(img, (x, y), 1, (0, 255, 255), 3)


cv2.imshow('output',img)
cv2.waitKey(0)
# cv.destroyAllWindows()