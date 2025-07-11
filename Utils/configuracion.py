# Utils/configuracion.py

import yaml
from pathlib import Path

with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# Exponer configuración como constantes o variables reutilizables
BASE_DATA_PATH = Path(config['base_data_path'])
SIMULACIONES_PATH = Path(config['simulaciones_path'])
LOG_PATH = Path(config['log_path'])
INTERVALO_EVENTOS = config['intervalo_eventos']
FAKER_LOCALE = config['faker_locale']
MAX_PRODUCTOS = config['max_productos']
MIN_PRODUCTOS = config['min_productos']
DIAS_RANGO_FECHA = config['dias_rango_fecha']
LAT_RANGE = tuple(config['lat_range'])
LON_RANGE = tuple(config['lon_range'])
