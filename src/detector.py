import logging
import random

import time

import cv2

logger = logging.getLogger(__name__)
logging.basicConfig(filename='{}.log'.format(__name__),level=logging.INFO)


class Detector():
	def __init__(self, fileName, avgS=30, xPos = 425, yPos = 300, width = 80, height = 10):
		if not fileName:
			return
		self.fileName = fileName
		# private
		self.__video = None
		self.__bWork = False
		self.__killThreads = False

		# reactangle 
		self.__xPos = xPos
		self.__yPos = yPos
		self.__width = width
		self.__height = height

		self.arr = []
		self.avgS = avgS

		self.colors = [
			(255, 0, 0), #    RED
			(255, 255, 0), #  YELLOW
			(0, 255, 0), #    GREEN
			(255, 0, 255), #  BLUE
			(32, 64, 196), #    ~BLUE
		]

		#threads
		#self.threads = {
		#	'frame': threading.Thread(target=self.frame_reader, args=(fileName)),
		#	'paint': threading.Thread(target=self.run, args=(None)),
		#	'detect': threading.Thread(target=self.detect, args=(None)),
		#}
		#self.threads['frame'].start()


	def setX(self, x):
		self.__xPos = x

	def setY(self, y):
		self.__yPos = y

	def setS(self, s):
		self.avgS = s
	
	def work(self, b):
		self.__bWork = b

	def isWork(self):
		return self.__bWork

	
	def crop(self, frame):
		return frame[self.__yPos:self.__yPos+self.__height, self.__xPos:self.__xPos+self.__width]


	def getS(self, frame):
		try:
			frame = self.crop(frame)
			i=0
			cMatrix = []
			for line in frame:
				for pixel in line:
					cMatrix.append(0.299*pixel[2]+0.587*pixel[1]+0.144*pixel[0])

			
			awg = 0
			i = 0
			for x in cMatrix:
				awg += x
				i += 1
			awg = awg / i # int or not to int???
			s = 0
			for x in cMatrix:
				s += abs(awg - x)
				
			s = round(s / (self.__xPos*self.__xPos), 3) * 1000
			#s = s / (self.__xPos*self.__xPos)
			
			self.arr.append(s)
			ans = False
			if len(self.arr) > 2:
				if self.arr[-1] > self.avgS:
					if self.arr[-2] < self.avgS:
						ans = True
			return ans, s
			
			
		except Exception as e:
			print(e)
		return ans, s

	def Paint(self, frame):
		try:
			cv2.rectangle(frame, 
					(self.__xPos, self.__yPos), 
					(self.__xPos + self.__width, self.__yPos + self.__height), 
					self.colors[0], 
					1)#max(self.__width, self.__height) // 10)
		except Exception as e:
			print(e)
		return frame