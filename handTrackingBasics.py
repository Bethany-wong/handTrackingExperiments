import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLandMarks in results.multi_hand_landmarks:
            for id, landMark in enumerate(handLandMarks.landmark):
                #print(id, landMark)
                h, w, c = img.shape
                center_x, center_y = int(landMark.x*w), int(landMark.y*h)
                #print(id, center_x, center_y)
                if id == 8:
                    cv2.circle(img, (center_x, center_y), 10, (255, 0, 255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLandMarks, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
