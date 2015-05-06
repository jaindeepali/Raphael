import cv2
import numpy as np
from scipy.cluster.vq import *
from helper import *
import os

HISTOGRAM_BINS = 10
KMEANS_CLUSTERS_FOR_SIFT = 25

class featureDetector():

	def __init__( self, path ):
		self.path = path
		self.img = cv2.imread( self.path )

	def preprocess( self ):
		self.YUVimg = cv2.cvtColor( self.img, cv2.COLOR_BGR2YUV )
		self.bw_img = cv2.cvtColor( self.img, cv2.COLOR_BGR2GRAY )
		self.HSVimg = cv2.cvtColor( self.img, cv2.COLOR_BGR2HSV )

	def SIFT( self ):
		sift = cv2.SIFT()
		kp, des = sift.detectAndCompute( self.bw_img, None )

		# out_img = cv2.drawKeypoints( self.img, kp, flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS )
		# cv2.imwrite( 'data/sample/sample_sift_keypoints.png', out_img)

		return des

	def brightness( self ):
		hist = cv2.calcHist( [self.YUVimg], [0], None, [HISTOGRAM_BINS], [0,256] )
		hist = np.transpose( hist )[0]
		return hist

	def saturationHist( self ):
		shist = cv2.calcHist( [self.HSVimg], [1], None, [HISTOGRAM_BINS], [0,256] )
		shist = np.transpose( shist )[0]
		return shist

	def colorHist( self ):
		bhist = cv2.calcHist( [self.img], [0], None, [HISTOGRAM_BINS], [0,256] )
		ghist = cv2.calcHist( [self.img], [1], None, [HISTOGRAM_BINS], [0,256] )
		rhist = cv2.calcHist( [self.img], [2], None, [HISTOGRAM_BINS], [0,256] )
		bhist = np.transpose( bhist )[0]
		ghist = np.transpose( ghist )[0]
		rhist = np.transpose( rhist )[0]
		colorHist = np.append( bhist, [ ghist, rhist ] )
		return colorHist

class featurePooling():

	def __init__( self, image_list, test = 0 ):
		self.image_list = image_list
		self.test = test
		self.descriptor_pool = None
		self.image_data = []
		self.voc = None
		self.features = None

	def clusterSIFTDescriptors( self, k ):
		voc, variance = kmeans2(self.descriptor_pool, k)
		self.voc = voc

	def getFeatures( self, voc = None ):

		# Get features of all images in self.image_list

		for img_path in self.image_list:

			image = {}
			image['path'] = img_path

			f = featureDetector( img_path )
			f.preprocess()
			des = f.SIFT()

			if des is None:
				os.remove(img_path)
				print 'No descriptors found for image'
				continue

			image['descriptors'] = des
			image['no_of_descriptors'] = len(des)
			image['brightness'] = f.brightness()
			image['colorHist'] = f.colorHist()
			image['saturationHist'] = f.saturationHist()

			self.image_data.append( image )

			if not self.test:
				if self.descriptor_pool == None :
					self.descriptor_pool = des
				else:
					self.descriptor_pool = np.vstack( ( self.descriptor_pool, des ) )

		print 'inital pass complete'

		if voc == None:
			print 'starting kmeans'
			self.clusterSIFTDescriptors( KMEANS_CLUSTERS_FOR_SIFT )
			print 'kmeans complete'
		else:
			self.voc = voc

		for img in self.image_data:
			hist = createHistogram( img['descriptors'], self.voc, KMEANS_CLUSTERS_FOR_SIFT )
			img['SIFThistogram'] = hist
			img['features'] = hist
			img['features'] = np.append( img['features'], img['brightness'] )
			img['features'] = np.append( img['features'], img['colorHist'] )
			img['features'] = np.append( img['features'], img['saturationHist'] )

			if self.features == None:
				self.features = img['features']
			else:
				self.features = np.vstack( ( self.features, img['features'] ) )

		return self.voc

if __name__ == "__main__":

	sample_path = 'data/sample/sample2.png'
	f = featurePooling( [sample_path] )
	f.getFeatures()
	img = f.image_data[0]
	print 'SIFThistogram', img['SIFThistogram']
	print 'brightness', img['brightness']
	print 'colorHist', img['colorHist']
	print 'saturationHist', img['saturationHist']
