import cv2
import numpy as np
import os
from scipy.cluster.vq import *
from featureExtractor import featureExtractor
from helper import *

class trainer():

	def __init__( self, training_path ):
		self.training_path = training_path
		self.descriptor_pool = None
		self.image_data = []
		self.voc = None

	def getFeatures( self ):

		# Get features of all training images

		classes = os.listdir( self.training_path )
		for c in classes:
			class_path = os.path.join( self.training_path, c )
			images = os.listdir( class_path )
			for i in images:
				image = {}

				img_path = os.path.join( class_path, i )
				image['path'] = img_path

				f = featureExtractor( img_path )
				f.preprocess()
				des = f.SIFT()

				image['descriptors'] = des
				image['no_of_descriptors'] = len(des)
				image['class'] = c
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
			img['histogram'] = hist

	def clusterSIFTDescriptors( self, k ):

		voc, variance = kmeans(self.descriptor_pool, k, 1)
		self.voc = voc	

if __name__ == '__main__' :
	path = 'data/training'
	f = trainer( path )
	f.getFeatures()
	print f.image_data
