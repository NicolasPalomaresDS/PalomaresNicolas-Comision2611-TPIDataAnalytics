import pandas as pd
from pathlib import Path
import plotly.express as px
import ipywidgets as widgets
from IPython.display import display

DATA_PATH = Path("../data/clean/clientes.parquet")

class ClientesDashboardBuilder:
    """Construye y gestiona un panel interactivo de análisis de clientes.

    La clase carga datos limpios de clientes e ingresos y expone métodos para filtrar,
    graficar y mostrar los elementos del panel en un entorno de notebook.
    """

    def __init__(self):
        """Inicializa el estado del panel y los controles de filtrado.

        El constructor carga el conjunto de datos de clientes ya procesado y prepara
        los widgets de salida y el filtro de ciudad usados en las visualizaciones.
        """

        self.df = pd.read_parquet(DATA_PATH)

        self.output_edad_clientes = widgets.Output(
            layout=widgets.Layout(
                width="50%",
                border="1px solid #e0e0e0",
                border_radius="8px",
                padding="10px",
                margin="8px"
            )
        )

        self.output_distribucion_ingresos = widgets.Output(
            layout=widgets.Layout(
                width="50%",
                border="1px solid #e0e0e0",
                border_radius="8px",
                padding="10px",
                margin="8px"
            )
        )

        self.output_ingresos_clientes = widgets.Output(
            layout=widgets.Layout(
                width="50%",
                border="1px solid #e0e0e0",
                border_radius="8px",
                padding="10px",
                margin="8px"
            )
        )

        self.output_edad_ingresos = widgets.Output(
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
                self.df["ciudad"]
                .unique()
                .tolist()
            ),
            value="Todas",
            description="Ciudad:",
            style={"description_width": "initial"}
        )

    def _get_filtered_df(self):
        """Filtra el conjunto de datos del panel según la ciudad seleccionada.

        El método devuelve el conjunto de datos completo o solo las filas que
        coinciden con la ciudad actualmente seleccionada en el desplegable.

        Returns:
            pandas.DataFrame: Registros de clientes filtrados de acuerdo
            con la ciudad activa.
        """

        if self.filter.value == "Todas":
            return self.df
        return self.df[self.df["ciudad"] == self.filter.value]

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
            margin=dict(l=40, r=20, t=50, b=40),

            title=dict(
                font=dict(size=13, color="#333333", family="sans-serif"),
                x=0,
                xanchor="left"
            ),

            xaxis=dict(
                showgrid=True,
                gridcolor="#e0e0e0",
                gridwidth=0.5,
                griddash="dot",
                title=dict(font=dict(size=11, color="#333333", family="sans-serif")),
            ),

            yaxis=dict(
                showgrid=True,
                gridcolor="#e0e0e0",
                gridwidth=0.5,
                griddash="dot",
                title=dict(font=dict(size=11, color="#333333", family="sans-serif"))
            ),

        )

        return fig

    def _plot_distribucion_edades(self):
        """Genera un histograma con la distribución de edades de los clientes.

        El método construye un histograma de la columna de edad, ajusta el estilo
        del gráfico y lo muestra en el widget de salida correspondiente del panel.
        """

        df = self._get_filtered_df()

        fig = px.histogram(
            df,
            x="edad",
            title="<b>Distribución de edades</b>",
            labels={"edad": "Edad (Años)", "count": "Total"},
            nbins=20
        )

        fig.add_vline(
            x=df["edad"].mean(),
            line_dash="dash",
            line_color="red",
            opacity=0.5,
            annotation_text="Media",
            annotation_position="top"
        )

        fig.update_traces(
            marker=dict(
                color="#44A194",
                line=dict(color="#174f47", width=0.5)
            ),
            marker_color="#44A194",
            opacity=0.85
        )

        fig.update_layout(
            yaxis_title="Frecuencia",
            xaxis=dict(range=[df["edad"].min() - 2, df["edad"].max() + 2])
        )

        fig = self._apply_style(fig)

        self.output_edad_clientes.clear_output(wait=True)

        with self.output_edad_clientes:
            fig.show()

    def _plot_distribucion_ingresos(self):
        """Muestra un gráfico de barras horizontal con el ingreso promedio por ciudad.

        El método calcula el ingreso promedio por ciudad, ordena los resultados y
        los visualiza en un gráfico de barras estilizado.
        """

        df = self._get_filtered_df()

        fig = px.histogram(
            df,
            x="ingresos",
            title="<b>Distribución de ingresos</b>",
            labels={"ingresos": "Ingresos ($)"},
            nbins=20
        )

        fig.add_vline(
            x=df["ingresos"].mean(),
            line_dash="dash",
            line_color="red",
            opacity=0.5,
            annotation_text="Media",
            annotation_position="top"
        )

        fig.update_traces(
            marker=dict(
                color="#44A194",
                line=dict(color="#174f47", width=0.5)
            ),
            marker_color="#44A194",
            opacity=0.85
        )

        fig.update_layout(
            yaxis_title="Frecuencia",
            xaxis=dict(range=[df["ingresos"].min() - 3500, df["ingresos"].max() + 3500])
        )

        fig = self._apply_style(fig)

        self.output_distribucion_ingresos.clear_output(wait=True)

        with self.output_distribucion_ingresos:
            fig.show()

    def _plot_top_ingresos(self):
        """Crea un gráfico de barras horizontal con los 10 clientes de mayor ingreso.

        El método selecciona los 10 clientes con mayores ingresos, ordena los resultados,
        construye una visualización de barras estilizada y la muestra en el panel.
        """

        df = self._get_filtered_df()

        top_ingresos = df.nlargest(10, columns="ingresos")
        top_ingresos = top_ingresos.sort_values(ascending=True, by="ingresos")

        fig = px.bar(
            top_ingresos,
            x="ingresos",
            y="nombre",
            title="<b>Top 10 Clientes con Mayor Ingreso</b>",
            labels={"nombre": "", "ingresos": "Ingresos ($)"},
            orientation="h",
            range_x=[
                top_ingresos["ingresos"].min() * 0.95,
                top_ingresos["ingresos"].max() * 1.05
            ],
            text="ingresos"
        )

        fig.update_traces(
            marker=dict(
                color="#537D96",
                line=dict(color="#537D96", width=0.5)
            ),
            texttemplate="$%{text:,.0f}",
            textposition="outside"
        )

        fig = self._apply_style(fig)

        fig.update_layout(margin=dict(l=150, r=60, t=50, b=40))

        self.output_ingresos_clientes.clear_output(wait=True)

        with self.output_ingresos_clientes:
            fig.show()

    def _plot_edad_ingresos(self):
        """Construye un diagrama de dispersión de edad de clientes vs. ingresos.

        El método muestra la relación entre la edad de los clientes y sus ingresos,
        aplicando el estilo del panel y renderizando el resultado en el widget
        correspondiente.
        """

        df = self._get_filtered_df()

        fig = px.scatter(
            df,
            x="edad",
            y="ingresos",
            title="<b>Edad de Clientes vs. Ingresos</b>",
            labels={"edad": "Edad", "ingresos": "Ingresos ($)"},
            trendline="ols"
        )

        fig.update_traces(
            marker=dict(
                color="#EC8F8D",
                size=8,
                opacity=0.7,
                symbol="circle",
                line=dict(
                    color="#b55755",
                    width=1
                )
            ),
            selector=dict(mode="markers")
        )

        fig.update_traces(
            line=dict(dash="solid", color="#EC8F8D"),
            selector=dict(mode="lines")
        )

        fig = self._apply_style(fig)

        self.output_edad_ingresos.clear_output(wait=True)

        with self.output_edad_ingresos:
            fig.show()

    def _build_kpis(self):
        """Crea y devuelve una fila de tarjetas de indicadores clave de rendimiento (KPIs).

        El método resume los datos de clientes filtrados en widgets de KPI estilizados que
        resaltan totales, promedios y clientes/ciudades más relevantes en el panel.
        """

        df = self._get_filtered_df()

        total_clientes = len(df)
        edad_promedio = df["edad"].mean()
        ingreso_promedio = df["ingresos"].mean()
        cliente_con_mas_ingresos = df.loc[df['ingresos'].idxmax(), 'nombre']
        ciudad_con_mayor_ingreso = df.groupby("ciudad")["ingresos"].sum().idxmax()

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
                <div style="font-size: 12px; color: #666;">Total clientes</div>
                <div style="font-size: 22px; font-weight: bold; color: #333;">{total_clientes}</div>
            </div>
        """)

        kpi2 = widgets.HTML(f"""
            <div style="{kpi_style}">
                <div style="font-size: 12px; color: #666;">Edad promedio</div>
                <div style="font-size: 22px; font-weight: bold; color: #333;">{edad_promedio:.0f}</div>
            </div>
        """)

        kpi3 = widgets.HTML(f"""
            <div style="{kpi_style}">
                <div style="font-size: 12px; color: #666;">Ingreso promedio</div>
                <div style="font-size: 22px; font-weight: bold; color: #333;">${ingreso_promedio:,.0f}</div>
            </div>
        """)

        kpi4 = widgets.HTML(f"""
            <div style="{kpi_style}">
                <div style="font-size: 12px; color: #666;">Cliente con más ingresos</div>
                <div style="font-size: 22px; font-weight: bold; color: #333;">{cliente_con_mas_ingresos}</div>
            </div>
        """)

        kpi5 = widgets.HTML(f"""
            <div style="{kpi_style}">
                <div style="font-size: 12px; color: #666;">Ciudad con mayores ingresos</div>
                <div style="font-size: 16px; font-weight: bold; color: #333;">{ciudad_con_mayor_ingreso}</div>
            </div>
        """)

        return widgets.HBox([kpi1, kpi2, kpi3, kpi4, kpi5])

    def _update_all(self):
        """Actualiza todas las visualizaciones del panel según el estado actual del filtro.

        El método vuelve a ejecutar cada rutina de graficado para que los gráficos se mantengan
        sincronizados cuando cambian los datos base o la ciudad seleccionada por el usuario.
        """

        self._plot_distribucion_edades()
        self._plot_distribucion_ingresos()
        self._plot_edad_ingresos()
        self._plot_top_ingresos()

    def build_dashboard(self):
        """Ensamblar y mostrar el panel interactivo completo de clientes.

        El método conecta las interacciones del filtro por ciudad, organiza los widgets de KPIs
        y gráficos y realiza el renderizado inicial de todos los componentes del panel
        en el notebook.
        """

        def on_filter_change(change):
            if change["name"] == "value":
                self._update_all()

        self.filter.observe(on_filter_change)

        layout = widgets.VBox([

            self.filter,

            self._build_kpis(),

            widgets.HBox(
                [self.output_edad_clientes, self.output_distribucion_ingresos],
                layout=widgets.Layout(width="100%", gap="16px")
            ),

            widgets.HBox(
                [self.output_edad_ingresos, self.output_ingresos_clientes],
                layout=widgets.Layout(width="100%", gap="16px")
            ),

        ], layout=widgets.Layout(
            padding="16px",
            width="100%",
        ))

        display(layout)
        self._update_all()