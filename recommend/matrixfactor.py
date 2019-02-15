import sys

import numpy as np
import pandas as pd
from recommend.models import UserRating
import scipy.optimize


def MFRecommender():
    def normalize(y, R):
        ymean = np.sum(y, axis=1) / np.sum(R, axis=1)
        ymean = ymean.reshape((ymean.shape[0], 1))
        return y - ymean, ymean

    def flattenp(x, thet):
        return np.concatenate((x.flatten(), thet.flatten()))

    def reshapeParams(flattened_xandthet, nm, nu, nf):
        assert flattened_xandthet.shape[0] == int(nm * nf + nu * nf)
        rex = flattened_xandthet[:int(nm * nf)].reshape((nm, nf))
        rethet = flattened_xandthet[int(nm * nf):].reshape((nu, nf))
        return rex, rethet

    def ccosfun(pparams, y, R, nu, nm, nf, plambda=0.):
        x, thet = reshapeParams(pparams, nm, nu, nf)
        term1 = x.dot(thet.T)
        term1 = np.multiply(term1, R)
        cost = 0.5 * np.sum(np.square(term1 - y))
        cost += (plambda / 2.) * np.sum(np.square(thet))
        cost += (plambda / 2.) * np.sum(np.square(x))
        return cost

    def cgradfun(pparams, y, R, nu, nm, nf, plambda=0.):
        x, thet = reshapeParams(pparams, nm, nu, nf)
        term1 = x.dot(thet.T)
        term1 = np.multiply(term1, R)
        term1 -= y
        xgrad = term1.dot(thet)
        thetgrad = term1.T.dot(x)
        xgrad += plambda * x
        thetgrad += plambda * thet
        return flattenp(xgrad, thetgrad)

    df = pd.DataFrame(list(UserRating.objects.all().values()))
    print(df)
    nu = int(df['user'].astype(int).max())
    nm = int(df['movie'].astype(int).max())
    print()
    print(nu,nm)
    nf = 10
    y = np.zeros((nm, nu))
    print(df.itertuples())
    for row in df.itertuples():
        print(row)
        print(y)
        print(int(row[3]) - 1, int(row[5]) - 1)
        y[int(row[3]) - 1, int(row[5]) - 1] = int(row[4])
    R = np.zeros((nm, nu))
    for i in range(y.shape[0]):
        for j in range(y.shape[1]):
            if y[i][j] != 0:
                R[i][j] = 1

    ynorm, ymean = normalize(y, R)
    x = np.random.rand(nm, nf)
    thet = np.random.rand(nu, nf)
    flat = flattenp(x, thet)
    plambda = 12.2
    result = scipy.optimize.fmin_cg(ccosfun, x0=flat, fprime=cgradfun, args=(y, R, nu, nm, nf, plambda),
                                    maxiter=40, disp=True, full_output=True)
    resx, resthet = reshapeParams(result[0], nm, nu, nf)
    prediction_matrix = resx.dot(resthet.T)
    return prediction_matrix, ymean
