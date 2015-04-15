import cv2
import numpy as np
from scipy.cluster.vq import *
from helper import *

class featureDetector():

	def __init__( self, path ):
		self.path = path
		self.img = cv2.imread( self.path )

	def preprocess ( self ):
		self.bw_img = cv2.cvtColor( self.img, cv2.COLOR_BGR2GRAY )
		self.HSVimg = cv2.cvtColor( self.img, cv2.COLOR_BGR2HSV )

	def SIFT ( self ):
		sift = cv2.SIFT()
		kp, des = sift.detectAndCompute( self.bw_img, None )

		# out_img = cv2.drawKeypoints( self.img, kp, flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS )
		# cv2.imwrite( 'data/sample/sample_sift_keypoints.png', out_img)

		return des

	def brightness ( self ):
		avg = np.average( self.bw_img )
		return avg

	def saturationHist ( self ):
		shist = cv2.calcHist( [self.HSVimg], [1], None, [50], [0,256] )
		shist = np.transpose( shist )[0]
		return shist

	def darkPixels ( self ):
		dhist = cv2.calcHist( [self.HSVimg], [2], None, [3], [0,256] )
		dhist = np.transpose( dhist )[0]
		darkness = dhist[0] / ( dhist[0] + dhist[1] + dhist[2] )
		return darkness

	def colorHist ( self ):
		bhist = cv2.calcHist( [self.img], [0], None, [50], [0,256] )
		ghist = cv2.calcHist( [self.img], [1], None, [50], [0,256] )
		rhist = cv2.calcHist( [self.img], [2], None, [50], [0,256] )
		bhist = np.transpose( bhist )[0]
		ghist = np.transpose( ghist )[0]
		rhist = np.transpose( rhist )[0]
		colorHist = np.append( bhist, [ ghist, rhist ] )
		return colorHist

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
			image['colorHist'] = f.colorHist()
			image['saturationHist'] = f.saturationHist()
			image['darkPixels'] = f.darkPixels()

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
			img['features'] = np.append( img['features'], img['colorHist'] )
			img['features'] = np.append( img['features'], img['saturationHist'] )
			img['features'] = np.append( img['features'], img['darkPixels'] )

			if self.features == None:
				self.features = img['features']
			else:
				self.features = np.vstack( ( self.features, img['features'] ) )

if __name__ == "__main__":

	sample_path = 'data/sample/sample2.png'
	f = featureDetector( sample_path )
	f.preprocess()
	print f.darkPixels()
