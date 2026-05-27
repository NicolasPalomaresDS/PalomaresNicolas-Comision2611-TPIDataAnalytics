import pandas as pd
from pathlib import Path
import plotly.express as px

DATA_PATH = Path("../data/clean/ventas_marketing.parquet")

class DashUtils:
    def __init__(self):
        self.df = pd.read_parquet(DATA_PATH)

    def plot_ventas_mensuales(self):
        ventas_mensuales = (
            self.df
            .groupby("mes_venta")["precio_total"]
            .sum()
            .reset_index()
        )
        ventas_mensuales.columns = ["mes", "total_ventas"]

        fig = px.line(
            ventas_mensuales,
            x="mes",
            y="total_ventas",
            title="Ventas por Mes - 2024",
            line_shape="spline",
            render_mode="svg"
        )
        fig.show()