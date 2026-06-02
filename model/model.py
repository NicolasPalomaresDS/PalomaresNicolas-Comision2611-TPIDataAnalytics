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
    """Representa un modelo de clasificación de ventas basado en XGBoost.
    Proporciona métodos para entrenamiento, predicción, evaluación y visualización.

    El modelo realiza una búsqueda de hiperparámetros durante el ajuste y guarda
    la mejor configuración junto con métricas de rendimiento para su inspección posterior.

    Atributos:
        model: Instancia subyacente de XGBClassifier ajustada.
        best_params: Mejores hiperparámetros encontrados durante la búsqueda.
        f1: Puntaje F1 ponderado obtenido en el conjunto de evaluación.
        report: Informe de clasificación del conjunto de evaluación.
        le: Codificador de etiquetas asociado a la variable objetivo, si aplica.
    """

    def __init__(self):
        """Inicializa una nueva instancia del modelo de ventas.
        Configura el modelo base y los contenedores para resultados y codificación de etiquetas.

        Atributos inicializados:
            model: Modelo XGBClassifier con una semilla fija para reproducibilidad.
            best_params: Diccionario para almacenar los mejores hiperparámetros encontrados.
            f1: Puntaje F1 ponderado calculado tras el ajuste del modelo.
            report: Informe de clasificación generado después de la evaluación.
            le: Codificador de etiquetas asociado a la variable objetivo, si se utiliza.
        """

        self.model = XGBClassifier(random_state=42)
        self.best_params = None
        self.f1 = None
        self.report = None
        self.le = None

    def fit(self, X_train, X_test, y_train, y_test, le=None):
        """Entrena el modelo de ventas usando datos de entrenamiento y evaluación.
        Devuelve la instancia actualizada del modelo con métricas calculadas.

        Args:
            X_train: Características del conjunto de entrenamiento.
            X_test: Características del conjunto de prueba o evaluación.
            y_train: Etiquetas verdaderas del conjunto de entrenamiento.
            y_test: Etiquetas verdaderas del conjunto de prueba o evaluación.
            le: Codificador de etiquetas opcional utilizado para mapear las clases.

        Returns:
            La instancia del modelo con el mejor estimador ajustado, parámetros óptimos
            y métricas de rendimiento actualizadas.
        """

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
        """Genera predicciones de ventas para nuevas observaciones.
        Utiliza el modelo previamente entrenado para estimar la clase de cada muestra.

        Args:
            X: Matriz de características de las observaciones a predecir.

        Returns:
            Arreglo con las etiquetas predichas para cada observación.
        """

        return self.model.predict(X)

    def metrics(self):
        """Devuelve un resumen de las métricas principales del modelo.
        Permite acceder de forma sencilla al rendimiento y configuración óptima obtenida.

        Returns:
            Diccionario con el puntaje F1 ponderado y los mejores hiperparámetros encontrados.
        """

        return {"f1-score": self.f1, "best_params": self.best_params}

    def summary(self):
        """Muestra un resumen textual del rendimiento del modelo.
        Imprime el informe de clasificación almacenado tras la evaluación.

        Returns:
            None. El informe se envía directamente a la salida estándar.
        """

        print(self.report)

    def plot_confusion_matrix(self, X, y):
        """Genera y muestra la matriz de confusión del modelo.
        Permite visualizar el desempeño de las predicciones frente a las clases reales.

        Args:
            X: Características del conjunto de datos a evaluar.
            y: Etiquetas verdaderas correspondientes a las observaciones de X.

        Returns:
            None. La matriz de confusión se muestra en una ventana gráfica.
        """

        y_pred = self.model.predict(X)
        cm = confusion_matrix(y, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot(cmap="Blues")
        plt.title("Matriz de Confusión", loc="left")
        plt.show()