import os, sys
path = os.path.abspath("/home/toni/.usrconfig/python/")
sys.path.append(path)
import ownUtils
import numpy as np


data = ownUtils.readDataFile("../rawdata/someData.dat")
data = map(np.array, data)
data = map(lambda x : [x[0], x[1] ** 2], data)
ownUtils.writeDataFile("../data/test.dat", data)
