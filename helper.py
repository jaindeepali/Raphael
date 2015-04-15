import numpy as np
from scipy.cluster.vq import *

def createHistogram( descriptor_list, voc, k ):

	features = np.zeros( k, "float32" )
	words, distance = vq(descriptor_list, voc)
	for w in words:
		features[w] += 1
	return features
