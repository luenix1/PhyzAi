import cv2 as cv
import numpy as np
from enum import Enum
import Variables

MAX_HEIGHT = 300
MAX_WIDTH = 200

cap = cv.VideoCapture(0,cv.CAP_DSHOW)

def detectCard(frame):
    guess = "none"
    gotCard = False
    frame2 = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    crop = frame
    blur = cv.GaussianBlur(frame2, (5,5), 0)
    ret, thresh = cv.threshold(blur, 60, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    contours, heiarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    height, width, _ = frame.shape
    cards = 0

    for cnt in contours:
        size = cv.contourArea(cnt)
        peri = cv.arcLength(cnt,True)
        approximation = cv.approxPolyDP(cnt,0.01*peri, True)
        if size > 10000 and size < 120000 and len(approximation) == 4:
            draw = cv.drawContours(frame, cnt, -1, (0,255,0), 10)

            x,y,w,h = cv.boundingRect(cnt)

            pts = np.float32(approximation)
            tempPt = np.float32(approximation)

            tempPt[0] = pts[3]
            tempPt[1] = pts[2]
            tempPt[2] = pts[1]
            tempPt[3] = pts[0]
            
            if(w > 1.2*h):
                tempPt[0] = pts[2]
                tempPt[1] = pts[3]
                tempPt[2] = pts[0]
                tempPt[3] = pts[1]
                # print("horizontal")
            elif(w> h*0.8 and h*1.2 > w):
                
                if(pts[1][0][1] >= pts[3][0][1]):
                    tempPt[0] = pts[2]
                    tempPt[1] = pts[3]
                    tempPt[2] = pts[0]
                    tempPt[3] = pts[1]
                    # print("diamond")

                if(pts[3][0][1] > pts[1][0][1]):
                    tempPt[0] = pts[1]
                    tempPt[1] = pts[2]
                    tempPt[2] = pts[3]
                    tempPt[3] = pts[0]
                    # print("diamond")   

            input = np.float32([tempPt[0],tempPt[1],tempPt[2],tempPt[3]])
            output =np.float32([[0,0], 
                               [0,MAX_HEIGHT-1],
                               [MAX_WIDTH -1, MAX_HEIGHT -1],
                               [MAX_WIDTH-1,0]])
            
            M = cv.getPerspectiveTransform(input,output)
            crop = cv.warpPerspective(frame2,M,(MAX_WIDTH,MAX_HEIGHT),flags = cv.INTER_LINEAR)
            cards+=1
            
        
    if crop.all() != frame.all():
        guess, gotCard = readCard(crop)
        # print(guess, gotCard)
        cv.putText(frame,guess,(150, 100),cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0),2)

    cv.imshow("crop", crop)
    cv.imshow("test", frame)

    return guess, gotCard
    # print(cards)

def readCard(crop):
    bestMatch = 0.0
    card = "none"

    rankOnly = crop[0:50, 0:32]
    rankOnly = cv.resize(rankOnly, (0,0), fx = 4, fy = 4)

    filter = cv.GaussianBlur(rankOnly, (3,3), 0)
    ret, filter = cv.threshold(rankOnly, 150, 255, cv.THRESH_BINARY_INV)


    for i in Variables.Templates:
        template = cv.imread(i.value)
        template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)


        matchTemplate = cv.matchTemplate(filter, template, cv.TM_CCOEFF_NORMED)
        _, match, _, _ = cv.minMaxLoc(matchTemplate)
        

        if(abs(match) > abs(bestMatch)):
            bestMatch = match
            if(abs(bestMatch) > 0.5):
                card = i.name

    cv.imshow("rank", rankOnly)
    cv.imshow("processed", filter)
    
    if card == "none":
        return card, False
    else: 
        return card, True
    


    #this was for writing the template images, I'll keep just incase I want to redo them
    if cv.waitKey(1) & 0xFF == ord("e"):
        cv.imwrite("A.png", filter)
        print("wrote")

    if cv.waitKey(1) & 0xFF == ord("r"):
        cv.imwrite("2.png", filter)
        print("wrote")

    if cv.waitKey(1) & 0xFF == ord("t"):
        cv.imwrite("3.png", filter)
        print("wrote")
    
    if cv.waitKey(1) & 0xFF == ord("y"):
        cv.imwrite("4.png", filter)
        print("wrote")

    if cv.waitKey(1) & 0xFF == ord("u"):
        cv.imwrite("5.png", filter)
        print("wrote")

    if cv.waitKey(1) & 0xFF == ord("i"):
        cv.imwrite("6.png", filter)
        print("wrote")
    
    if cv.waitKey(1) & 0xFF == ord("o"):
        cv.imwrite("7.png", filter)
        print("wrote")

    if cv.waitKey(1) & 0xFF == ord("p"):
        cv.imwrite("8.png", filter)
        print("wrote")

    if cv.waitKey(1) & 0xFF == ord("a"):
        cv.imwrite("9.png", filter)
        print("wrote")
    
    if cv.waitKey(1) & 0xFF == ord("s"):
        cv.imwrite("10.png", filter)
        print("wrote")

    if cv.waitKey(1) & 0xFF == ord("d"):
        cv.imwrite("J.png", filter)
        print("wrote")

    if cv.waitKey(1) & 0xFF == ord("f"):
        cv.imwrite("Q.png", filter)
        print("wrote")
    
    if cv.waitKey(1) & 0xFF == ord("g"):
        cv.imwrite("K.png", filter)
        print("wrote")





# while cap.isOpened:
#     ret, frame = cap.read()

#     detectCard(frame)

#     if cv.waitKey(1) & 0xFF == ord("q"):
#         break
    

# print("endLoop")
# cap.release()
# cv.destroyAllWindows()


    



        

