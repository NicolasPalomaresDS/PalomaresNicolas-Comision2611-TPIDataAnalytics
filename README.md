# Palomares Nicolas (Comisión 26110) TPI Data Analytics

### [1. Notebook Limpieza](https://nbviewer.org/github/NicolasPalomaresDS/PalomaresNicolas-Comision2611-TPIDataAnalytics/blob/main/notebooks/limpieza.ipynb)
### [2. Notebook Análisis Exploratorio + FE](https://nbviewer.org/github/NicolasPalomaresDS/PalomaresNicolas-Comision2611-TPIDataAnalytics/blob/main/notebooks/analisis.ipynb)
### [3. Notebook Dashboards](https://nbviewer.org/github/NicolasPalomaresDS/PalomaresNicolas-Comision2611-TPIDataAnalytics/blob/main/notebooks/dashboard.ipynb)
### [4. Notebook Modelo XGBoost](https://nbviewer.org/github/NicolasPalomaresDS/PalomaresNicolas-Comision2611-TPIDataAnalytics/blob/main/notebooks/modelado.ipynb)

**(Poner Google Colab en modo claro (light) para que se visualicen correctamente los tableros)**

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