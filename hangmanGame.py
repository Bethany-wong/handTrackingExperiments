import random

import cv2
import time
import os
import handTrackingModule as htm
import morseTree as morse
import numpy as np
import hangmanResources as resource

def updateGuessedWord(answer, guessedWord, guess):
    for position in range(len(answer)):
        letter = answer[position]
        if letter == guess:
            guessedWord[position] = letter
            return guessedWord

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

print("Hello")

# parameters
numDot = 1 # number of fingers detected to represent a dot (thumb not included)
numDash = 4 # same for dash
detectAlphabetAfter = 35 # interpret code after period of inactivity

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
lastState = 0 # last detected gesture (0, 1, 5)
cnt = 0 # no. frames of the latest state
detected = False # already detected alphabet after period of inactivity
noHandCount = 0

# game variables
stages = resource.stages
lives = len(stages)
answer = random.choice(resource.wordList)
print(f"answer is {answer}")
guessedWord = ['_' for _ in range(len(answer))]
wrongGuesses = []

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
                        if alphabet in answer:
                            guessedWord = updateGuessedWord(answer, guessedWord, alphabet)
                        elif alphabet not in wrongGuesses:
                            print("Wrong guess")
                            wrongGuesses.append(alphabet)
                            lives -= 1
                            if lives == 0:
                                break
                        else:
                            print("You've already guessed the letter")
                    else:
                        print("Invalid morse code")
                    code = ""
                    print("reset")
        else:
            lastState = totalFingers
            cnt = 0
            detected = False
            print(code)

        displayCurrentSymbol(totalFingers)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f"FPS: {int(fps)}", (400, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0))
    cv2.putText(img, str(guessedWord), (10, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 10)
    cv2.putText(img, str(guessedWord), (10, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 128, 255), 6)
    cv2.putText(img, stages[len(stages) - lives], (10, 300), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 10)

    cv2.imshow("Image", img)
    cv2.waitKey(1)


# end of game
if lives == 0:
    cv2.putText(img, "You lose", (10, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 128, 255), 6)
else:
    cv2.putText(img, "You won", (10, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 128, 255), 6)