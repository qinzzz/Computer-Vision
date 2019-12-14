import cv2 as cv
import numpy as np

def convolve(image, kernel):
	h, w  = image.shape
	k_size = kernel.shape[0]
	image_extend = np.zeros((h+k_size-1, w+k_size-1))
	margin_right = k_size//2 
	margin_left = k_size-1-margin_right
	image_extend[margin_right:h+margin_right, margin_right:w+margin_right] = image

	image_extend[0:margin_right, margin_right:w+margin_right] = image[0:margin_right,:]
	image_extend[h+margin_right:, margin_right:w+margin_right] = image[h-margin_left:,:]
	image_extend[margin_right:h+margin_right, 0:margin_right] = image[:, 0:margin_right]
	image_extend[margin_right:h+margin_right, w+margin_right:] = image[:,w-margin_left:]
	# print(image_extend)
	# print(image)
	dst = np.zeros((h,w))
	for i in range(h):
		for j in range(w):
			dst[i,j] = np.sum(image_extend[i:i+k_size, j:j+k_size]*kernel)
	
	return dst

def roberts(image):
	Gx = np.array([[1,0],[0,-1]])
	Gy = np.array([[0,1],[-1,0]])
	# conv135 = cv.filter2D(image, -1, Gx)
	# conv45 = cv.filter2D(image, -1, Gy)
	conv135 = convolve(image, Gx)
	conv45 = convolve(image, Gy)
	edge = np.abs(conv135) + np.abs(conv45)
	# edge = np.sqrt(np.power(conv135, 2.0) + np.power(conv45, 2.0))
	# print(edge)

	return np.uint8(edge)


def prewitt(image):
	Gx = np.array([[-1,-1,-1],[0,0,0],[1,1,1]])
	Gy = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
	# conv135 = cv.filter2D(image, -1, Gx)
	# conv45 = cv.filter2D(image, -1, Gy)
	conv135 = convolve(image, Gx)
	conv45 = convolve(image, Gy)
	# edge = np.sqrt(np.power(conv135, 2.0) + np.power(conv45, 2.0))
	edge = np.abs(conv135) + np.abs(conv45)
	# print(edge)

	return np.uint8(edge)


def sobel(image):
	
	Gx = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
	Gy = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
	# conv135 = cv.filter2D(image, -1, Gx)
	# conv45 = cv.filter2D(image, -1, Gy)
	conv135 = convolve(image, Gx)
	conv45 = convolve(image, Gy)
	edge = np.sqrt(np.power(conv135, 2.0) + np.power(conv45, 2.0))
	# edge = np.abs(conv135) + np.abs(conv45)
	# print(edge)

	return np.uint8(edge)


def main():
	image = cv.imread('blur.jpg', cv.IMREAD_GRAYSCALE)
	cv.imshow('original image',image)
	edge_rob = roberts(image)
	edge_sob = sobel(image)
	edge_prew = prewitt(image)
	cv.imshow('robert operator', edge_rob)
	cv.imshow('prewitt operator', edge_prew)
	cv.imshow('sobel operator', edge_sob)
	cv.waitKey ()  
	cv.destroyAllWindows()

if __name__ == "__main__":
	main()



