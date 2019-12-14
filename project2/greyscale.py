import cv2
import numpy as np


def dilate(image, se):
	h, w  = image.shape
	se_h, se_w = se.shape
	image_extend = np.zeros((h+se_h-1, w+se_w-1))
	left = se_w//2
	right = se_w - left - 1
	up = se_h//2
	down = se_h - up -1
	image_extend[up:h+up, left:w+left] = image
	
	rse = np.flip(se, 1) # 对称翻转

	dst = np.zeros((h,w))

	for i in range(h):
		for j in range(w):
			dst[i,j] = np.max(image_extend[i:i+se_h, j:j+se_w] + rse)
			# dst[i,j] = np.max(image_extend[i:i+se_h, j:j+se_w])
			
	dst[dst>255] = 255
	# print (dst)
	return np.uint8(dst)


def erode(image, se):
	h, w  = image.shape
	se_h, se_w = se.shape
	image_extend = np.zeros((h+se_h-1, w+se_w-1))
	left = se_w//2
	right = se_w - left - 1
	up = se_h//2
	down = se_h - up -1
	image_extend[up:h+up, left:w+left] = image
	# image_extend[0:h, 0:w] = image
	dst = np.zeros((h,w))

	for i in range(h):
		for j in range(w):
			dst[i,j] = np.min(image_extend[i:i+se_h, j:j+se_w] - se)
			# dst[i,j] = np.min(image_extend[i:i+se_h, j:j+se_w])

	dst[dst>255] = 255
	dst[dst<0] = 0
	# print (dst)
	return np.uint8(dst)


def gradient(image, se, mode = 0):	# mode: 0-standard 1-external 2-internal
	h, w = image.shape
	# dst = np.zeros((h,w))
	dilate_image = dilate(image, se)
	erode_image = erode(image, se)
	if mode == 0:
		dst = (dilate_image - erode_image)*0.5
	elif mode ==1 :
		dst = (dilate_image - image)*0.5
	elif mode ==2:
		dst = (image - erode_image)*0.5

	return np.uint8(dst)

def opening(image, se):
	tmp = erode(image, se)
	dst = dilate(tmp, se)
	return dst

def closing(image, se):
	tmp = dilate(image, se)
	dst = erode(tmp, se)
	return dst

def reconstruct(marker, mask, se, mode = 0): # mode: 0-dilate 1-erode
	h, w  = marker.shape
	prevR = marker.copy()
	cnt = 0
	if mode == 0:
		marker = dilate(marker, se)
		R = np.minimum(marker, mask)
		# cv2.imshow('recon'+str(cnt), R)
		while not (prevR == R).all():
			cnt +=1
			prevR = R.copy()
			R = dilate(R, se)
			R = np.minimum(R, mask)
			# if cnt% 10 == 0:
			# 	cv2.imshow('recon'+str(cnt), R)
			
	elif mode == 1:
		marker = erode(marker, se)
		R = np.maximum(marker, mask)
		while not (prevR == R).all():
			cnt +=1
			prevR = R.copy()
			R = erode(R, se)
			R = np.maximum(R, mask)
	print(cnt)
	return np.uint8(R)


def CBR(image, se): # Grayscale Closing by Reconstruction
	tmp = closing(image, se)
	dst = reconstruct(tmp, image, se, 1)
	return dst


def OBR(image, se): # Grayscale Opening by Reconstruction
	tmp = opening(image, se)
	dst = reconstruct(tmp, image, se, 0)
	return dst


def main():
	img = cv2.imread('light.png', 0)
	cv2.imshow('original image',img)
	se = np.zeros((10,10))
	opened = opening(img, se)
	di1 = dilate(img, se)

	# erode_image = erode(img, se)
	# grad = gradient(img,se)
	# recE = reconstruct(erode_image, img, se, 0)
	# recD = reconstruct(dilate_image, img, se, 1)
	# marker = np.zeros(img.shape).astype(np.uint8)
	# marker[10:20] = 100
	# recons = reconstruct(marker, img, se)
	obr = OBR(img, se)
	cbr = CBR(img, se)
	# cl = CBR(img, se)
	# cv2.imshow('marker',marker)
	cv2.imshow('open by reconstruction', obr)
	cv2.imshow('close by reconstruction', cbr)
	cv2.imshow('dilate1', di1)
	cv2.imshow('opening', opened)
	cv2.waitKey ()  
	cv2.destroyAllWindows()


if __name__ == "__main__":
	main()
