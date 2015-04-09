import cv2
import numpy as np

class featureExtractor():

	def __init__( self, path ):
		self.path = path
		self.img = cv2.imread( self.path )

	def preprocess ( self ):
		self.img = cv2.cvtColor( self.img, cv2.COLOR_BGR2GRAY )

	def SIFT ( self ):
		sift = cv2.SIFT()
		kp, des = sift.detectAndCompute( self.img, None )

		# out_img = cv2.drawKeypoints( self.img, kp, flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS )
		# cv2.imwrite( 'data/sample/sample_sift_keypoints.png', out_img)
		
		return des

	def brightness ( self ):
		avg = np.average( self.img )
		return avg

	def texture ( self ):
		return 0

if __name__ == "__main__":

	sample_path = 'data/sample/sample.png'
	f = featureExtractor( sample_path )
	f.preprocess()
	print f.brightness()
	print f.SIFT()