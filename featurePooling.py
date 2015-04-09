import cv2
import numpy as np
import os
from sklearn.cluster import KMeans
from featureExtractor import featureExtractor

class featurePooling():

	def __init__( self, training_path ):
		self.training_path = training_path

	def getSIFTDescriptors( self ):

		# Get SIFT Descriptors of all images

		self.descriptors = []
		self.descriptor_pool = None

		classes = os.listdir( self.training_path )
		for c in classes:
			class_path = os.path.join( self.training_path, c )
			images = os.listdir( class_path )
			for i in images:
				img_path = os.path.join( class_path, i )
				f = featureExtractor( img_path )
				f.preprocess()
				des = f.SIFT()
				self.descriptors.append( ( img_path, des ) )
				if self.descriptor_pool == None :
					self.descriptor_pool = des
				else:
					self.descriptor_pool = np.vstack( ( self.descriptor_pool, des ) )

	def clusterSIFTDescriptors( self ):
		kmeans = KMeans( n_clusters = 100 )
		kmeans.fit( self.descriptor_pool )
		print kmeans.labels

if __name__ == '__main__' :
	path = 'data/training'
	f = featurePooling( path )
	f.getSIFTDescriptors()
	f.clusterSIFTDescriptors()
	# print f.descriptor_pool
