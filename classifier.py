import cv2
import numpy as np
import os
from datetime import datetime
from helper import *
from featureExtractor import *
from neuralNetwork import *
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA
from sklearn.preprocessing import StandardScaler

class classifier():

	def __init__( self, training_path, testing_path, number_of_classes = 3 ):
		self.training_path = training_path
		self.testing_path = testing_path
		self.training_image_list = []
		self.testing_image_list = []
		self.training_labels = []
		self.testing_labels = []
		self.class_map = {}
		self.n_classes = number_of_classes
		self.classifiers = {
			'knn': KNeighborsClassifier( 3 ),
		    'svm_linear': SVC(kernel="linear", C=0.025),
		    'svm': SVC(gamma=2, C=1),
		    'tree': DecisionTreeClassifier(max_depth=5),
		    'rf': RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
		    'adb': AdaBoostClassifier(),
		    'gauss': GaussianNB(),
		    'lda': LDA(),
		    'qda': QDA(),
		    'ann': neuralNetwork( self.n_classes ) }

	def get_training_image_list( self ):
		classes = os.listdir( self.training_path )
		cid = 0
		for c in classes:
			self.class_map[cid] = c
			class_path = os.path.join( self.training_path, c )
			images = os.listdir( class_path )
			n = len( images )
			self.training_labels.extend( [cid] * n )
			for i in images:
				img_path = os.path.join( class_path, i )
				self.training_image_list.append( img_path )
			cid = cid + 1

	def get_testing_image_list( self ):
		images = os.listdir( self.testing_path )
		for i in images:
			img_path = os.path.join( self.testing_path, i )
			self.testing_image_list.append( img_path )

	def preprocess( self, features ):
		self.scaler = StandardScaler()
		self.scaler.fit( features )

	def train( self, classifier ):
		self.get_training_image_list()
		f = featurePooling( self.training_image_list )
		self.voc = f.getFeatures()
		features = f.features
		self.preprocess( features )
		features = self.scaler.transform( features );
		self.classifiers[ classifier ].fit( features, self.training_labels )

	def classify( self, classifier ):
		self.train( classifier )
		self.get_testing_image_list()
		f = featurePooling( self.testing_image_list, 1 )
		f.getFeatures( self.voc )
		features = f.features
		features = self.scaler.transform( features )
		self.testing_labels = self.classifiers[ classifier ].predict( features )


if __name__ == '__main__' :
	training_path = 'data/training'
	testing_path = 'data/testing'
	print 'Script started at', datetime.now()
	f = classifier( training_path, testing_path, 3 )
	# f.classify( 'knn' )
	# f.classify( 'svm_linear' )
	# f.classify( 'svm' )
	# f.classify( 'tree' )
	# f.classify( 'rf' )
	# f.classify( 'adb' )
	# f.classify( 'gauss' )
	# f.classify( 'lda' )
	# f.classify( 'qda' )
	f.classify( 'ann' )
	# print [f.class_map[cid] for cid in f.testing_labels]
	print f.testing_labels
	print 'Script finished at', datetime.now()
