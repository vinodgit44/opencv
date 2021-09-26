import cv2
import cv2 as cv
import numpy as np
##image stacking
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
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv.cvtColor(imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver
path = './images/shapes.png'
img = cv.imread(path)

print(img.shape)

def getcontour(img):
    contour,hierarchy=cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    for cnt in contour:
        area=cv.contourArea(cnt) #####getting contour area

        if area>1000:
            cv.drawContours(imgcontour, cnt, -1, (255, 0, 0), 1)####drawing contours
            print(area)
            peri=cv.arcLength(cnt,True) ####getting perimeter
            print(peri)
            approx=cv.approxPolyDP(cnt,.02*peri,True) ####getting no. of corners
            print(len(approx))
            ####getting bounding box.
            objcor=len(approx)
            x, y, w, h =cv.boundingRect(approx)
            cv.rectangle(imgcontour,(x,y),(x+w,y+h),(0,0,0),3)

           #####identifying object according to corners
            if objcor ==3: objecttype="tri"
            elif objcor==4:
                aspRatio = w / float(h)
                if aspRatio > 0.98 and aspRatio < 1.03:
                    objecttype = "Square"
                else:
                    objecttype = "Rectangle"

            else :  objecttype="circle"
            cv.putText(imgcontour,objecttype,(x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.5,
                        (0,0,0),2)



img = img[5:253,3:194]
im_gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
im_blur=cv.GaussianBlur(im_gray,(3,5),0)
im_canny=cv.Canny(im_gray,50,50)
im_blank=np.zeros_like(img)
imgcontour=img.copy()
getcontour(im_canny)
imgstack=stackImages(0.9,([img,im_gray,im_blur,],[im_canny,imgcontour,im_blank]))
cv.imshow("image",imgstack)
# cv.imshow("gray",im_gray)
# cv.imshow("blur",im_blur)
cv.waitKey(0)