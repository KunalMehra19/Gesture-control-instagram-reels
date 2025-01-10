import webbrowser
import cv2
import keyboard
import mediapipe as mp
import time


cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

def dist(points,a,b):
    d=((points[a][1]-points[b][1])**2)+((points[a][2]-points[b][2])**2)
    return d**0.5

pTime=0
cTime=0
thumbs_up_detected = False

while True:
    success , img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    points=[]
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id ,lm in enumerate(handLms.landmark):
                # print(id,lm)
                h,w,c=img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                points.append([id,cx,cy])

                # if id == 4:
                #     cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    
    # print(points)
    if points:
        if dist(points,4,0) > dist(points,8,0) and dist(points,4,0) > dist(points,12,0) and dist(points,4,0) > dist(points,16,0) and dist(points,4,0) > dist(points,20,0) and dist(points,4,7)>dist(points,4,2):
            cv2.putText(img, "Thumbs Up", (70, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

            if not thumbs_up_detected:
                        # webbrowser.open("https://www.instagram.com/reels/")
                        thumbs_up_detected=True
            
        if dist(points,4,0) == dist(points,8,0)==dist(points,12,0)==dist(points,16,0)==dist(points,20,0):
             cv2.putText(img,"close",(70,50),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),2)

        if dist(points,8,0)>dist(points,4,0) and dist(points,8,0)>dist(points,12,0) and dist(points,8,0)>dist(points,16,0) and dist(points,8,0)>dist(points,20,0):
            cv2.putText(img, "Index Up", (70, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            # keyboard.press_and_release('down')

    points=[]
    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)


    cv2.imshow('Image', img)
    cv2.waitKey(1)