import requests
import pandas as pd

# Precipitación
# Datos desde el 2004-01-01 a 2020-03-21
url_precipitación = "https://www.datos.gov.co/resource/s54a-sgyg.json?$where=departamento%20in%20('NARIÑO','CUNDINAMARCA')&$limit=500000"

# Datos desde el 2017-01-01 a 2020-03-23
# url_precipitación="https://www.datos.gov.co/resource/m84s-22dd.json?$where=departamento%20in%20('NARIÑO','CUNDINAMARCA')&$limit=500000"

response = requests.get(url_precipitación)
response.raise_for_status()

data = response.json()

df_precipitacion= pd.DataFrame(data)

df_precipitacion = df_precipitacion[[
    "departamento",
    "municipio",
    "fechaobservacion",
    "valorobservado"
]]

# Convertir fechaobservacion a datetime
df_precipitacion["fechaobservacion"] = pd.to_datetime(
    df_precipitacion["fechaobservacion"],
    errors="coerce"
)

# Renombrar columna 
df_precipitacion = df_precipitacion.rename(
    columns={"valorobservado": "precipitacion"}
)

# Crear la columna FECHA (año-mes-día)
df_precipitacion["fecha"] = df_precipitacion["fechaobservacion"].dt.date

# Asegurar que precipitación sea numérico
df_precipitacion["precipitacion"] = pd.to_numeric(
    df_precipitacion["precipitacion"], errors="coerce"
)

# Agrupar por departamento, municipio y fecha para calcular promedio precipitacion y precipitacion acumulada
df_precipitacion = (
    df_precipitacion
    .groupby(["departamento", "municipio", "fecha"], as_index=False)
    .agg(
        precipitacion_promedio=("precipitacion", "mean"),
        precipitacion_acumulada=("precipitacion", "sum")
    )
)

fecha_min = df_precipitacion["fecha"].min()
fecha_max = df_precipitacion["fecha"].max()

print(df_precipitacion.head())
print(df_precipitacion.shape)

print("Fecha mínima:", fecha_min)
print("Fecha máxima:", fecha_max)
print(df_precipitacion.describe())

