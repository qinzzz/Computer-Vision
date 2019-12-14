'''
date: 2019/11/06 
creatd by: wqx

Convolution and Image Filters

Requirement：
1. Program to realize the convolution operation and the next filters
 - Roberts operator; Prewitt operator; Sobel operator;
 - Gaussian filter, mean filter and Median filter
 - Kernal size and sigma adjustable
2. Design proper UI and display I/O images

'''
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from filter import mean_filter, median_filter, gaussian_filter
from conv_operator import roberts, prewitt, sobel

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
		# self.r_image = np.ndarray(())
		# self.g_image = np.ndarray(())
		# self.b_image = np.ndarray(())
		self.initUI()


	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		# left
		selectLabel = QLabel('Target Image: ')
		selectBtn = QPushButton("Select")
		self.imgLabel = QLabel()

		#right
		self.subTitle = QLabel("Select an operation...")
		self.subTitle.setObjectName('h1')
		self.filterLabel = QLabel("Filter")
		self.operatorLabel = QLabel("Convolution Operator")
		self.filterLabel.setObjectName('h2')
		self.operatorLabel.setObjectName('h2')

		self.btn11 = QRadioButton("Roberts operator")
		self.btn12 = QRadioButton("Prewitt operator")
		self.btn13 = QRadioButton("Sobel operator")

		self.btn21 = QRadioButton("Median filter")
		self.btn22 = QRadioButton("Mean filter")
		self.btn23 = QRadioButton("Gaussian filter")
		self.btn21.setChecked(True) # default

		ksizeLabel = QLabel("Kernel size:")
		self.numLabel = QLabel("3")
		sigmaLabel = QLabel("Sigma size:")
		self.sigmanumLabel = QLabel("1")

		self.splider = QSlider(Qt.Horizontal)
		self.splider.valueChanged.connect(self.kernel_size)
		self.splider.setMinimum(1)
		self.splider.setMaximum(20)
		self.splider.setSingleStep(1)
		self.splider.setValue(3)

		self.splider2 = QSlider(Qt.Horizontal)
		self.splider2.valueChanged.connect(self.sigma_size)
		self.splider2.setMinimum(1)
		self.splider2.setMaximum(100)
		self.splider2.setSingleStep(1)
		self.splider2.setValue(10)
		

		# add adjustble kernel size

		submitBtn = QPushButton("Confirm")
		saveBtn = QPushButton("Save")
		cancelBtn = QPushButton("Cancel")

		# click select
		selectBtn.clicked.connect(self.load_image)
		# click submit
		submitBtn.clicked.connect(self.submit)
		saveBtn.clicked.connect(self.save)
		cancelBtn.clicked.connect(self.close)

		hboxLeftUp = QHBoxLayout()
		hboxLeftUp.addWidget(selectLabel,0,Qt.AlignLeft)
		hboxLeftUp.addWidget(selectBtn,1,Qt.AlignLeft)

		vboxLeft = QVBoxLayout()
		vboxLeft.addLayout(hboxLeftUp)
		vboxLeft.addWidget(self.imgLabel)

		hboxRightDown = QHBoxLayout()
		hboxRightDown.addWidget(submitBtn)
		hboxRightDown.addWidget(saveBtn)
		hboxRightDown.addWidget(cancelBtn)

		hboxRight1 = QHBoxLayout()
		hboxRight1.addWidget(ksizeLabel)
		hboxRight1.addWidget(self.numLabel, 0, Qt.AlignLeft)

		hboxRight2 = QHBoxLayout()
		hboxRight2.addWidget(sigmaLabel)
		hboxRight2.addWidget(self.sigmanumLabel, 0, Qt.AlignLeft)

		vboxRight = QVBoxLayout()
		vboxRight.addWidget(self.subTitle,0,Qt.AlignTop)
		vboxRight.addStretch(1)
		vboxRight.addWidget(self.filterLabel)
		vboxRight.addStretch(1)
		vboxRight.addWidget(self.btn21)
		vboxRight.addWidget(self.btn22)
		vboxRight.addWidget(self.btn23)
		vboxRight.addLayout(hboxRight1)
		vboxRight.addWidget(self.splider)
		vboxRight.addLayout(hboxRight2)
		vboxRight.addWidget(self.splider2)


		vboxRight.addStretch(1)
		vboxRight.addWidget(self.operatorLabel)
		vboxRight.addStretch(1)
		vboxRight.addWidget(self.btn11)
		vboxRight.addWidget(self.btn12)
		vboxRight.addWidget(self.btn13)
		vboxRight.addStretch(10)

		# vboxRight.addStretch(1)
		vboxRight.addLayout(hboxRightDown)


		hboxAll = QHBoxLayout()
		hboxAll.addLayout(vboxLeft)
		hboxAll.addStretch(6)
		hboxAll.addLayout(vboxRight)
		hboxAll.addStretch(3)

		self.setLayout(hboxAll)
		self.show()


	def submit(self):
		if self.image.size == 1:
			QMessageBox.information(self,'Fail','No image selected.')
			return
		if self.btn11.isChecked():
			res = roberts(self.image)
		elif self.btn12.isChecked():
			res = prewitt(self.image)
		elif self.btn13.isChecked():
			res = sobel(self.image)
		elif self.btn21.isChecked():
			res = median_filter(self.image, self.ksize)
		elif self.btn22.isChecked():
			res = mean_filter(self.image, self.ksize)
		elif self.btn23.isChecked():
			res = gaussian_filter(self.image, self.ksize, self.sigma)

		# show image
		height, width = res.shape

		bytesPerline = width
		self.qImg = QImage(res.data, width, height, bytesPerline, QImage.Format_Indexed8)
		img = QPixmap.fromImage(self.qImg)
		self.imgLabel.setPixmap(img)
		# size = self.imgLabel.size()
		self.imgLabel.resize(1,1)
		#refresh
		QApplication.processEvents()



	def load_image(self):
		fname, _ = QFileDialog.getOpenFileName(self, 'select image', '', 'Image files(*.jpg *.jpeg *.png)')
		# self.imgLabel.setPixmap(QPixmap(fname))
		if fname:
			self.image = cv2.imread(fname, 0) # read greyscale image
			# self.b_image, self.g_image, self.r_image = cv2.split(self.image)
			height, width = self.image.shape

			if height >= width:
				_height = 450
				_width = width * _height/height
			else:
				_width = 450
				_height = height * _width/width

			_width = int(_width)	
			_height = int(_height)
			bytesPerline = _width

			self.image = cv2.resize(self.image, (_width, _height))
			# self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
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
		cv2.imwrite(fname, self.image)


	def kernel_size(self):
		self.ksize = self.splider.value()
		self.numLabel.setText(str(self.ksize))
		

	def sigma_size(self):
		self.sigma = self.splider2.value() / 10.0
		self.sigmanumLabel.setText(str(self.sigma))

if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = imageProcessing()
	sys.exit(app.exec_())


