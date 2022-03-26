from imp import init_builtin
import cv2
import math
from RioComms import RioComms

tableName = "balls"
serverURL = "10.40.26.2"

rioComms = RioComms(serverURL)

def send(key, val):
    rioComms.send(tableName, key, val)

def get(key):
    rioComms.get(tableName, key, -1000)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_EXPOSURE, -6)

while True:
    _, initImg = cap.read()
    img = initImg.copy()

    redBalls = []
    blueBalls = []

    #cv2.imshow("yo", img)

    img = cv2.resize(img, (133, 100))

    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(img, (0,255*1/3, 50), (360,255,255))

    blueSat = cv2.inRange(img, (0, 255 * 1/3, 30), (360,255,255))

    blueImg = cv2.bitwise_and(img, img, mask=blueSat)

    img = cv2.bitwise_and(img, img, mask=mask)

    #cv2.imshow("yo2", mask)
    #cv2.imshow("yo3", img)

    mask2 = cv2.inRange(img, (0, 0, 0), (10, 255, 255))
    mask3 = cv2.inRange(img, (175, 0, 0), (180, 255, 255))

    mask4 = cv2.bitwise_or(mask2, mask3)

    mask5 = cv2.bitwise_and(mask4, mask)

    maskBlue = cv2.inRange(blueImg, (90, 0, 0), (110, 255, 255))

    maskBlue = cv2.bitwise_and(maskBlue, blueSat)

    #cv2.imshow("blue", cv2.bitwise_and(blueImg, blueImg, mask=maskBlue))

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(5, 5))

    maskBlue = cv2.dilate(maskBlue, kernel)
    maskBlue = cv2.erode(maskBlue, kernel)
    
    maskBlue = cv2.erode(maskBlue, kernel, iterations=2)

    maskBlue = cv2.dilate(maskBlue, kernel, iterations=2)

    mask5 = cv2.dilate(mask5, kernel, iterations=1)

    mask5 = cv2.erode(mask5, kernel, iterations=1)

    mask5 = cv2.erode(mask5, kernel, iterations=2)

    mask5 = cv2.dilate(mask5, kernel, iterations=2)

    

    #mask5 = cv2.dilate(mask5, kernel, iterations=2)

    img = cv2.bitwise_and(img, img, mask=mask5)

    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)


    #cv2.imshow("yo5", mask5)

    cnts = cv2.findContours(mask5.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #print(len(cnts[0]))

    for i in cnts[0]:
        
        peri = cv2.arcLength(i, True)
        area = cv2.contourArea(i)

        if(area > 100):
            M = cv2.moments(i)
            cX = int((M["m10"] / M["m00"])) / 133
            cY = int((M["m01"] / M["m00"])) / 100

            peri = cv2.arcLength(i, True)
            area = cv2.contourArea(i)

            rat = peri/math.sqrt(area)

            if rat < 4 and rat > 3.4 and area > 100:
                #print(rat)
                initImg = cv2.circle(initImg,(math.floor(cX * 640), math.floor(cY * 480)), 20, (255,0,0), -1)
                redBalls.append([cX, cY])

            #print(peri/math.sqrt(area))

            #print("x: " + str(cX) + ", y: " + str(cY))

    cnts = cv2.findContours(maskBlue.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #print(len(cnts[0]))

    for i in cnts[0]:
        
        peri = cv2.arcLength(i, True)
        area = cv2.contourArea(i)

        if(area > 100):
            M = cv2.moments(i)
            cX = int((M["m10"] / M["m00"])) / 133
            cY = int((M["m01"] / M["m00"])) / 100

            peri = cv2.arcLength(i, True)
            area = cv2.contourArea(i)

            rat = peri/math.sqrt(area)

            if rat < 4 and rat > 3.4 and area > 100:
                #print(rat)
                initImg = cv2.circle(initImg,(math.floor(cX * 640), math.floor(cY * 480)), 20, (0,0,255), -1)
                #print(cX * 640)
                blueBalls.append([cX, cY])

            #print(peri/math.sqrt(area))

            #print("x: " + str(cX) + ", y: " + str(cY))

    
    if len(redBalls) > 0:
        send("redX", redBalls[0][0])

        send("redY", redBalls[0][1])

    if len(blueBalls) > 0:
        send("blueX", blueBalls[0][0])

        send("blueY", blueBalls[0][1])
    
    #cv2.imshow("yo4", img)

    cv2.imshow("final", initImg)

    cv2.waitKey(5)