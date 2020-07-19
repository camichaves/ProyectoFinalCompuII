import os
import numpy as np
from matplotlib import pyplot
from scipy import optimize
from scipy.io import loadmat
import utils
from oneVsAll import oneVsAll
from predictOneVsAll import predictOneVsAll
import mmap
import sys
sys.path.insert(1,"/home/camila/Documentos/Proyecto/ProyectoFinalCompuII/Global")
from glob import generarmem
#%matplotlib inline
#jdk-11.0.5

# 20x20 Input Images
input_layer_size = 400

# 10 labels
num_labels = 10

#  training data stored in arrays X, y
data = loadmat(os.path.join('Data', 'ex3data1.mat'))
X, y = data['X'], data['y'].ravel()
print(X[1,:])

y[y == 10] = 0
m = y.size

# Randomly select 100 data points to display
rand_indices = np.random.choice(m, 100, replace=False)
sel = X[rand_indices, :]
utils.displayData(sel)


theta_t = np.array([-2, -1, 1, 2], dtype=float)
X_t = np.concatenate([np.ones((5, 1)), np.arange(1, 16).reshape(5, 3, order='F')/10.0], axis=1)
y_t = np.array([1, 0, 1, 0, 1])
lambda_t = 3


lambda_ = 0.1
all_theta = oneVsAll(X, y, num_labels, lambda_)

pred = predictOneVsAll(all_theta, X)
print('Training Set Accuracy: {:.2f}%'.format(np.mean(pred == y) * 100))
print('Thetas: ')
print(np.matrix(all_theta))
np.savetxt("thetas.txt",all_theta)
generarmem()
glob.cargarmem(all_thetas)
print(glob.leermem())
indices = np.random.permutation(m)
if indices.size > 0:
    i, indices = indices[0], indices[1:]
    utils.displayData(X[i, :], figsize=(4, 4))
    pred = predictOneVsAll(all_theta, X[i, :])
    print('Prediccion de prueba: {}'.format(*pred))
else:
    print('No hay más imagenes por mostrar!')
