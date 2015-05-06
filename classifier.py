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

	def __init__( self, training_path, testing_path ):
		self.training_path = training_path
		self.testing_path = testing_path
		self.training_features = None
		self.testing_features = None
		self.training_image_list = []
		self.testing_image_list = []
		self.training_labels = []
		self.testing_labels = []
		self.predicted_testing_labels = []
		self.class_map = {}
		self.n_classes = len( os.listdir( os.path.join( '.', 'data', 'training' ) ) )
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
		self.get_training_image_list()
		self.get_testing_image_list()

	def get_training_image_list( self ):
		classes = os.listdir( self.training_path )
		cid = 0
		for c in classes:
			self.class_map[c] = cid
			class_path = os.path.join( self.training_path, c )
			images = os.listdir( class_path )
			n = len( images )
			self.training_labels.extend( [cid] * n )
			for i in images:
				img_path = os.path.join( class_path, i )
				self.training_image_list.append( img_path )
			cid = cid + 1

	def get_testing_image_list( self ):
		classes = os.listdir( self.testing_path )
		for c in classes:
			cid = self.class_map[c]
			class_path = os.path.join( self.testing_path, c )
			images = os.listdir( class_path )
			n = len( images )
			self.testing_labels.extend( [cid] * n )
			for i in images:
				img_path = os.path.join( class_path, i )
				self.testing_image_list.append( img_path )

	def preprocess( self, features ):
		self.scaler = StandardScaler()
		self.scaler.fit( features )

	def train( self, classifier ):
		if self.training_features is None:
			self.loadFeatures()
		self.classifiers[ classifier ].fit( self.training_features, self.training_labels )

	def classify( self, classifier ):
		if self.testing_features is None:
			self.train(classifier)
		self.predicted_testing_labels = self.classifiers[ classifier ].predict( self.testing_features )

	def loadFeatures( self ):
		if os.path.exists( os.path.join( 'data/features/features.lock' ) ):
			training_file = open( 'data/features/training.npy' )
			self.training_features = np.load( training_file )
			training_file.close()

			testing_file = open( 'data/features/testing.npy' )
			self.testing_features = np.load( testing_file )
			testing_file.close()

		else:
			training_f = featurePooling( self.training_image_list )
			self.voc = training_f.getFeatures()
			training_features = training_f.features
			self.preprocess( training_features )
			self.training_features = self.scaler.transform( training_features )

			testing_f = featurePooling( self.testing_image_list, 1 )
			testing_f.getFeatures( self.voc )
			testing_features = testing_f.features
			self.testing_features = self.scaler.transform( testing_features )

			training_file = open( 'data/features/training.npy', 'w' )
			np.save( training_file, self.training_features )
			training_file.close()

			testing_file = open( 'data/features/testing.npy', 'w' )
			np.save( testing_file, self.testing_features )
			testing_file.close()

			lock_file = open( 'data/features/features.lock', 'w' )
			lock_file.write( self.voc )
			lock_file.close()

def final_classification( f, classifier_type ):
	f.classify( classifier_type )
	total_samples = 0
	correct_samples = 0
	for actual, predicted in zip(f.testing_labels, f.predicted_testing_labels):
		if actual == predicted:
			correct_samples += 1
		total_samples += 1
	print classifier_type, correct_samples, total_samples, (correct_samples * 1.0) / (total_samples * 1.0)

if __name__ == '__main__' :
	print 'Script started at', datetime.now()
	training_path = 'data/training'
	testing_path = 'data/testing'
	classifiers = ['knn', 'svm_linear', 'svm', 'tree', 'rf', 'adb', 'gauss', 'lda', 'qda', 'ann']
	classifier_type = 'svm'

	f = classifier( training_path, testing_path )
	f.loadFeatures()
	# final_classification( f, classifier_type )

	print 'Script finished at', datetime.now()
