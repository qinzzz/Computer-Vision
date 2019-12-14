'''
date: 2019/11/06 
creatd by: wqx

1. Morphological edge detection [done]
2. Morphological Reconstruction
	Conditional dilation in binary image [done]
	Grey scale Reconstruction [done]
	Morphological gradient [done]

Requirements:

	Design your own UI and display I/O images
	User customized SE
	language：python or C++
'''

import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QRadioButton, QTextEdit, QHBoxLayout, QVBoxLayout, QMessageBox, QFileDialog, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from binary import edge_detection, cond_dilate, cond_erode
from greyscale import CBR, OBR, gradient

class imageProcessing(QWidget):
	def __init__(self):
		super().__init__()
		self.setStyleSheet('''
			QLabel#h1{
			font-size:14px;
			font-weight:600;
			}
			QLabel#h2{
			font-size:14px;
			font-weight:600;
			}
			''')
		self.title = "image processing program"
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 540
		self.ksize = 3
		self.sigma = 1.0
		self.image = np.ndarray(())
		self.bi_img = np.ndarray(())
		self.marker = np.ndarray(())
		self.se = np.ndarray(())
		self.cur_img = np.ndarray(())
		self.initUI()


	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		# left
		selectLabel = QLabel('Target Image: ')
		selectBtn = QPushButton("Select")
		self.imgLabel = QLabel()
		convertBtn = QPushButton("Convert to binary")

		#right
		self.subTitle = QLabel("Select an operation...")
		self.subTitle.setObjectName('h1')
		self.binaryLabel = QLabel("Binary")
		self.greyLabel = QLabel("Greyscale")
		self.binaryLabel.setObjectName('h2')
		self.greyLabel.setObjectName('h2')

		self.btn11 = QRadioButton("Edge Detection")
		self.cbbox1 = QComboBox()
		self.cbbox1.addItems(['standard', 'external', 'internal'])

		self.btn12 = QRadioButton("Conditional Dilation")
		self.btn13 = QRadioButton("Conditional Erosion")
		self.btn11.setChecked(True) # default

		selectMarkerBtn = QPushButton("Select a marker")
		self.markerLabel = QLabel("No marker selected.")

		self.btn21 = QRadioButton("Morphological gradient")
		self.cbbox2 = QComboBox()
		self.cbbox2.addItems(['standard', 'external', 'internal'])

		self.btn22 = QRadioButton("Closing by Reconstruction")
		self.btn23 = QRadioButton("Opening by Reconstruction")

		self.seLabel = QLabel("Enter Structure Element")
		self.seLabel.setObjectName('h2')
		self.seLabel2 = QLabel("(recommend odd dimensional matrix)")
		self.seText = QTextEdit()
		self.seText.setText("1,1,1\n1,1,1\n1,1,1")

		# add adjustble kernel size

		submitBtn = QPushButton("Confirm")
		saveBtn = QPushButton("Save")
		cancelBtn = QPushButton("Exit")


		hboxLeftUp = QHBoxLayout()
		hboxLeftUp.addWidget(selectLabel,0,Qt.AlignLeft)
		hboxLeftUp.addWidget(selectBtn,1,Qt.AlignLeft)
		hboxLeftUp.addWidget(convertBtn)


		'''connection'''
		# click select
		selectBtn.clicked.connect(self.load_image)
		# click confirm/save/cancel
		submitBtn.clicked.connect(self.submit)
		saveBtn.clicked.connect(self.save)
		cancelBtn.clicked.connect(self.close)
		# click convert to binary
		convertBtn.clicked.connect(self.convert_binary)


		vboxLeft = QVBoxLayout()
		vboxLeft.addLayout(hboxLeftUp)
		vboxLeft.addWidget(self.imgLabel)

		hboxRightDown = QHBoxLayout()
		hboxRightDown.addWidget(submitBtn)
		hboxRightDown.addWidget(saveBtn)
		hboxRightDown.addWidget(cancelBtn)

		vboxRight = QVBoxLayout()
		vboxRight.addWidget(self.subTitle,0,Qt.AlignTop)
		vboxRight.addStretch(1)
		vboxRight.addWidget(self.binaryLabel)
		vboxRight.addStretch(1)
		vboxRight.addWidget(self.btn11)
		vboxRight.addWidget(self.cbbox1)
		vboxRight.addWidget(self.btn12)
		# vboxRight.addWidget(self.btn13)
		# select marker button & name label
		hboxRight1 = QHBoxLayout()
		hboxRight1.addWidget(selectMarkerBtn)
		hboxRight1.addWidget(self.markerLabel)
		vboxRight.addLayout(hboxRight1)

		'''connection'''
		# click select marker
		selectMarkerBtn.clicked.connect(self.load_marker)

		vboxRight.addStretch(1)
		vboxRight.addWidget(self.greyLabel)
		vboxRight.addStretch(1)
		vboxRight.addWidget(self.btn21)
		vboxRight.addWidget(self.cbbox2)
		vboxRight.addWidget(self.btn22)
		vboxRight.addWidget(self.btn23)
		
		vboxRight.addStretch(1)
		vboxRight.addWidget(self.seLabel)
		vboxRight.addWidget(self.seLabel2)
		vboxRight.addWidget(self.seText)
		
		vboxRight.addStretch(10)

		vboxRight.addLayout(hboxRightDown)

		hboxAll = QHBoxLayout()
		hboxAll.addLayout(vboxLeft)
		hboxAll.addStretch(6)
		hboxAll.addLayout(vboxRight)
		hboxAll.addStretch(3)


		self.setLayout(hboxAll)
		self.show()

	
	def submit(self):
		self.readSe()
		isBinary = False
		if self.image.size == 1:
			QMessageBox.information(self,'Fail','No image selected.')
			return
		if self.se.size == 1:
			QMessageBox.information(self,'Fail','No structure element.')
			return
			
		if self.btn11.isChecked():
			isBinary = True
			res = edge_detection(self.bi_img, self.se, self.cbbox1.currentIndex())

		elif self.btn12.isChecked():
			isBinary = True
			if self.marker.size == 1:
				QMessageBox.information(self,'Fail','No marker selected.')
				return
			else:
				res = cond_dilate(self.marker, self.bi_img, self.se)

		# elif self.btn13.isChecked():
		# 	isBinary = True
		# 	if self.marker.size == 1:
		# 		QMessageBox.information(self,'Fail','No marker selected.')
		# 		return
		# 	else:
		# 		res = cond_erode(self.marker, self.bi_img, self.se)

		elif self.btn21.isChecked():
			res = gradient(self.image, self.se, self.cbbox2.currentIndex())
		elif self.btn22.isChecked():
			res = CBR(self.image, self.se)
		elif self.btn23.isChecked():
			res = OBR(self.image, self.se)

		# show image
		self.cur_img = res
		height, width = res.shape
		bytesPerline = width
		
		self.qImg = QImage(res.data, width, height, bytesPerline, QImage.Format_Indexed8)
		img = QPixmap.fromImage(self.qImg)
		self.imgLabel.setPixmap(img)

		#refresh
		self.imgLabel.resize(1,1)
		# QApplication.processEvents()


	def load_image(self):
		fname, _ = QFileDialog.getOpenFileName(self, 'select image', '', 'Image files(*.jpg *.jpeg *.png)')
		# self.imgLabel.setPixmap(QPixmap(fname))
		if fname:
			self.image = cv2.imread(fname, 0) # read greyscale image
			# self.b_image, self.g_image, self.r_image = cv2.split(self.image)
			height, width = self.image.shape
			
			# if height >= width:
			# 	_height = 450
			# 	_width = int(width * _height/height)
			# else:
			# 	_width = 450
			# 	_height = int(height * _width/width)

			_height = max(450, int(height * 450/width))
			_width = max(450, int(width * 450/height))
			bytesPerline = _width

			self.image = cv2.resize(self.image, (_width, _height))
			ret, self.bi_img = cv2.threshold(self.image, 150, 255, cv2.THRESH_BINARY)
			self.qImg = QImage(self.image.data, _width, _height, bytesPerline, QImage.Format_Indexed8)
			img = QPixmap.fromImage(self.qImg)
			self.imgLabel.setPixmap(img)
			self.imgLabel.resize(1,1)


	def save(self):
		if self.image.size == 1:
			QMessageBox.information(self,'Fail','No image selected.')
			return
		fname, _ = QFileDialog.getSaveFileName(self, 'Save Image', 'Image', '*.png *.jpg *.bmp')
		if fname is '':
			QMessageBox.information(self,'Fail','Image name can not be empty.')
			return
		cv2.imwrite(fname, self.cur_img)

	def readSe(self):
		text = self.seText.toPlainText()
		textlist = text.split()
		mtx = []
		for li in textlist:
			line = li.split(',')
			line = [int(i) for i in line]
			if len(mtx) !=0 and len(line) != len(mtx[0]) :
				QMessageBox.information(self,'Fail','Invalid structure element.')
				return
			mtx.append(line)
		self.se = np.array(mtx)

	def load_marker(self):
		fname, _ = QFileDialog.getOpenFileName(self, 'select a marker', '', 'Image files(*.jpg *.jpeg *.png)')
		if fname:
			self.marker = cv2.imread(fname, 0) # read greyscale image
			ret, self.marker = cv2.threshold(self.marker, 150, 255, cv2.THRESH_BINARY)
			height, width = self.marker.shape
			_height = max(450, int(height * 450/width))
			_width = max(450, int(width * 450/height))
			self.marker = cv2.resize(self.marker, (_width, _height))
			if(self.marker.shape != self.image.shape):
				QMessageBox.information(self,'Fail','Marker should have the same as mask image!')
				return 
			self.markerLabel.setText(fname)


	def convert_binary(self):
		if self.image.size == 1:
			QMessageBox.information(self,'Fail','No image selected.')
			return

		self.cur_img = self.bi_img
		height, width = self.bi_img.shape
		bytesPerline = width
		# ret, self.bi_img = cv2.threshold(self.image, 150, 255, cv2.THRESH_BINARY)
		self.qImg = QImage(self.bi_img.data, width, height, bytesPerline, QImage.Format_Indexed8)
		img = QPixmap.fromImage(self.qImg)
		self.imgLabel.setPixmap(img)
		self.imgLabel.resize(1,1)
		self.cur_img = self.bi_img


if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = imageProcessing()
	sys.exit(app.exec_())


