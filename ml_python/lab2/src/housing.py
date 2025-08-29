# Creating housing.py file to use
with open("ml_python/lab2/src/housing.py","w") as f:
    f.write('''import random
from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_california_housing
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pandas as pd
import numpy as np

BASE_PIPELINE = [
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
]

MODELS = {
    "simple_elastic": {
        "pipeline": Pipeline(BASE_PIPELINE + [("model", ElasticNet(max_iter=1000))]),
        "param_grid": {
            "model__alpha": [0.001,0.01,0.1,0.3,0.5,0.7,1.0,10.0],
            "model__l1_ratio": [0.0,0.5,1.0],
        },
    },
    "poly_elastic": {
        "pipeline": Pipeline(BASE_PIPELINE + [
            ("poly", PolynomialFeatures(degree=2, include_bias=False)),
            ("model", ElasticNet(max_iter=1000)),
        ]),
        "param_grid": {
            "model__alpha": [0.001,0.01,0.1,0.3,0.5,0.7,1.0,10.0],
            "model__l1_ratio": [0.0,0.5,1.0],
        },
    },
    "knn": {
        "pipeline": Pipeline(BASE_PIPELINE + [("model", KNeighborsRegressor())]),
        "param_grid": {
            "model__n_neighbors": [2,5,10,20,50],
            "model__p": [1,2],
        },
    },
}

def set_seed(seed:int=1):
    np.random.seed(seed)
    random.seed(seed)

def load_dataset(test_size:float=0.2, random_state:int=1):
    ds = fetch_california_housing(as_frame=True)
    df = ds.frame.copy()
    X = df.drop(columns=["MedHouseVal"])
    y = df["MedHouseVal"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

def train(model:str, X_train:pd.DataFrame, y_train:pd.DataFrame, cv_splits:int=5, random_state:int=1):
    pipeline = MODELS[model]["pipeline"]
    param_grid = MODELS[model]["param_grid"]
    cv = KFold(n_splits=cv_splits, shuffle=True, random_state=random_state)
    gs = GridSearchCV(pipeline, param_grid, cv=cv, scoring="neg_mean_squared_error", n_jobs=-1, refit=True)
    gs.fit(X_train, y_train)
    return gs

def eval(gs:GridSearchCV, X_test:pd.DataFrame, y_test:pd.DataFrame):
    best = gs.best_estimator_
    y_pred = best.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return {"estimator": best["model"], "preds": y_pred, "rmse": rmse, "mae": mae, "r2": r2}
''')
print("housing.py created!")
