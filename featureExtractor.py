import cv2
import numpy as np
from scipy.cluster.vq import *
from helper import *

class featureDetector():

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

class featurePooling():

	def __init__( self, image_list ):
		self.image_list = image_list
		self.descriptor_pool = None
		self.image_data = []
		self.voc = None
		self.features = None

	def clusterSIFTDescriptors( self, k ):
		voc, variance = kmeans(self.descriptor_pool, k, 1)
		self.voc = voc

	def getFeatures( self ):

		# Get features of all images in self.image_list

		for img_path in self.image_list:

			image = {}
			image['path'] = img_path

			f = featureDetector( img_path )
			f.preprocess()
			des = f.SIFT()

			image['descriptors'] = des
			image['no_of_descriptors'] = len(des)
			image['brightness'] = f.brightness()

			if self.descriptor_pool == None :
				self.descriptor_pool = des
			else:
				self.descriptor_pool = np.vstack( ( self.descriptor_pool, des ) )

			self.image_data.append( image )

		k = 100
		self.clusterSIFTDescriptors( k )

		for img in self.image_data:
			hist = createHistogram( img['descriptors'], self.voc, k )
			img['SIFThistogram'] = hist
			img['features'] = hist
			img['features'] = np.append( img['features'], img['brightness'] )

			if self.features == None:
				self.features = img['features']
			else:
				self.features = np.vstack( ( self.features, img['features'] ) )

if __name__ == "__main__":

	sample_path = 'data/sample/sample.png'
	f = featureExtractor( sample_path )
	f.preprocess()
	print f.brightness()
	print f.SIFT()