#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from sklearn.linear_model import LinearRegression

if __name__ == "__main__":
    x = np.array([5, 15, 25, 35, 45, 55]).reshape((-1, 1))
    y = np.array([5, 20, 14, 32, 22, 38])

    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    print(f"residual square: {r_sq}, intercept: {model.intercept_}, slope: {model.coef_}")
    print(f"predict {x} => {model.predict(x)}")
    x2 = np.linspace(0, 100, 20).reshape(-1, 1)
    print(f"predict {x2} => {model.predict(x2)}")
