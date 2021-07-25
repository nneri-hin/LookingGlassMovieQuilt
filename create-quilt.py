#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from sys import argv  as a
import datetime
import locale   
import numpy as np
import cv2
from optparse import OptionParser

W= 8
H= 6
#W=5
#H=9

MULTI_W = 3840
MULTI_H = 3840
#MULTI_W = 7680
#MULTI_H = 7680
SINGLE_W = int(MULTI_W / W)
SINGLE_H = int(MULTI_H / H)

#一枚画像
def createBuf():
    return  np.zeros((int(SINGLE_H),int(SINGLE_W),3),np.uint8)

if __name__ == '__main__':
    #縦長の動画受け取った時の処理必要
    parser =  OptionParser()
    parser.add_option("-r","--rotate_clockwise",dest="rotate_clock",action="store_true",default=False,help="movie rotating clockwise")
    parser.add_option("-R","--rotate_counter",dest="rotate_counter",action="store_true",default=False,help="movie rotating counter clockwise")
    parser.add_option("-i","--reverse",dest="reverse",action="store_true",default=False,help="Reverse Rotation")
    (options,args) = parser.parse_args()
    aspect  = SINGLE_W / SINGLE_H
    print(aspect)
    cap = cv2.VideoCapture(a[1])
    cnt = 0
    images = []
    while(cap.isOpened()):
        #print(cnt)
        ret, frame = cap.read()
        if frame is None:
            break
        #とりあえず全部90度回転させる方針
        if options.rotate_clock:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        if options.rotate_counter:
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        worg = frame.shape[1]
        horg = frame.shape[0]
        w = int(frame.shape[0] * aspect)
        h = int(frame.shape[1] / aspect)
        #print(w,h,aspect)
        movAspect = frame.shape[0] / frame.shape[1]
        #print(aspect,movAspect,frame.shape[0],frame.shape[1])
        #print(movAspect / aspect)
        #print( aspect / movAspect)
        #if frame.shape[0] > frame.shape[1] : 
        if movAspect / aspect > 1 :
            #print("trim1")
            #trim = frame[:, int((worg - w) / 2 )  : int(  ( worg+w) / 2  ) ]
            trim = frame[ int((horg - h) / 2 )  : int(  ( horg+h) / 2  ),: ] 
            #print(trim.shape)
            pass
        else:
            #print("trim2")
            trim = frame[:, int((worg - w) / 2 )  : int(  ( worg+w) / 2  ) ]
            #print(frame.shape)
            #print(trim.shape)
        #print(trim.shape)
        resized = cv2.resize(trim,(SINGLE_W,SINGLE_H))
        images.append(resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #一旦画像を格納してからやるのはあとで特徴量抽出して使用フレームを決めるため
    cnt = len(images)
    offset = (len(images) -1 ) / 48
    #print(cnt-1 / 48 )
    pos = 0.0
    p = 0
    final = np.zeros((MULTI_W,MULTI_H,3),np.uint8)
    temp = []
    print(cnt)
    ##逆回転の時に使う
    if options.reverse:
        for i in range(len(images)):
            print(i)
            print(len(images)-i)
            temp.append(images[len(images)-i-1])
        images = temp

    while (pos < cnt - 1)  and p < W*H:
        pos = pos + offset
        i = round(pos)
        ws = p % W * SINGLE_W
        hs = int(p / W) *SINGLE_H
        if i >len(images) -1 :
            i = len(images) -1 
        #final[hs:hs+SINGLE_H,ws:ws+SINGLE_W]= images[i]
        final[hs:hs+SINGLE_H,MULTI_W-ws-SINGLE_W:MULTI_W-ws]= images[i]
        #hs = p % H * SINGLE_H
        #ws = int(p/H) * SINGLE_W
        #final[ws:ws+SINGLE_W,hs:hs+SINGLE_H] = images[i]
        p += 1
    cap.release()
    cv2.imwrite(a[2],final)
    #cv2.destroyAllWindows()

