import pandas as pd
from pathlib import Path
import plotly.express as px
import ipywidgets as widgets
from IPython.display import display

DATA_PATH = Path("../data/clean/ventas_marketing.parquet")

class DashUtils:
    def __init__(self):
        self.df = pd.read_parquet(DATA_PATH)
        self.output_ventas_mensuales = widgets.Output()
        self.output_mejores_productos = widgets.Output()
        self.output_duracion_ratio = widgets.Output()

        self.filter = widgets.Dropdown(
            options=["Todas"] + sorted(
                self.df["categoria"]
                .unique()
                .tolist()
            ),
            value="Todas",
            description="Categoría:",
            style={"description_width": "initial"}
        )

    def _get_filtered_df(self):
        if self.filter.value == "Todas":
            return self.df
        return self.df[self.df["categoria"] == self.filter.value]

    def _plot_ventas_mensuales(self):
        df = self._get_filtered_df()
        ventas_mensuales = (
            df
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
            render_mode="svg",
            markers=True
        )

        fig.update_traces(
            line=dict(color="#4C72B0", width=2),
            mode="lines+markers",
            marker=dict(size=6, color="#4C72B0")
        )

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="sans-serif", size=12),
            title_font=dict(size=13, color="#333333"),
            xaxis=dict(showgrid=True, gridcolor="#e0e0e0", gridwidth=0.5),
            yaxis=dict(showgrid=True, gridcolor="#e0e0e0", gridwidth=0.5),
            margin=dict(l=40, r=20, t=50, b=40)
        )
        self.output_ventas_mensuales.clear_output(wait=True)
        with self.output_ventas_mensuales:
            fig.show()

    def _plot_mejores_productos(self):
        df = self._get_filtered_df()
        mejores_productos = (
            df
            .groupby("producto")["precio_total"]
            .sum()
            .pipe(lambda s: s[s > s.mean()])
            .sort_values(ascending=True)
            .reset_index()
        )

        fig = px.bar(
            mejores_productos,
            x="precio_total",
            y="producto",
            title="Mejores Productos por Rendimiento",
            orientation="h"
        )
        self.output_mejores_productos.clear_output(wait=True)
        with self.output_mejores_productos:
            fig.show()

    def _plot_duracion_ratio(self):
        df = self._get_filtered_df()

        fig = px.scatter(
            df,
            x="duracion_campanha",
            y="ratio_ventas_costo",
            title="Duración de campañas (en días) vs. Ratio de ventas/costo"
        )
        self.output_duracion_ratio.clear_output(wait=True)
        with self.output_duracion_ratio:
            fig.show()

    def _update_all(self):
        self._plot_ventas_mensuales()
        self._plot_mejores_productos()
        self._plot_duracion_ratio()

    def build_dashboard(self):
        def on_filter_change(change):
            if change["name"] == "value":
                self._update_all()

        self.filter.observe(on_filter_change)

        layout = widgets.VBox([
            self.filter,
            self.output_ventas_mensuales,
            widgets.HBox([
                self.output_mejores_productos,
                self.output_duracion_ratio
            ])
        ])

        display(layout)
        self._update_all()