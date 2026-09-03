# Pipeline de Datos Macroeconómicos EM

Un pipeline en Python que extrae, limpia y exporta datos macroeconómicos de seis economías de Centroamérica y el Caribe, listos para ser analizados en cualquier herramienta.

## Países Incluidos

- Panamá (economía ancla)
- Costa Rica
- República Dominicana
- Guatemala
- Uruguay
- El Salvador

Estas economías comparten características estructurales importantes: son pequeñas y abiertas, dependientes del comercio exterior, y sensibles a la política monetaria de los Estados Unidos — lo que las convierte en un grupo de pares significativo para el análisis comparativo.

## Fuentes de Datos

| Fuente | Indicadores |
|---|---|
| API REST del Banco Mundial | Crecimiento del PIB, inflación (IPC), deuda pública, cuenta corriente, IED, tasa de interés activa, tasa de desempleo |
| FRED (Reserva Federal de St. Louis) | Tasa de fondos federales de EE.UU., VIX, índice del dólar |

Los datos cubren el período 2000–2023. No se realizan descargas manuales — toda la información se obtiene de forma programática mediante llamadas a APIs.

## Archivos de Salida

El pipeline genera los siguientes archivos en la carpeta `data/`:

- `wb_data.csv` — indicadores del Banco Mundial por país y año
- `fred_data.csv` — indicadores globales de FRED por año
- `em_macro_dashboard.xlsx` — dataset combinado con dos hojas, listo para análisis

Estos archivos pueden ser consumidos por cualquier herramienta de análisis o visualización — Power BI, Tableau, Excel, o directamente en Python.

## Estructura del Proyecto

```
EM Macro/
│
├── main.py                  # Orquesta el pipeline completo
├── .env                     # Clave de API de FRED (no incluida en el repositorio)
├── data/                    # Archivos generados (no incluidos en el repositorio)
└── modules/
    ├── wb_fetcher.py        # Extrae indicadores del Banco Mundial vía API REST
    ├── fred_fetcher.py      # Extrae indicadores globales de FRED
    └── exporter.py          # Combina los datasets y exporta a Excel
```

## Configuración

**1. Clonar el repositorio**
```bash
git clone https://github.com/TonyJC99/em-macro-dashboard.git
cd em-macro-dashboard
```

**2. Instalar dependencias**
```bash
pip install requests pandas openpyxl fredapi python-dotenv
```

**3. Crear un archivo `.env` dentro de la carpeta `EM Macro`**
```
FRED_API_KEY=tu_clave_aqui
```

Puedes obtener una clave gratuita de FRED en [fred.stlouisfed.org](https://fred.stlouisfed.org/docs/api/api_key.html).

**4. Ejecutar el pipeline**
```bash
python main.py
```

## Decisiones de Diseño

- Todos los indicadores expresados en porcentaje se almacenan como decimales (8% → 0.08) para que las herramientas de análisis puedan aplicar el formato correcto sin manipulación adicional
- El VIX y el índice del dólar se mantienen como valores de índice sin modificar — no son porcentajes
- Las rutas de archivo se anclan con `Path(__file__).resolve()` para que el pipeline funcione correctamente sin importar el directorio de trabajo
- Toda la limpieza y normalización de datos ocurre en Python, no en la herramienta de análisis

## Tecnologías Utilizadas

- Python 3.12
- pandas, requests, fredapi, python-dotenv, openpyxl
