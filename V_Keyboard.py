import cv2
from pynput import keyboard
import Hand_tracking as htm
import numpy as np
import cvzone
from time import sleep
from pynput.keyboard import Controller


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = htm.handDetector(detectionCon=0.8)

keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L","!"],
        ["Z","X","C","V","B","N","M",",",".","/"]
        ]
finalText = ""
keyboard = Controller()
def drawAll(frame, ButtonList):

    for button in ButtonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(frame, (button.pos[0],button.pos[1],button.size[0],button.size[1]), l=20,rt=0)
        cv2.rectangle(frame, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(frame, button.text, (x+20, y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)
    return frame

# def drawAll(frame, ButtonList):
#     frameNew = np.zeros_like(frame, np.uint8)
#     for button in ButtonList:
#         x, y = button.pos
#         cvzone.cornerRect(frameNew, (button.pos[0],button.pos[1],button.size[0],button.size[1]), l=20, t=3,rt=0)
#         cv2.rectangle(frameNew, button.pos, (x + button.size[0], y + button.size[1]), (255, 0, 255), cv2.FILLED)
#         cv2.putText(frameNew, button.text, (x+20, y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)
    

#     out = frame.copy()
#     alpha = 0.5
#     mask = frameNew.astype(bool)
#     out[mask] = cv2.addWeighted(frame, alpha, frameNew, 1 - alpha, 0)[mask]
#     return out 


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

    # def draw(self, frame):
        # x, y = self.pos
        # w, h = self.size
        # cv2.rectangle(frame, self.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        # cv2.putText(frame, self.text, (x+20, y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)
        # return frame

ButtonList = []
for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            ButtonList.append(Button([100*j + 50, 100 * i+50], key))

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame)
    frame = drawAll(frame, ButtonList)

    if lmList:
        for button in ButtonList:
            x, y = button.pos
            w, h = button.size
            if x<lmList[8][1]<x+w and y<lmList[8][2]<y+h:
                cv2.rectangle(frame, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(frame, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)
                
                length, info, frame = detector.findDistance(8, 12, frame, draw=False)
                if length<40:
                    keyboard.press(button.text)
                    cv2.rectangle(frame, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)
                    finalText += button.text
                    sleep(0.15)


    cv2.rectangle(frame, (50, 350), (700, 450), (0, 255, 0), cv2.FILLED)
    cv2.putText(frame, finalText, (60, 425), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)

    cv2.imshow("Image", frame)
    if cv2.waitKey(1) & 0xFF == ord("e"):
        break 

cap.release()
cv2.destroyAllWindows()