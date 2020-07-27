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
    # 20x20 Input Images
    input_layer_size = 400
    # 10 labels
    num_labels = 10
    #  training data stored in arrays X, y
    data = loadmat(os.path.join('Data', 'ex3data1.mat'))
    X, y = data['X'], data['y'].ravel()
    y[y == 10] = 0
    m = y.size
    theta_t = np.array([-2, -1, 1, 2], dtype=float)
    X_t = np.concatenate(
        [np.ones((5, 1)), np.arange(1, 16).reshape(5, 3, order='F')/10.0],
        axis=1)
    y_t = np.array([1, 0, 1, 0, 1])
    lambda_t = 3
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

