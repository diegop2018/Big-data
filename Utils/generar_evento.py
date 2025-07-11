# Utils/generar_evento.py

import random
import uuid
from datetime import datetime
from faker import Faker

from Utils.configuracion import (
    MAX_PRODUCTOS, MIN_PRODUCTOS, DIAS_RANGO_FECHA,
    LAT_RANGE, LON_RANGE, FAKER_LOCALE
)

fake = Faker(FAKER_LOCALE)

def generar_evento(customers, employees):
    fecha_evento = fake.date_time_between(
        start_date=f"-{DIAS_RANGO_FECHA}d", end_date="now"
    )
    timestamp_now = datetime.now()

    return {
        "order_id": str(uuid.uuid4()),
        "fecha_orden": fecha_evento.strftime("%d/%m/%Y %H:%M:%S"),
        "customer_id": int(random.choice(customers)),
        "employee_id": int(random.choice(employees)),
        "quantity_products": random.randint(MIN_PRODUCTOS, MAX_PRODUCTOS),
        "ubicacion": {
            "latitude": round(random.uniform(*LAT_RANGE), 6),
            "longitude": round(random.uniform(*LON_RANGE), 6),
            "ciudad": "Medellín",
            "departamento": "Antioquia"
        },
        "metadata": {
            "timestamp_generacion": timestamp_now.isoformat(),
            "version_simulacion": "3.0",
            "fuente_datos": "Faker + Simulación Optimizada"
        }
    }


# Permite usar el módulo desde línea de comandos para pruebas rápidas
