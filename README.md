# Palomares Nicolas (Comisión 26110) TPI Data Analytics

Este repositorio contiene el Trabajo Práctico Integrador del curso Data Analytics (Comisión 2611). El proyecto abarca el ciclo completo de análisis de datos sobre un dataset de ventas: desde la recopilación y limpieza, pasando por el análisis exploratorio y estadístico, hasta la visualización con Matplotlib, Seaborn y dashboards interactivos con Plotly. Desarrollado en VSCode; la notebook con los dashboards está disponible para visualizar directamente en Google Colab mediante el siguiente enlace:

### [Notebook Dashboards (poner Colab en modo claro)](https://colab.research.google.com/drive/1uXq0WZ5mHBYsBHBzej6pMA21Z00lqlFD?usp=sharing)

## Estructura del Directorio

Organización del repositorio actual, describiendo los archivos y carpetas principales del proyecto.

```
.
├── data
│   ├── clean                          # Datos procesados y listos para análisis
│   │   ├── clientes.parquet
│   │   ├── marketing.parquet
│   │   ├── ventas_marketing.parquet   # Dataset combinado de ventas y marketing
│   │   └── ventas.parquet
│   │
│   └── raw                            # Datos originales sin procesar
│       ├── clientes.csv
│       ├── marketing.csv
│       └── ventas.csv
│
├── model
│   ├── __init__.py
│   └── model.py                       # Definición de modelos de datos
│
├── utils
│   ├── __init__.py
│   ├── clientes_dashboard_builder.py  # Construcción del dashboard de clientes
│   ├── static_utils.py                # Funciones auxiliares compartidas
│   └── ventas_dashboard_builder.py    # Construcción del dashboard de ventas
│
├── notebooks
│   ├── analisis.ipynb                 # Análisis exploratorio y estadístico
│   ├── dashboard.ipynb                # Dashboard interactivo con Plotly
│   ├── limpieza.ipynb                 # Limpieza y transformación de datos
│   └── modelado.ipynb                 # Modelado y consolidación de datos
│
├── .gitignore                         # Archivo gitignore
└── README.md                          # Este archivo
```

## Desarrollo local

Para explorar o modificar manualmente el código:

**Requisitos:**

- Python v3.12.3 o superior

**Clonar el repositorio:**

```bash
git clone https://github.com/NicolasPalomaresDS/PalomaresNicolas-Comision2611-TPIDataAnalytics.git
```

**Entrar al directorio:**

```bash
cd PalomaresNicolas-Comision2611-TPIDataAnalytics
```

**Crear entorno virtual y activarlo:**

```bash
python -m venv venv
source venv/bin/activate
```

**Instalar librerías necesarias:**

```bash
pip install -r requirements.txt
```