import cv2
import numpy as np
import HandTrackingModule as htm
brushThickness = 25
drawColor = (255, 0, 255)
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.65,maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
  success, img = cap.read()
  img = cv2.flip(img, 1)
  img = detector.findHands(img)
  lmList = detector.findPosition(img, draw=False)

  if len(lmList) != 0:
    x1, y1 = lmList[8][1:]
    x2, y2 = lmList[12][1:]
    fingers = detector.fingersUp()
    if fingers[1] and fingers[2] == False:
      cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
      if xp == 0 and yp == 0:
        xp, yp = x1, y1

        cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)

        xp, yp = x1, y1

  imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
  _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
  imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
  img = cv2.bitwise_and(img,imgInv)
  img = cv2.bitwise_or(img,imgCanvas)
  cv2.imshow("Image", img)
  cv2.imshow("Canvas", imgCanvas)
  cv2.imshow("Inv", imgInv)
  cv2.waitKey(1)
