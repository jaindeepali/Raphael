import cv2
import numpy as np

def SIFT ( img ):
	sift = cv2.SIFT()
	kp, des = sift.detectAndCompute( img, None )
	print des[0]

	img = cv2.drawKeypoints( img, kp, flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS )

	cv2.imwrite( 'images/sample_sift_keypoints.png', img)

if __name__ == "__main__":

	img = cv2.imread('images/sample.png')
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	SIFT( gray )