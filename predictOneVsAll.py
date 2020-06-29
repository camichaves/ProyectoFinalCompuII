import numpy as np
import utils


def predictOneVsAll(all_theta, X):
    m = X.shape[0];
    num_labels = all_theta.shape[0]
    p = np.zeros(m)
    X = np.concatenate([np.ones((m, 1)), X], axis=1)

    p = np.argmax(utils.sigmoid(X.dot(all_theta.T)), axis=1)

    # ============================================================
    return p
