import cv2
import time
import os
import handTrackingModule as htm
import morseTree as morse
import numpy as np

# parameters
numDot = 1 # number of fingers detected to represent a dot (thumb not included)
numDash = 4 # same for dash
addSpaceAfter = 100 # append a space after certain frames of inactivity
detectAlphabetAfter = 35 # interpret code after period of inactivity

def detectNumbers(lmList):
    tipIds = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinkie
    fingers = []
    for id in range(1, 5): # other fingers
        # compare fingertip height to palm and finger intersection height
        if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers


def displayCurrentSymbol(fingerCnt):
    if fingerCnt == numDot:
        h, w, c = dotImage.shape
        img[0:h, 0:w] = dotImage
    elif fingerCnt == numDash:
        h, w, c = dashImage.shape
        img[0:h, 0:w] = dashImage
    else:
        h, w, c = holdImage.shape
        img[0:h, 0:w] = holdImage


wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

dotImage = cv2.imread("dot_dash_symbol/dot.png")
dashImage = cv2.imread("dot_dash_symbol/dash.jpg")
holdImage = cv2.imread("dot_dash_symbol/hold.png")

pTime = 0 # previous time
detector = htm.handDetector(detectionCon=0.75)
code = ""
currWord = ""
lastState = 0 # last detected gesture (0, 1, 5)
cnt = 0 # no. frames of the latest state
detected = False # already detected alphabet after period of inactivity
noHandCount = 0
#inactivityBar = 400

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # mirror the image
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = detectNumbers(lmList)
        totalFingers = fingers.count(1)  # number of fingers detected
        if totalFingers == lastState:    # gesture is same as last frame
            cnt += 1
            if totalFingers == numDot and cnt == 3: # write a dot after detection in 3 consecutive frames
                code += "."
            elif totalFingers == numDash and cnt == 3: # same for dash
                code += "-"
            else:
                if cnt > detectAlphabetAfter and detected == False: # detect alphabet after period of inactivity
                    detected = True
                    alphabet = morse.traverse_morse_tree(code)
                    print(alphabet)
                    if alphabet != None:
                        currWord += alphabet
                    code = ""
                    print("reset")
                elif cnt > addSpaceAfter and len(currWord) > 0 and currWord[-1] != " ": # add a space after period of inactivity
                    print("New Word")
                    currWord += " "
        else:
            lastState = totalFingers
            cnt = 0
            detected = False
            print(code)
            alphabet = morse.traverse_morse_tree(code)
            if alphabet == None:
                code = ""
                print("reset")
            elif len(code) == 4:
                currWord += alphabet
                code = ""
                print("reset")

        displayCurrentSymbol(totalFingers)
        #inactivityBar = np.interp(cnt, [50, 300], [0, 100])


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f"FPS: {int(fps)}", (400, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0))
    cv2.putText(img, currWord, (10, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 10)
    cv2.putText(img, currWord, (10, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 128, 255), 6)
    #cv2.rectangle(img, (50, 150), (85, 150+addSpaceAfter), (255, 0, 0), 3)  # frame of volume bar
    #cv2.rectangle(img, (50, int(inactivityBar)), (85, 150+addSpaceAfter), (255, 0, 0), cv2.FILLED)

    cv2.imshow("Image", img)
    cv2.waitKey(1)