import cv2
import numpy as np

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def getConters(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE )
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 10:
            print(area)
            cv2.drawContours(imgContourB, cnt, -1, (255, 0, 0), 2)
            # cv2.drawContours(imgContourY, cnt, -1, (203, 255, 0), 1)
            peri = cv2.arcLength(cnt, True)
            print(peri)
            approx = cv2.approxPolyDP(cnt, 0* peri, True )
            print(len(approx))

            objCor = len(approx)
            x, y , w, h = cv2.boundingRect(approx)
            
            # objectType = "Crater"
            # cv2.putText(imgContour, objectType,
            #             (x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7,
            #             (0, 0, 0), 2)

            cv2.rectangle(imgContourY, (x,y),(x+w,y+h), (0,255,0 ), 2)








path ='Resources/robin19.png'
img =cv2.imread(path)
imgContourB = img.copy()
imgContourY = img.copy()

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur =  cv2.GaussianBlur(imgGray, (3,3), 3)
imgBlur2 =  cv2.GaussianBlur(imgGray, (7,7), 2)
imgCanny = cv2.Canny(imgBlur2,70, 50 )
getConters(imgCanny)

##### circle detection
# detected_circles = cv2.HoughCircles(imgBlur2,
#                    cv2.HOUGH_GRADIENT, 2, 20, param1 = 50,
#                param2 = 30, minRadius = 1, maxRadius = 30)
# # Draw circles that are detected.
# if detected_circles is not None:
#
#     # Convert the circle parameters a, b and r to integers.
#     detected_circles = np.uint16(np.around(detected_circles))
#
#     for pt in detected_circles[0, :]:
#         a, b, r = pt[0], pt[1], pt[2]
#
#         # Draw the circumference of the circle.
#         cv2.circle(imgContourY, (a, b), r, (0, 255, 0), 2)
#
#         # Draw a small circle (of radius 1) to show the center.
#         cv2.circle(imgContourB, (a, b), 1, (0, 0, 255), 3)
#         # cv2.imshow("Detected Circle", img)


# 50cv2.imshow("original", img)
# cv2.imshow("Gray", imgGray)
# cv2.imshow("Blur", imgBlur)
# cv2.imshow("Blur2", imgBlur2)
# cv2.imshow("canny ", imgCanny)


imgStack = stackImages(0.8, ([img, imgContourB, imgContourY],
                             [img, imgBlur2, imgCanny]))
cv2.imshow("stack ", imgStack)

cv2.waitKey(0)