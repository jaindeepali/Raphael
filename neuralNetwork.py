from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.structure import TanhLayer
from pybrain.supervised.trainers import BackpropTrainer
import numpy as np

class neuralNetwork():

	def __init__( self ):
		self.net = None

	def fit( self, X, Y ):
		n_features = X.shape[1]
		self.ds = SupervisedDataSet( n_features, 1 )
		for train, target in zip( X, Y ):
			self.ds.addSample( train, target )

		self.net = buildNetwork( n_features, 2*n_features, 1, hiddenclass=TanhLayer )
		self.trainer = BackpropTrainer( self.net, self.ds )
		self.trainer.train()

	def predict( self, X ):
		labels = []
		for test in X:
			labels.append( self.net.activate( test )[0] )
		return labels

if __name__ == '__main__':
	X = np.array([[ 0.,  0.],
		[ 0.,  1.],
		[ 1.,  0.],
		[ 1.,  1.]])
	Y = [ 0, 1, 1, 0 ]
	test = np.array([[ 0.,  0.],
		[ 0.,  1.],
		[ 1.,  0.],
		[ 1.,  1.]])
	n = neuralNetwork()
	n.fit( X, Y )
	print n.predict( test )