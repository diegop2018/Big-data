import pandas as pd
from pathlib import Path

Base_data = "Base_data"  # Reemplaza esto con la ruta correcta
base_data = Path(Base_data)
df = pd.read_parquet(base_data / "medellin_neighborhoods.parquet")
print(df.head(10))