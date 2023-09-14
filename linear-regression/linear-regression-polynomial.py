#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from sklearn.linear_model import LinearRegression

if __name__ == "__main__":
    x = np.array([5, 15, 25, 35, 45, 55]).reshape((-1, 1))
    y = np.array([5, 20, 14, 32, 22, 38])

    x_ = np.hstack((x, x*x))
    model = LinearRegression().fit(x_, y)
    r_sq = model.score(x_, y)
    print(f"residual square: {r_sq}, intercept: {model.intercept_}, slope: {model.coef_}")
    print(f"predict {x_} => {model.predict(x_)}")
    x2 = np.linspace(0, 100, 20).reshape(-1, 1)
    x2_ = np.hstack((x2, x2*x2))
    print(f"predict {x2_} => {model.predict(x2_)}")
