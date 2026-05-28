import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import RandomizedSearchCV

from sklearn.metrics import (
    f1_score,
    classification_report,
    ConfusionMatrixDisplay,
    confusion_matrix
)

class SalesModel:
    """Model utilities for sales analysis.

    This module defines functions and classes that support training, evaluating,
    and using models to analyze sales data.
    """

    def __init__(self):
        self.model = XGBClassifier(random_state=42)
        self.best_params = None
        self.f1 = None
        self.report = None
        self.le = None

    def fit(self, X_train, X_test, y_train, y_test, le=None):
        param_grid = {
            "n_estimators": [100, 500, 1000],
            "learning_rate": [0.01, 0.1, 0.2],
            "max_depth": [2, 3, 4, 5],
            "subsample": [0.7, 0.8, 1.0],
            "colsample_bytree": [0.7, 0.8, 1.0]
        }

        search = RandomizedSearchCV(
            XGBClassifier(random_state=42),
            param_grid,
            n_iter=20,
            cv=5,
            scoring="f1_weighted",
            random_state=42
        )

        search.fit(X_train, y_train)
        self.model = search.best_estimator_
        self.best_params = search.best_params_

        y_pred = self.model.predict(X_test)
        self.f1 = f1_score(y_test, y_pred, average="weighted")
        self.report = classification_report(
            y_test, y_pred,
            target_names=le.classes_ if le is not None else None
        )
        return self

    def predict(self, X):
        return self.model.predict(X)

    def metrics(self):
        return {"f1-score": self.f1, "best_params": self.best_params}

    def summary(self):
        print(self.report)

    def plot_confusion_matrix(self, X, y):
        y_pred = self.model.predict(X)
        cm = confusion_matrix(y, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot(cmap="Blues")
        plt.title("Matriz de Confusión", loc="left")
        plt.show()