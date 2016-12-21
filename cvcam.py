import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
#/usr/bin/env python
import time
import numpy as np
import cv2

def on_turn():
    cam = cv2.VideoCapture(0)
    cam.set(3,320)
    cam.set(4,180)

    ret, prev = cam.read()
    #prev = prev[200:400,100:300]
    prev = cv2.resize(prev,(320,180), interpolation = cv2.INTER_LINEAR)
    #cv2.imwrite('1.jpg',prev)
    #prev = cv2.QueryFrame(cam)
    prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    show_hsv = False
    show_glitch = False
    cur_glitch = prev.copy()

    cols = 320
    rows = 180

    detect = 0
    left = 0
    right = 0
    t = threading.currentThread()
    while getattr(t,'do_run',True):
        ret, img = cam.read()
        #img = img[200:400,100:300]
        img = cv2.resize(img,(320,180), interpolation = cv2.INTER_LINEAR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        prevgray = gray
        cv2.imshow('flow', draw_flow(gray, flow))
        #fl = draw_flow(gray, flow)
        #cv2.imshow('flow', gray)
        #cv2.imwrite('1.jpg',fl)
        #cv2.imwrite('1.jpg',img)
        #print 'array':
        #print flow

        
        pos = 0
        neg = 0
        for i in range(0, cols, 10):
            for j in range(0, rows, 10):
                dx = flow[j, i][0]
                dy = flow[j, i][1]

                if abs(dx) > 0.6:
                    if dx > 0:
                        pos = pos + 1
                    else:
                        neg = neg + 1

		if abs(pos - neg) > 20:
			if pos - neg > 0:
				left = left + 1
			elif pos - neg < 0:
				right = right + 1
			if detect:

				if time.time() - start_time > 0.1:
					if right > left:
    					t.turn = 4
					else:
						t.turn = 3
					detect = 0
					left = 0
					right = 0
			else:
				detect = 1
				left = 0
				right = 0
				t.turn = 0
				start_time = time.time()
		'''
		else:
			detect = 0
        print pos, ' ', neg
        ''' 
def cam_off():
	cv2.VidepCapture(0).release()

