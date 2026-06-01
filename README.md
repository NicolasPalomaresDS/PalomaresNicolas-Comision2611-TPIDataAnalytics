# Palomares Nicolas (Comisión 26110) TPI Data Analytics

Este repositorio contiene el Trabajo Práctico Integrador de la materia Data Analytics (Comisión 2611). El proyecto abarca el ciclo completo de análisis de datos sobre un dataset de ventas: desde la recopilación y limpieza, pasando por el análisis exploratorio y estadístico, hasta la visualización con Matplotlib, Seaborn y dashboards interactivos con Plotly. Desarrollado en VSCode; los notebooks principales están disponibles para visualizar y ejecutar directamente en Google Colab mediante los enlaces siguientes:

### [1. Notebook Limpieza](https://colab.research.google.com/github/NicolasPalomaresDS/PalomaresNicolas-Comision2611-TPIDataAnalytics/blob/main/notebooks/limpieza.ipynb)
### [2. Notebook Análisis Exploratorio + FE](https://colab.research.google.com/github/NicolasPalomaresDS/PalomaresNicolas-Comision2611-TPIDataAnalytics/blob/main/notebooks/analisis.ipynb)
### [3. Notebook Dashboards (poner Colab en modo claro o "light")](https://colab.research.google.com/drive/1uXq0WZ5mHBYsBHBzej6pMA21Z00lqlFD?usp=sharing)
### [4. Notebook Modelo XGBoost](https://colab.research.google.com/github/NicolasPalomaresDS/PalomaresNicolas-Comision2611-TPIDataAnalytics/blob/main/notebooks/modelado.ipynb)

## Estructura del Directorio

```
.
├── data
│   ├── clean
│   │   ├── clientes.parquet
│   │   ├── marketing.parquet
│   │   ├── ventas_marketing.parquet
│   │   └── ventas.parquet
│   │
│   └── raw
│       ├── clientes.csv
│       ├── marketing.csv
│       └── ventas.csv
│
├── model
│   ├── __init__.py
│   └── model.py
│
├── notebooks
│   ├── analisis.ipynb
│   ├── dashboard.ipynb
│   ├── limpieza.ipynb
│   └── modelado.ipynb
│
├── README.md
│
└── utils
    ├── clientes_dashboard_builder.py
    ├── __init__.py
    ├── static_utils.py
    └── ventas_dashboard_builder.py
```