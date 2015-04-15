import cv2
import numpy as np
import os
from datetime import datetime
from scipy.cluster.vq import *
from featureExtractor import *
from helper import *
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn import svm
from sklearn.preprocessing import StandardScaler

class trainer():

	def __init__( self, training_path, testing_path ):
		self.training_path = training_path
		self.testing_path = testing_path
		self.training_image_list = []
		self.testing_image_list = []
		self.training_labels = []
		self.testing_labels = []
		self.class_map = {}

	def get_training_image_list( self ):
		classes = os.listdir( self.training_path )
		cid = 0
		for c in classes:
			cid = cid + 1
			self.class_map[cid] = c
			class_path = os.path.join( self.training_path, c )
			images = os.listdir( class_path )
			n = len( images )
			self.training_labels.extend( [cid] * n )
			for i in images:
				img_path = os.path.join( class_path, i )
				self.training_image_list.append( img_path )

	def get_testing_image_list( self ):
		images = os.listdir( self.testing_path )
		for i in images:
			img_path = os.path.join( self.testing_path, i )
			self.testing_image_list.append( img_path )

	def preprocess( self, features ):
		self.scaler = StandardScaler()
		self.scaler.fit( features )

	def train( self ):
		self.get_training_image_list()
		f = featurePooling( self.training_image_list )
		f.getFeatures()
		features = f.features
		self.preprocess( features )
		features = self.scaler.transform( features );
		self.clf = svm.SVC()
		self.clf.fit( features, self.training_labels )

	def classify( self ):
		self.train()
		self.get_testing_image_list()
		f = featurePooling( self.testing_image_list )
		f.getFeatures()
		features = f.features
		features = self.scaler.transform( features )
		self.testing_labels = self.clf.predict( features )


if __name__ == '__main__' :
	training_path = 'data/training'
	testing_path = 'data/testing'
	print 'Script started at', datetime.now()
	f = trainer( training_path, testing_path )
	f.classify()
	print [f.class_map[cid] for cid in f.testing_labels]
	print 'Script finished at', datetime.now()
