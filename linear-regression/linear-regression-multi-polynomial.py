#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


if __name__ == "__main__":

    x = np.array([0, 1, 5, 1, 15, 2, 25, 5, 35, 11, 45, 15, 55, 34, 60, 35]).reshape((8, 2))
    y = np.array([4, 5, 20, 14, 32, 22, 38, 43])

    x_ = PolynomialFeatures(degree=2, include_bias=False).fit_transform(x)
    model = LinearRegression().fit(x_, y)
    r_sq = model.score(x_, y)
    print(f"residual square: {r_sq}, intercept: {model.intercept_}, slope: {model.coef_}")
    print(f"predict {x_} => {model.predict(x_)}")
    x2 = np.arange(10).reshape(-1, 2)
    x2_ = PolynomialFeatures(degree=2, include_bias=False).fit_transform(x2)
    print(f"predict {x2_} => {model.predict(x2_)}")
