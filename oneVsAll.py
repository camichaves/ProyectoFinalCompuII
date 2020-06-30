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

    futures = {hijos.submit(calculateThetas(c, X, y, lambda_, n)): c
               for c in np.arange(num_labels)
               }

    for f in concurrent.futures.as_completed(futures):
        all_theta[futures[f]] = f.result
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
