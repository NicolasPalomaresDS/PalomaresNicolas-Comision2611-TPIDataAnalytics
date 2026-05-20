import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
from numpy.typing import ArrayLike

class StaticUtils():
    """Utilidades estáticas para configurar aspectos globales de la aplicación.

    Esta clase agrupa funciones auxiliares que no dependen del estado de una instancia.
    """

    @staticmethod
    def set_plt_config() -> None:
        """Configura los parámetros globales de matplotlib para los gráficos.

        Establece valores coherentes de tipografía, estilos y colores
        para un formato visual unificado.

        Args:
            None

        Returns:
            None
        """

        # Fuente
        plt.rcParams["font.family"] = "sans-serif"
        plt.rcParams["font.size"] = 11

        # Título
        plt.rcParams["axes.titlesize"] = plt.rcParams["axes.labelsize"]
        plt.rcParams["axes.titleweight"] = "bold"
        plt.rcParams["axes.titlepad"] = 10

        # Etiquetas de ejes
        plt.rcParams["axes.labelpad"] = 10
        plt.rcParams["axes.labelweight"] = "bold"

        # Marcos
        plt.rcParams["axes.spines.top"] = False
        plt.rcParams["axes.spines.right"] = False

        # Grilla
        plt.rcParams["axes.grid"] = True
        plt.rcParams["grid.linestyle"] = "--"
        plt.rcParams["grid.alpha"] = 0.3

        # Colores
        plt.rcParams["axes.prop_cycle"] = plt.cycler(color=[
            "#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2"
        ])

    @staticmethod
    def smooth_line(x: ArrayLike, y: ArrayLike) -> tuple:
        """Suaviza una serie de puntos para generar una línea continua.

        Crea una interpolación suave a partir de datos discretos para
        mejorar la presentación gráfica.

        Args:
            x: Valores de eje x de los puntos originales.
            y: Valores de eje y de los puntos originales.

        Returns:
            Una tupla `(x_smooth, y_smooth)` con los valores suavizados de x e y.
        """

        x_smooth = np.linspace(x.min(), x.max(), 300)
        y_smooth = make_interp_spline(x, y)(x_smooth)

        return x_smooth, y_smooth