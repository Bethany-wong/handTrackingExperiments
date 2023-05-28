import random

import cv2
import time
import os
import handTrackingModule as htm
import morseTree as morse
import numpy as np
import hangmanResources as resource

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
lives = 7
answer = random.choice(resource.wordList).upper()
print(f"answer is {answer}")
guessedWord = ['_' for _ in range(len(answer))]
wrongGuesses = []
stagesList = []
for imPath in os.listdir("hangmanImages"):
    image = cv2.imread(f'hangmanImages/{imPath}')
    stagesList.append(image)
currentStageImage = stagesList[0]

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
                            print("Correct guess")
                            for position in range(len(answer)): # update guessed word list
                                letter = answer[position]
                                if letter == alphabet:
                                    guessedWord[position] = letter
                            if '_' not in guessedWord: # all letters guessed
                                break;
                        elif alphabet not in wrongGuesses:
                            print("Wrong guess")
                            wrongGuesses.append(alphabet)
                            lives -= 1
                            if lives == 0:
                                break
                            currentStageImage = stagesList[7 - lives]
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


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f"FPS: {int(fps)}", (400, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0))
    cv2.putText(img, code, (200, 70), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 6)
    cv2.putText(img, "".join(guessedWord), (10, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 10)
    cv2.putText(img, "".join(guessedWord), (10, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 128, 255), 6)
    cv2.putText(img, "".join(wrongGuesses), (10, 450), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 6)

    h, w, c = currentStageImage.shape
    img[0:h, 0:w] = currentStageImage

    cv2.imshow("Image", img)
    cv2.waitKey(1)


# end of game
if lives == 0:
    print("")
    print("You lose")
    #cv2.putText(img, "You lose", (10, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 128, 255), 6)
else:
    print("You won")
    #cv2.putText(img, "You won", (10, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 128, 255), 6)
print(f"The word is: {answer}")