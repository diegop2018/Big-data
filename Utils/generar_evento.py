# Utils/generar_evento.py

import random
import uuid
from datetime import datetime
from faker import Faker
from pathlib import Path

import pandas as pd
import geopandas as gpd
from shapely import wkb
from shapely.geometry import Point

from Utils.configuracion import (
    MAX_PRODUCTOS, MIN_PRODUCTOS, DIAS_RANGO_FECHA,
    FAKER_LOCALE
)

# Inicializar faker
fake = Faker(FAKER_LOCALE)

# === Cargar distritos desde archivo .parquet ===
Base_data = "Base_data"  # Reemplaza esto con la ruta correcta
base_data = Path(Base_data)
df_barrios = pd.read_parquet(base_data / "medellin_neighborhoods.parquet")

# Asegurar que la columna geometry esté correctamente convertida a objetos shapely
if not isinstance(df_barrios["geometry"].iloc[0], Point):
    df_barrios["geometry"] = df_barrios["geometry"].apply(wkb.loads)

gdf_barrios = gpd.GeoDataFrame(df_barrios, geometry="geometry")

# === Función para generar punto aleatorio dentro de un polígono ===
def generar_punto_dentro(poligono):
    minx, miny, maxx, maxy = poligono.bounds
    for _ in range(100):  # Intentar hasta 100 veces
        punto = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if poligono.contains(punto):
            return punto
    raise ValueError("No se pudo generar un punto dentro del polígono.")

# === Función principal ===
def generar_evento(customers, employees):
    fecha_evento = fake.date_time_between(
        start_date=f"-{DIAS_RANGO_FECHA}d", end_date="now"
    )
    timestamp_now = datetime.now()

    # Elegir aleatoriamente un barrio/distrito
    barrio = gdf_barrios.sample(1).iloc[0]
    nombre_barrio = barrio["NOMBRE"]
    poligono = barrio.geometry

    # Generar ubicación realista dentro del polígono
    punto = generar_punto_dentro(poligono)

    return {
        "order_id": str(uuid.uuid4()),
        "fecha_orden": fecha_evento.strftime("%d/%m/%Y %H:%M:%S"),
        "customer_id": int(random.choice(customers)),
        "employee_id": int(random.choice(employees)),
        "quantity_products": random.randint(MIN_PRODUCTOS, MAX_PRODUCTOS),
        "ubicacion": {
            "latitude": round(punto.y, 6),  # y = latitud
            "longitude": round(punto.x, 6),  # x = longitud
            "ciudad": "Medellín",
            "departamento": "Antioquia",
            "barrio": nombre_barrio
        },
        "metadata": {
            "timestamp_generacion": timestamp_now.isoformat(),
            "version_simulacion": "3.1",
            "fuente_datos": "Faker + Simulación Geoespacial"
        }
    }
