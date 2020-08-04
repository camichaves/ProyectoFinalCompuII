import os
import numpy as np
from matplotlib import pyplot
from scipy import optimize
from scipy.io import loadmat
import utils
from oneVsAll import oneVsAll
from predictOneVsAll import predictOneVsAll


def calcularThetas():
    print("Calculando thetas para predecir nùmeros....")
    # 20x20 imagenes de Entrada
    input_layer_size = 400
    # 10 labels
    num_labels = 10
    #  traigo las imagenes de MNIST almacenadas
    data = loadmat(os.path.join('Data', 'ex3data1.mat'))
    X, y = data['X'], data['y'].ravel()
    y[y == 10] = 0
    m = y.size
    lambda_ = 0.1
    all_theta = oneVsAll(X, y, num_labels, lambda_)
    pred = predictOneVsAll(all_theta, X)
    print('Training Set Accuracy: {:.2f}%'.format(np.mean(pred == y) * 100))
    np.savetxt("thetas.txt", all_theta)
    indices = np.random.permutation(m)
    i, indices = indices[0], indices[1:]
    pred = predictOneVsAll(all_theta, X[i, :])
    print('Prediccion aleatoria para control: {}'.format(*pred))

if __name__ == "__main__":
    calcularThetas()

