import pandas as pd
from pathlib import Path
import plotly.express as px
import ipywidgets as widgets
from IPython.display import display

DATA_PATH = Path("../data/clean/ventas_marketing.parquet")

class DashboardBuilder:
    """Construye y gestiona un panel interactivo de análisis de ventas.

    La clase carga datos limpios de ventas y marketing y expone métodos para filtrar,
    graficar y mostrar los elementos del panel en un entorno de notebook.
    """

    def __init__(self):
        """Inicializa el estado del panel y los controles de filtrado.

        El constructor carga el conjunto de datos de ventas ya procesado y prepara
        los widgets de salida y el filtro de categoría usados en las visualizaciones.
        """

        self.df = pd.read_parquet(DATA_PATH)

        self.output_ventas_mensuales = widgets.Output(
            layout=widgets.Layout(
                width="50%",
                border="1px solid #e0e0e0",
                border_radius="8px",
                padding="10px",
                margin="8px"
            )
        )

        self.output_costo_por_canal = widgets.Output(
            layout=widgets.Layout(
                width="50%",
                border="1px solid #e0e0e0",
                border_radius="8px",
                padding="10px",
                margin="8px"
            )
        )

        self.output_mejores_productos = widgets.Output(
            layout=widgets.Layout(
                width="50%",
                border="1px solid #e0e0e0",
                border_radius="8px",
                padding="10px",
                margin="8px"
            )
        )

        self.output_duracion_ratio = widgets.Output(
            layout=widgets.Layout(
                width="50%",
                border="1px solid #e0e0e0",
                border_radius="8px",
                padding="10px",
                margin="8px"
            )
        )

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
        """Filtra el conjunto de datos del panel según la categoría seleccionada.

        El método devuelve el conjunto de datos completo o solo las filas que
        coinciden con la categoría actualmente seleccionada en el desplegable.

        Returns:
            pandas.DataFrame: Registros de ventas y marketing filtrados de acuerdo
            con la categoría activa.
        """

        if self.filter.value == "Todas":
            return self.df
        return self.df[self.df["categoria"] == self.filter.value]

    def _apply_style(self, fig):
        """Aplica un estilo visual consistente a una figura de Plotly.

        El método actualiza las propiedades de diseño para alinear los gráficos con
        el tema visual del panel y mejorar su legibilidad.

        Args:
            fig: Figura de Plotly a la que se le aplicará el estilo.

        Returns:
            La misma instancia de figura de Plotly con la configuración de diseño actualizada.
        """

        fig.update_layout(

            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="sans-serif", size=12),

            title=dict(
                font=dict(size=13, color="#333333", family="sans-serif"),
                x=0,
                xanchor="left"
            ),

            xaxis=dict(
                showgrid=True, gridcolor="#e0e0e0", gridwidth=0.5,
                title=dict(font=dict(size=11, color="#333333", family="sans-serif"))
            ),

            yaxis=dict(
                showgrid=True, gridcolor="#e0e0e0", gridwidth=0.5,
                title=dict(font=dict(size=11, color="#333333", family="sans-serif"))
            ),

            margin=dict(l=40, r=20, t=50, b=40)
        )

        return fig

    def _plot_ventas_mensuales(self):
        """Genera un gráfico de serie temporal de ventas mensuales para el panel.

        El método agrega las ventas totales por mes, crea un gráfico de líneas estilizado
        y lo muestra en el widget de salida correspondiente del panel.
        """

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
            title="<b>Ventas por Mes - 2024</b>",
            labels={"mes": "Mes", "total_ventas": "Total Ventas ($)"},
            line_shape="spline",
            render_mode="svg",
            markers=True
        )

        fig.update_traces(
            line=dict(color="#4C72B0", width=2),
            mode="lines+markers",
            marker=dict(size=6, color="#4C72B0"),
        )
        fig = self._apply_style(fig)

        self.output_ventas_mensuales.clear_output(wait=True)
        with self.output_ventas_mensuales:
            fig.show()

    def _plot_costo_por_canal(self):
        """Crea un gráfico de barras que compara el costo total de marketing por canal.

        El método agrega los costos únicos por producto en cada canal, construye una
        visualización de barras estilizada y la muestra en la sección de costo por canal.
        """

        df = self._get_filtered_df()

        costo_total_por_canal = (
            pd.Series({
                "Email": (
                    df
                    .drop_duplicates(subset=["producto"])["costo_email"]
                    .sum()
                ),
                "RRSS": (
                    df
                    .drop_duplicates(subset=["producto"])["costo_rrss"]
                    .sum()
                ),
                "TV": (
                    df
                    .drop_duplicates(subset=["producto"])["costo_tv"]
                    .sum()
                )
            })
            .reset_index()
        )
        costo_total_por_canal.columns = ["canal", "costo_total"]

        fig = px.bar(
            costo_total_por_canal,
            x="canal",
            y="costo_total",
            title="<b>Costo Total por Canal</b>",
            labels={"canal": "Canal", "costo_total": "Costo Total ($)"},
            range_y=[
                costo_total_por_canal["costo_total"].min() * 0.95,
                costo_total_por_canal["costo_total"].max() * 1.05
            ]
        )
        fig.update_traces(marker_color="#4C72B0")
        fig = self._apply_style(fig)

        self.output_costo_por_canal.clear_output(wait=True)
        with self.output_costo_por_canal:
            fig.show()

    def _plot_mejores_productos(self):
        """Construye un gráfico de barras horizontal que resalta los productos con mejor rendimiento.

        El método selecciona los productos con ventas totales por encima del promedio, crea una
        visualización de barras estilizada ordenada por rendimiento y la muestra en el panel.
        """

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
            title="<b>Mejores Productos por Rendimiento</b>",
            labels={"precio_total": "Ganancias Totales ($)", "producto": "Producto"},
            orientation="h",
            range_x=[
                mejores_productos["precio_total"].min() * 0.95,
                mejores_productos["precio_total"].max() * 1.05
            ]
        )
        fig.update_traces(marker_color="#4C72B0")
        fig = self._apply_style(fig)

        self.output_mejores_productos.clear_output(wait=True)
        with self.output_mejores_productos:
            fig.show()

    def _plot_duracion_ratio(self):
        """Muestra un diagrama de dispersión que relaciona la duración de la campaña con el ratio ventas/costo.

        El método visualiza cómo la duración de las campañas y el precio del producto interactúan con
        los indicadores de eficiencia entre categorías, ayudando a identificar rangos óptimos.
        """

        df = self._get_filtered_df()

        fig = px.scatter(
            df,
            x="duracion_campanha",
            y="ratio_ventas_costo",
            title="<b>Duración de campañas (en días) vs. Ratio de ventas/costo</b>",
            labels={
                "duracion_campanha": "Duración de Campañas en Días",
                "ratio_ventas_costo": "Ratio Ventas/Costo",
                "precio": "Precio",
                "categoria": "Categoría"
            },
            size="precio",
            color="categoria",
            color_discrete_sequence=["#1a3a5c", "#4C72B0", "#a8c4e0"]
        )
        fig = self._apply_style(fig)

        self.output_duracion_ratio.clear_output(wait=True)
        with self.output_duracion_ratio:
            fig.show()

    def _build_kpis(self):
        """Crea y devuelve una fila de tarjetas de indicadores clave de rendimiento (KPIs).

        El método resume los datos de ventas filtrados en widgets de KPI estilizados que
        resaltan totales, promedios y productos de mejor rendimiento en el panel.
        """

        df = self._get_filtered_df()

        total_ventas = df["precio_total"].sum()
        venta_promedio = df["precio_total"].mean()
        total_productos = df["producto"].nunique()
        total_transacciones = len(df)
        producto_mas_vendido = df.groupby("producto")["precio_total"].sum().idxmax()

        kpi_style = """
            background-color: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 16px;
            margin: 8px;
            text-align: center;
            width: 242px;
        """

        kpi1 = widgets.HTML(f"""
            <div style="{kpi_style}">
                <div style="font-size: 12px; color: #666;">Total Ventas</div>
                <div style="font-size: 22px; font-weight: bold; color: #333;">${total_ventas:,.0f}</div>
            </div>
        """)

        kpi2 = widgets.HTML(f"""
            <div style="{kpi_style}">
                <div style="font-size: 12px; color: #666;">Venta Promedio</div>
                <div style="font-size: 22px; font-weight: bold; color: #333;">${venta_promedio:,.0f}</div>
            </div>
        """)

        kpi3 = widgets.HTML(f"""
            <div style="{kpi_style}">
                <div style="font-size: 12px; color: #666;">Productos</div>
                <div style="font-size: 22px; font-weight: bold; color: #333;">{total_productos}</div>
            </div>
        """)

        kpi4 = widgets.HTML(f"""
            <div style="{kpi_style}">
                <div style="font-size: 12px; color: #666;">Total Transacciones</div>
                <div style="font-size: 22px; font-weight: bold; color: #333;">{total_transacciones:,}</div>
            </div>
        """)

        kpi5 = widgets.HTML(f"""
            <div style="{kpi_style}">
                <div style="font-size: 12px; color: #666;">Producto más Vendido</div>
                <div style="font-size: 16px; font-weight: bold; color: #333;">{producto_mas_vendido}</div>
            </div>
        """)

        return widgets.HBox([kpi1, kpi2, kpi3, kpi4, kpi5])

    def _update_all(self):
        """Actualiza todas las visualizaciones del panel según el estado actual del filtro.

        El método vuelve a ejecutar cada rutina de graficado para que los gráficos se mantengan
        sincronizados cuando cambian los datos base o la categoría seleccionada por el usuario.
        """

        self._plot_ventas_mensuales()
        self._plot_costo_por_canal()
        self._plot_mejores_productos()
        self._plot_duracion_ratio()

    def build_dashboard(self):
        """Ensamblar y mostrar el panel interactivo completo de ventas.

        El método conecta las interacciones del filtro, organiza los widgets de KPIs y gráficos
        y realiza el renderizado inicial de todos los componentes del panel en el notebook.
        """

        def on_filter_change(change):
            if change["name"] == "value":
                self._update_all()

        self.filter.observe(on_filter_change)

        layout = widgets.VBox([

            self.filter,

            self._build_kpis(),

            widgets.HBox(
                [self.output_ventas_mensuales, self.output_costo_por_canal],
                layout=widgets.Layout(width="100%", gap="16px")
            ),

            widgets.HBox(
                [self.output_mejores_productos, self.output_duracion_ratio],
                layout=widgets.Layout(width="100%", gap="16px")
            ),

        ], layout=widgets.Layout(
            padding="16px",
            width="100%",
        ))

        display(layout)
        self._update_all()