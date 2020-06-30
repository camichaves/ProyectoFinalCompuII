from scipy import optimize
from lrCostFunction import lrCostFunction
import numpy as np
import concurrent.futures


def calculateThetas(c, X, y, lambda_, n):
    initial_theta = np.zeros(n + 1)
    options = {'maxiter': 50}
    res = optimize.minimize(lrCostFunction,
                            initial_theta,
                            (X, (y == c), lambda_),
                            jac=True,
                            method='CG',
                            options=options)
    return res.x


def oneVsAll(X, y, num_labels, lambda_):
    m, n = X.shape

    all_theta = np.zeros((num_labels, n + 1))

    X = np.concatenate([np.ones((m, 1)), X], axis=1)
    hijos = concurrent.futures.ProcessPoolExecutor()
    hn = []
    for c in np.arange(num_labels):
        hn.append(hijos.submit(calculateThetas(c, X, y, lambda_, n)))

    for f in range(len(hn)):
        all_theta[f] = hn[f].result
        #     initial_theta = np.zeros(n + 1)
        #     options = {'maxiter': 50}
        #     res = optimize.minimize(lrCostFunction,
        #                             initial_theta,
        #                             (X, (y == c), lambda_),
        #                             jac=True,
        #                             method='CG',
        #                             options=options)

        # all_theta[c] = res.x

    # ============================================================
    return all_theta
