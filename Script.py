# Script.py

# 👉 Agrega esto al inicio del archivo
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

import time
from pathlib import Path
from faker import Faker

from Utils.Raw import cargar_datos_parquet
from Utils.guardar_evento import guardar_evento
from Utils.generar_evento import generar_evento
from Utils.configuracion import (
    BASE_DATA_PATH, SIMULACIONES_PATH, INTERVALO_EVENTOS, FAKER_LOCALE
)

DEBUG = True

# Carga de datos
print("🔄 Cargando datos optimizados...")
Customers_List = cargar_datos_parquet(BASE_DATA_PATH / "customers.parquet", "customer_id")
Employees_List = cargar_datos_parquet(BASE_DATA_PATH / "employees.parquet", "employee_id")

if not Customers_List or not Employees_List:
    print("❌ Error cargando datos. Verifica archivos y rutas.")
    exit(1)

if DEBUG:
    print(f"📊 Clientes: {len(Customers_List)} | Empleados: {len(Employees_List)}")
    print(f"👤 Ejemplo Cliente: {Customers_List[:3]}")
    print(f"👨‍💼 Ejemplo Empleado: {Employees_List[:3]}")
    print("-" * 60)

# Faker
fake = Faker(FAKER_LOCALE)

# Crear carpeta simulaciones
SIMULACIONES_PATH.mkdir(parents=True, exist_ok=True)

print("🚀 Simulación en tiempo real iniciada.")
print(f"📍 Ciudad: Medellín | 🗂 Directorio: {SIMULACIONES_PATH.resolve()}")
print(f"⏰ Intervalo: {INTERVALO_EVENTOS}s | 🛑 Ctrl+C para detener")
print("-" * 60)

contador, exitosos = 0, 0

try:
    while True:
        contador += 1
        evento = generar_evento(Customers_List, Employees_List)
        if guardar_evento(evento, SIMULACIONES_PATH):
            exitosos += 1
            if DEBUG:
                print(f"✅ Evento #{contador} guardado: {evento['order_id'][:8]}...")
        time.sleep(INTERVALO_EVENTOS)

except KeyboardInterrupt:
    print("\n🛑 Simulación detenida por el usuario.")
except Exception as e:
    print(f"💥 Error inesperado: {e}")
finally:
    print("-" * 60)
    print(f"📈 Eventos totales: {contador}")
    print(f"✅ Guardados: {exitosos}")
    print(f"❌ Fallidos: {contador - exitosos}")
    if contador:
        print(f"📊 Tasa de éxito: {(exitosos / contador) * 100:.1f}%")
