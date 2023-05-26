import cv2
import time
import os
import handTrackingModule as htm

def detectNumbers(lmList):
    fingers = []
    # Thumb
    if lmList[1][1] > lmList[17][1]:  # right hand
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:  # check if tip is right of knuckle
            fingers.append(1)
        else:
            fingers.append(0)
    else:  # left hand
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:  # check if tip is left of knuckle
            fingers.append(1)
        else:
            fingers.append(0)

    for id in range(1, 5): # other fingers
        # compare fingertip height to palm and finger intersection height
        if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers


wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "fingerImages"
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

pTime = 0 # previous time

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20] # thumb, index, middle, ring, pinkie


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # mirror the image
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = detectNumbers(lmList)
        totalFingers = fingers.count(1)  # find numbers of 1s in the list
        print(totalFingers)
        h, w, c = overlayList[totalFingers-1].shape
        img[0:h, 0:w] = overlayList[totalFingers-1] # print respective finger image, zero would be last image

        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED) # rectangle background
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25) # display number

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f"FPS: {int(fps)}", (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0))

    cv2.imshow("Image", img)
    cv2.waitKey(1)
