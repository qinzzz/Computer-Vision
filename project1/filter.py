import cv2 as cv
import numpy as np
from math import sqrt,pi,exp
from conv_operator import convolve

def extend_image(image,k_size=3):
	h, w  = image.shape
	image_extend = np.zeros((h+k_size-1, w+k_size-1))
	margin_right = k_size//2 
	margin_left = k_size-1-margin_right
	image_extend[margin_right:h+margin_right, margin_right:w+margin_right] = image

	image_extend[0:margin_right, margin_right:w+margin_right] = image[0:margin_right,:]
	image_extend[h+margin_right:, margin_right:w+margin_right] = image[h-margin_left:,:]
	image_extend[margin_right:h+margin_right, 0:margin_right] = image[:, 0:margin_right]
	image_extend[margin_right:h+margin_right, w+margin_right:] = image[:,w-margin_left:]
	return image_extend

def mean_filter(image,kernel_size=3):
	height, width = image.shape
	image_extend = extend_image(image,kernel_size)
	dst = image.copy()
	for i in range(height):
		for j in range(width):
			dst[i,j] = np.mean(image_extend[i:i+kernel_size,j:j+kernel_size])
	return np.uint8(dst)


def median_filter(image,kernel_size=3):
	height, width = image.shape
	image_extend = extend_image(image,kernel_size)
	dst = image.copy()
	for i in range(height):
		for j in range(width):
			dst[i,j] = np.median(image_extend[i:i+kernel_size,j:j+kernel_size])
	return np.uint8(dst)

def gaussian_mtx(kernel_size = 3, sigma = 1.0):
	mtx = np.zeros([kernel_size,kernel_size])
	center = (kernel_size-1)/2
	for i in range(kernel_size):
		for j in range(kernel_size):
			mtx[i][j] = (1/(sigma*sigma*sqrt(2*pi)))*exp(-((center-i)*(center-i)+(center-j)*(center-j))/(2*sigma*sigma))
	mtx = mtx / np.sum(mtx)
	# print(mtx)
	return mtx


def gaussian_filter(image,kernel_size=3,sigma=1.0):
	height, width = image.shape
	r = (kernel_size-1)//2
	kernel = gaussian_mtx(kernel_size,sigma)
	dst = convolve(image,kernel)
	return np.uint8(dst)


def main():
	image = cv.imread('pic.jpg', cv.IMREAD_GRAYSCALE)
	cv.imshow('original image',image)
	mean = mean_filter(image)
	median = median_filter(image)
	gauss = gaussian_filter(image)
	cv.imshow('mean_filter', mean)
	cv.imshow('median_filter', median)
	cv.imshow('gaussian_filter', gauss)
	cv.waitKey ()  
	cv.destroyAllWindows()


if __name__ == "__main__":
	main()
