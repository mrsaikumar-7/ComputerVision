from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np
import mediapipe as mp


# helper functions
def quit(lmList, lmList2):
    safe = 60
    dist, info = detectorHand.findDistance(lmList[5][0:2], lmList2[9][0:2])
    print("DISTANCE IS : ", dist)

    if dist < safe:
        return True
    return False


# Parameters
width, height = 1280, 720
gestureThreshold = 300

folderPath = "Presentation"

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Hand Detector
detectorHand = HandDetector(detectionCon=0.8, maxHands=2)

# Variables
imgList = []
delay = 20
buttonPressed = False
counter = 0
drawMode = False
imgNumber = 0
delayCounter = 0
annotations = [[]]
annotationNumber = -1
annotationStart = False
hs, ws = int(120 * 1), int(213 * 1)  # width and height of small image

# Zooming feature
initialDistance = 0
image_scale = 0
# Get list of presentation images
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)

while True:
    # Get image frame
    success, img = cap.read()
    # inorder to avoid the mirror effect , flip the image
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    winName = 'slide'
    cv2.namedWindow(winName, cv2.WINDOW_NORMAL)

    # Find the hand and its landmarks
    allHands, img = detectorHand.findHands(img)  # with draw
    # Draw Gesture Threshold line
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if allHands and buttonPressed is False:  # If hand is detected

        hand = allHands[0]

        cx, cy = hand["center"]
        lmList = hand["lmList"]  # List of 21 Landmark points
        fingers = detectorHand.fingersUp(hand)  # List of which fingers are up

        # Constrain values for easier drawing
        xVal = int(np.interp(lmList[8][0], [0,650], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))
        indexFinger = xVal, yVal

        if cy <= gestureThreshold:  # If hand is at the height of the face
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
                else:
                    cv2.putText(imgCurrent, 'Oops, it is FIRST SLIDE', (20, 40), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=2, color=(256, 0, 0), lineType=cv2.LINE_AA, thickness=2)
            if fingers == [0, 0, 0, 0, 1]:
                print("Right")
                buttonPressed = True
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
                else:
                    cv2.putText(imgCurrent, 'Oops, it is LAST SLIDE', (20, 40), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=2, color=(256, 0, 0), lineType=cv2.LINE_AA, thickness=2)

        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            print(annotationNumber)
            annotations[annotationNumber].append(indexFinger)
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        else:
            annotationStart = False
        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                buttonPressed = True
        else:
            annotationStart = False

    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False

    if len(allHands) == 2:
        hand2 = allHands[1]
        lmList2 = hand2['lmList']
        fingers2 = detectorHand.fingersUp(hand2)

        if fingers2 == [1, 1, 0, 0, 0] and fingers == [1, 1, 0, 0, 0]:
            if (initialDistance is None):
                fin_distance, info, img = detectorHand.findDistance(lmList[8][0:2], lmList2[8][0:2], img)
                initialDistance = fin_distance
            length, info, img = detectorHand.findDistance(lmList[8][0:2], lmList2[8][0:2], img)
            print('initaial distance , length : ', initialDistance, length)
            image_scale =  int(1.8 * (length - initialDistance))
            print('IMAGE SCALED BY ', image_scale)
            cx, cy = info[4:]

        # if quit(lmList, lmList2):
        #     print('GESTURED QUIT is activated')
        #     break
    else:
        initialDistance = None
    try:
        h1, w1, _ = imgCurrent.shape
        # print('h1,w1', h1,w1)
        # print('image_scale is : ',image_scale)
        new_height, new_width = ((300 + 2 * image_scale) // 2) * 2, ((400 + 2 * image_scale) // 2) * 2
        imgCurrent = cv2.resize(imgCurrent, (new_width, new_height))
        # keeping the image in the center of the width
        windowCenter = (info[4] - new_width // 2, info[5])
        cv2.moveWindow(winName, windowCenter[0], windowCenter[1])
        cv2.resizeWindow(winName, new_width, new_height)
    except:
        pass
    for i, annotation in enumerate(annotations):
        for j in range(len(annotation)):
            if j != 0:
                cv2.line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), 12)

    h, w, _ = imgCurrent.shape
    imgSmall = cv2.resize(img, (w // 6, h // 6))
    try:
        imgCurrent[0:h // 6, w - w // 6: w] = imgSmall
    except:
        pass
    # imgCurrent = cv2.resize(imgCurrent,(new_width,new_height,))
    cv2.imshow(winName, imgCurrent)
    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



