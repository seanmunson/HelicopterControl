#! /usr/bin/python

import cv, cv2, numpy, time
import serial

LED = 3
#To increment hex values, convert to int, add, then convert result to hex
signal ={'yaw':63,'pitch':63,'throttle':100,'trim':63}
ser = serial.Serial('/dev/tty.usbmodemfd121',9600)

#ser.open()
#ser.write('abcd')


#def send_packet():
#	x = 0
#	for k,v, in signal.iteritems():
#		signal[k] = hex(int(v, 16) + change[i]
#		++x
	#packet=bytearray([signal['yaw'], signal['pitch'],signal['throttle'],signal['trim']])
	#ser.open()
	#ser.write(packet)
	#ser.close()
#def setup():


#def filter():
#	for i in xrange(1,5):
#		filter = cv2.imread("filt_" + str(i) + ".png")

isFirst = True

def get_blobs():
	for i in xrange(1, 10):
		blob_name = "back_" + str(i) + ".png"
		img = cv2.imread(blob_name, -1)


def thresh():
	for i in xrange(1, 10):
		read_name = "gauss_image_" + str(i) + ".png"
		img = cv2.imread(read_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
		name = "thresh_" + str(i) + ".png"
		flag, thresh_img = cv2.threshold(img, 45, 255, cv2.THRESH_BINARY)
		cv2.imwrite(name, thresh_img)


def back_sub():
	for i in xrange(1, 10):
		img = cv2.imread("gauss_image_0.png", cv2.CV_LOAD_IMAGE_GRAYSCALE)
		proc = cv2.imread("gauss_image_" + str(i) + ".png", cv2.CV_LOAD_IMAGE_GRAYSCALE)
		cv2.namedWindow("win1", flags=cv2.WINDOW_NORMAL)
		cv2.imshow("win1", proc)
		#time.sleep(3)
		result = cv2.absdiff(img, proc)
		#cv.AbsDiff(img, proc, result)
		name = "back_" + str(i) + ".png"
		cv2.imwrite(name, result)

def capture():
	cv2.namedWindow("win1", flags=cv2.WINDOW_NORMAL)
	cv2.namedWindow("hsv", flags=cv2.WINDOW_NORMAL)
	cap = cv2.VideoCapture(0);
	for i in xrange(10):
		cap.grab()
		success, img = cap.retrieve()
		name = "pre_image_" + str(i) + ".png"
		cv2.imwrite(name, img)
		img = cv2.GaussianBlur(img, (5,5),0)
		name = "gauss_image_" + str(i) + ".png"
		cv2.imwrite(name, img)
		print("Taking image " + str(i))
		time.sleep(3)

def mask():
	for i in xrange(1, 5):
		mask = cv2.imread("mask.png", cv2.CV_LOAD_IMAGE_GRAYSCALE);
		img = cv2.imread("filt_" + str(i) + ".png", cv2.CV_LOAD_IMAGE_GRAYSCALE)
		#result = cv2.absdiff(img, mask)
		flag, thresh_img = cv2.threshold(result, 45, 255, cv2.THRESH_BINARY)
		name = "filtsub_" + str(i) + ".png"
		cv2.imwrite(name,img)

def hsv():
	for i in xrange(1,10):
		img = "thresh_" + str(i) + ".png"
		flag, hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
		thresh = cv2.inRange(hsv,numpy.array((0, 150, 150)), numpy.array((0, 255, 255)))
		thresh2 = thresh.copy()
		contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		max_area = 0
		for cnt in contours:
			area = cv2.contourArea(cnt)
			if area > max_area:
				max_area = area
				best_cnt = cnt
				M = cv2.moments(best_cnt)
		cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
		cv2.circle(img,(cx,cy),100,255,-1)
		#cv2.imshow("hsv", hsv)
		hsv_name = "hsv_image" + str(i) +".png"
		time.sleep(5)

def increase_throttle():
	print("Increase")

def decrease_throttle():
	print("Decrease")

def sigsend():
	sigstring = bytearray([signal['pitch'], signal['yaw'], signal['throttle'], signal['trim'], 128 ])
	print(str(sigstring) + "\n")
	ser.write(sigstring + str('\n'))
	ser.flush()
	#time.sleep(.03)

def hsv_capture():
	cv2.namedWindow("win1", flags=cv2.WINDOW_NORMAL)
	cap = cv2.VideoCapture(0);
	old_x = 0
	while(1):
		cap.grab()
		flag,frame = cap.retrieve()
		#frame = cv2.blur(frame,(5,5))
		hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		thresh = cv2.inRange(hsv,numpy.array((100, 150, 150)), numpy.array((180, 255, 255)))
		thresh2 = thresh.copy()
		#flag, thresh_img = cv2.threshold(thresh, 45, 255, cv2.THRESH_BINARY)
		contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		if(len(contours) > 0):
			max_area = 0
			M = 0
			for cnt in contours:
				area = cv2.contourArea(cnt)
				if area > max_area:
					max_area = area
					best_cnt = cnt
					M = cv2.moments(best_cnt)
			if not M == 0:
				cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
				cv2.circle(frame,(cx,cy),10,255,-1)
				old_x = cy
				if cy >= 200: 
					control(0)
				else:
					control(1)
				print("Y position = " + str(cy))
		cv2.line(frame, (0,200), (800,200),(200,255,100))
		cv2.imshow("win1", frame)
		sigsend()


def control(x):
		#signal['yaw'] = 63
		#signal['pitch'] = 63
		#signal['throttle'] = 50
		#signal['trim'] = 63
	if x == 0:
		signal['yaw'] = 63
		signal['pitch'] = 63
		signal['throttle'] = 110
		signal['trim'] = 63
	else:
		signal['yaw'] = 63
		signal['pitch'] = 63
		signal['throttle'] = 50
		signal['trim'] = 63



def main():
	hsv_capture()
	#capture()
	#back_sub()
	#thresh()
	#hsv()
	#mask = cv2.GaussianBlur(mask, (7,7),0)
	#print(str(int(signal['yaw'], 16) + 1))



if __name__=="__main__":
    main()