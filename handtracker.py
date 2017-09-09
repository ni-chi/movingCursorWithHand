import numpy as np
import cv2
from pymouse import PyMouse
import tkinter as tk
root = tk.Tk()
global screen_width,screen_height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

cap = cv2.VideoCapture(0)
global roi,roihsv
global windowHeight,windowHeight,heightMid,widthMid
global mouseObject

mouseObject = PyMouse()


 
while(True):
    ret, frame = cap.read()
    rows,cols=frame.shape[:2]
    windowHeight = rows/2
    windowWidth = cols/4
    widthMid = cols/2
    heightMid = rows/2

    cv2.rectangle(frame,(widthMid-windowWidth/2,heightMid-windowHeight/2),(widthMid+windowWidth/2,heightMid+windowHeight/2),(0,255,0),3)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
    	roi=frame[heightMid-windowHeight/2:heightMid+windowHeight/2,widthMid-windowWidth/2:widthMid+windowWidth/2]
    	roihsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
        break

lowLimit = np.array((0.,60.,32.))
highLimit = np.array((180.,255.,255.))
mask = cv2.inRange(roihsv,lowLimit,highLimit)
window=(widthMid-windowWidth/2,heightMid-windowHeight/2,windowWidth,windowHeight)


roiHist = cv2.calcHist([roihsv],[0],mask,[180],[0,180])
cv2.normalize(roiHist,roiHist,0,255,cv2.NORM_MINMAX)
terminationCriteria = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS , 10, 1)

mouseObject.move(screen_width/2,screen_height/2)
while True:
	ret,frame = cap.read()
	

	if ret:

		frameHsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		backprojectedFrame = cv2.calcBackProject([frameHsv], [0], roiHist, [0, 180], 1)

		mask = cv2.inRange(frameHsv, lowLimit, highLimit)
		backprojectedFrame &= mask

		ret, window = cv2.meanShift(backprojectedFrame, window, terminationCriteria)
		

		windowCol, windowRow = window[:2]
		mouseObject.move(683+(cols-4*(windowCol + windowWidth)/2),384-(rows-3*(windowRow + windowHeight)/2))
		frame = cv2.rectangle(frame, (windowCol, windowRow), (windowCol + windowWidth, windowRow + windowHeight), 255, 2)

		cv2.flip(frame,1)
		cv2.imshow('meanshift', frame)
		k = cv2.waitKey(60) & 0xff

		if k==27:
			break
	else:
		break





cap.release()
cv2.destroyAllWindows()