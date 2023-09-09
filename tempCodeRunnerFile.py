if len(allHands) ==2:
    #     hand2 = allHands[1]
    #     lmList2 = hand2['lmList']
    #     fingers2 = detectorHand.fingersUp(hand2)
        
    #     if fingers2==[1,1,0,0,0] and fingers == [1,1,0,0,0]:
    #         if (initialDistance is None):
    #             fin_distance, info,img= detectorHand.findDistance(lmList[8][0:2], lmList2[8][0:2],img)
    #             initialDistance = fin_distance
    #         length, info,img= detectorHand.findDistance(lmList[8][0:2], lmList2[8][0:2],img)
    #         print('initaial distance , length : ',initialDistance,length)
    #         image_scale = int(length-initialDistance)
    #         print('IMAGE SCALED BY ',image_scale)
    #         cx,cy = info[4:]
        
    #     if quit(lmList,lmList2):
    #         break
    # else:
    #     initialDistance= None
    # try:
    #     h1,w1,_= imgCurrent.shape
    #     # print('h1,w1', h1,w1)
    #     # print('image_scale is : ',image_scale)
    #     new_height, new_width = ((300+2*image_scale)//2)*2, ((400+2*image_scale)//2)*2
    #     imgCurrent = cv2.resize(imgCurrent,(new_width,new_height))
    #     #keeping the image in the center of the width
    #     windowCenter = (info[4]-new_width//2,info[5])
    #     cv2.moveWindow(winName,windowCenter[0],windowCenter[1])
    #     cv2.resizeWindow(winName,new_width,new_height)
    # except:
    #         pass