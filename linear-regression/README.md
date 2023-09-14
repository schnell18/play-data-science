# Introduction

Explore linear regression in Python.

## virtual environment

    python3 -m venv ~/python-envs/linear-regression --upgrade-deps
    source ~/python-envs/linear-regression/bin/activate
    pip3 install numpy scikit-learn statsmodels

## Simple Linear Regression With scikit-learn

There are five basic steps when you’re implementing linear regression:

- Import the packages
- Prepare training data
- Create a regression model and fit it with existing data
- Check model fitting
- Apply the model for predictions

### example

    import numpy as np
    from sklearn.linear_model import LinearRegression

    x = np.array([5, 15, 25, 35, 45, 55]).reshape((-1, 1))
    y = np.array([5, 20, 14, 32, 22, 38])

    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    print(f"residual square: {r_sq}, intercept: {model.intercept_}, slope: {model.coef_}")
    print(f"predict {x} => {model.predict(x)}")
    x2 = np.linspace(0, 100, 20).reshare(-1, 1)
    print(f"predict {x2} => {model.predict(x2)}")

