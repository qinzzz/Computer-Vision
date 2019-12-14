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

	dst = np.zeros((h,w))

	for i in range(h):
		for j in range(w):
			if np.sum(image_extend[i:i+se_h, j:j+se_w] * se) == 0:
				dst[i,j] = 0
			else:
				dst[i,j] = 255

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
	# print(image)
	dst = np.zeros((h,w))

	for i in range(h):
		for j in range(w):

			if np.sum(image_extend[i:i+se_h, j:j+se_w] * se) == 255* np.sum(se):
				dst[i,j] = 255
			else:
				dst[i,j] = 0

	return np.uint8(dst)


def edge_detection(image, se, mode=0 ): # mode: 0-standard 1-external 2-internal
	h, w = image.shape
	# dst = np.zeros((h,w))
	dilate_image = dilate(image, se)
	erode_image = erode(image, se)
	if mode == 0:
		dst = dilate_image - erode_image
	elif mode ==1:
		dst = dilate_image - image
	elif mode == 2:
		dst = image - erode_image

	return np.uint8(dst)


def cond_dilate(marker, mask, se):
	h, w  = marker.shape
	prevR = marker.copy()
	di = dilate(marker, se)
	R = np.minimum(di, mask)
	cnt = 0
	while not (prevR == R).all():
		cnt+=1
		prevR = R.copy()
		di = dilate(di, se)
		R = np.minimum(di, mask)
		# if cnt% 10 ==0:
		# 	cv2.imshow('cond_dilate'+str(cnt), R)
	print(cnt)
	return np.uint8(R)


def cond_erode(marker, mask, se):
	h, w  = marker.shape
	prevR = marker.copy()
	marker = erode(marker, se)
	R = np.maximum(marker, mask)
	while not (prevR == R).all():
		prevR = R.copy()
		marker = erode(marker, se)
		R = np.maximum(marker, mask)

	return np.uint8(R)


def main():
	img = cv2.imread('mask.jpg', 0)
	marker = cv2.imread('marker.jpg', 0)
	ret, bi_img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
	cv2.imshow('original image',bi_img)
	se = np.array([[1,1,1], [1,1,1],[1,1,1]])
	dilate_image = dilate(bi_img, se)
	erode_image = erode(bi_img, se)
	cond_di = cond_dilate(marker, bi_img, se)
	# cond_ed = cond_erode(dilate_image, img, se)
	cv2.imshow('dilate', dilate_image)
	cv2.imshow('erode', erode_image)
	cv2.imshow('cond_dilate', cond_di)
	# cv2.imshow('cond_erode', cond_ed)
	# cv2. imshow('edge', edge_detection(bi_img, se))
	cv2.waitKey ()  
	cv2.destroyAllWindows()


if __name__ == "__main__":
	main()
