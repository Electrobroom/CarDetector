import logging
import threading
import sys
import time

import cv2
from PyQt5 import QtCore, QtWidgets, QtGui

from detector import Detector
import userinterface as UI
import _thread

logger = logging.getLogger(__name__)
logging.basicConfig(filename='{}.log'.format(__name__),level=logging.INFO)


class App(QtWidgets.QMainWindow, UI.Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.DT = Detector(None)
		self.frameThread = threading.Thread(target=self.frame_reader, args=())

		self.setupUi(self)
		self.loadUi()


	def loadUi(self):

		# Buttons

		try:
			self.browseBtn.clicked.connect(self.showDialog)
		except Exception as e:
			print('-----> ERORR{}'.format(e))
		self.playBtn.clicked.connect(self.playMedia)
		self.playBtn.setEnabled(False)
		self.playBtn.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))

		self.stopBtn.clicked.connect(self.stopMedia)
		self.stopBtn.setEnabled(False)
		self.stopBtn.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaStop))

		# Lables and Edits
		self.XCoordEdit.textChanged.connect(self.updateDT)
		self.YCoordEdit.textChanged.connect(self.updateDT)
		self.sEdit.textChanged.connect(self.updateDT)


		self.listWidget = QtWidgets.QListWidget()

	def updateDT(self):
		try:
			self.DT.setX(int(self.XCoordEdit.text()))
			self.DT.setY(int(self.YCoordEdit.text()))
			self.DT.setS(int(self.sEdit.text()))
		except Exception as e:
			logger.warn(e)

	def showDialog(self):
		try:
			fName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose video', '{}/Desktop'.format(QtCore.QDir.homePath()), 'Video files (*.mp4)')
		except Exception as e:
			print('-----> ERORR{}'.format(e))
		if fName:
			#self.mediaPlayer.setMedia(
					#QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(fname)))
			self.DT = Detector(fName)
			#frameThread.start()
			#self.frame_reader()
			self.filenameLbl.setText('Видео: {}'.format(fName))
			self.playBtn.setEnabled(True)
			pass # todo: 
			# 1. CV detector
			# 2. run()


	def frame_reader(self):
		vCapture = cv2.VideoCapture(self.DT.fileName)
		logger.info('Detector %s: ', vCapture)
		ret, frame = vCapture.read()
		height, width = frame.shape[:2]
		fx = self.horizontalLayoutWidget_9.height() / height
		fy = self.horizontalLayoutWidget_9.width() / width
		while self.DT.isWork():
			frameIterator = 0
			count = 0
			while ret:
				frameIterator += 1
				frame = cv2.resize(frame, None, fx=fx, fy=fy, interpolation=cv2.INTER_AREA)
				if not self.DT.isWork():
					break
				try:
					ans, s = self.DT.getS(frame)
					#self.sEdit.setText(_translate("MainWindow", s))
					if ans:
						count +=1
						self.carsLbl.setText(str(count))

					frame = self.DT.Paint(frame)
					height, width, channel = frame.shape
					step = channel * width
					qImg = QtGui.QImage(frame.data, width, height, step, QtGui.QImage.Format_RGB888)
					self.image_label.setPixmap(QtGui.QPixmap.fromImage(qImg))
					
					ret, frame = vCapture.read()
					#time.sleep(0.020)
				except Exception as e:
					sys.exit()
			self.DT.work(False)
			self.stopBtn.setEnabled(False)
			self.playBtn.setEnabled(True)
			print('OK')
			return 
		return 


	def playMedia(self):
		self.DT.work(True)
		try:
			self.frameThread.start()
		except:
			pass
		self.stopBtn.setEnabled(True)
		self.playBtn.setEnabled(False)

	def stopMedia(self):
		self.DT.work(False)
		self.stopBtn.setEnabled(False)
		self.playBtn.setEnabled(True)


def Main():
	app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
	window = App()  # Создаём объект класса App
	window.show()  # Показываем окно
	app.exec_()


if __name__ == "__main__":
	Main()

"""
self.imageLayout = QtWidgets.QVBoxLayout(MainWindow)
self.imageLayout.setObjectName("imageLayout")
self.image_label = QtWidgets.QLabel(MainWindow)
self.image_label.setObjectName("image_label")
self.imageLayout.addWidget(self.image_label)
"""