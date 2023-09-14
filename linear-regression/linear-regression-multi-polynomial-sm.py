#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures


if __name__ == "__main__":

    x = np.array([0, 1, 5, 1, 15, 2, 25, 5, 35, 11, 45, 15, 55, 34, 60, 35]).reshape((8, 2))
    y = np.array([4, 5, 20, 14, 32, 22, 38, 43])

    xp = PolynomialFeatures(degree=2).fit_transform(x)

    model = sm.OLS(y, xp).fit()
    print(f"{model.summary()}")
    print(f"predict: {model.predict(xp)}")
