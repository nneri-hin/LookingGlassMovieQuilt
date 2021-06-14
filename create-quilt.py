#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from sys import argv  as a
import datetime
import locale   
import numpy as np
import cv2

W= 8
H= 6
MULTI_W = 3840
MULTI_H = 3840
SINGLE_W = int(3840 / W)
SINGLE_H = int(3840 / H)

#一枚画像
def createBuf():
    return  np.zeros((int(SINGLE_H),int(SINGLE_W),3),np.uint8)

if __name__ == '__main__':
    #縦長の動画受け取った時の処理必要
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
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        worg = frame.shape[1]
        horg = frame.shape[0]
        w = int(frame.shape[0] * aspect)
        h = int(frame.shape[1] / aspect)
        if frame.shape[0] > frame.shape[1] : 
            #trim = frame[:, int((worg - w) / 2 )  : int(  ( worg+w) / 2  ) ]
            trim = frame[ int((horg - h) / 2 )  : int(  ( horg+h) / 2  ),: ] 
            pass
        else:
            trim = frame[:, int((worg - w) / 2 )  : int(  ( worg+w) / 2  ) ]
        print(trim.shape)
        resized = cv2.resize(trim,(SINGLE_W,SINGLE_H))
        print(resized.shape)
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
    while pos < cnt - 1 :
        pos = pos + offset
        i = round(pos)
        ws = p % W * SINGLE_W
        hs = int(p / W) *SINGLE_H

        final[hs:hs+SINGLE_H,ws:ws+SINGLE_W]= images[i]

        #hs = p % H * SINGLE_H
        #ws = int(p/H) * SINGLE_W
        #final[ws:ws+SINGLE_W,hs:hs+SINGLE_H] = images[i]
        p += 1
    cap.release()
    cv2.imwrite("out.png",final)
    #cv2.destroyAllWindows()
