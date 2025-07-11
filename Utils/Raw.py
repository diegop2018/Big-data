#Leer archivo parquet
import pandas as pd
import os
from pathlib import Path
import logging
from typing import Union, List, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_parquet(archivo: Union[str, Path], **kwargs) -> Optional[pd.DataFrame]:
    """
    Función optimizada para leer archivos Parquet con manejo de errores
    
    Args:
        archivo: Ruta del archivo Parquet
        **kwargs: Argumentos adicionales para pd.read_parquet()
    
    Returns:
        DataFrame de pandas o None si hay error
    """
    try:
        # Convertir a Path si es string
        archivo_path = Path(archivo) if isinstance(archivo, str) else archivo
        
        # Verificar que el archivo existe
        if not archivo_path.exists():
            logger.error(f"❌ El archivo no existe: {archivo_path}")
            return None
        
        # Verificar que es un archivo Parquet
        if archivo_path.suffix.lower() != '.parquet':
            logger.warning(f"⚠️ El archivo no tiene extensión .parquet: {archivo_path}")
        
        # Leer el archivo
        logger.info(f"📖 Leyendo archivo: {archivo_path}")
        df = pd.read_parquet(archivo_path, **kwargs)
        
        logger.info(f"✅ Archivo leído exitosamente: {df.shape[0]} filas x {df.shape[1]} columnas")
        return df
        
    except FileNotFoundError:
        logger.error(f"❌ Archivo no encontrado: {archivo}")
        return None
    except Exception as e:
        logger.error(f"❌ Error leyendo archivo {archivo}: {str(e)}")
        return None

def convertir_columna_a_lista(df: pd.DataFrame, columna: str) -> Optional[List]:
    """
    Función optimizada para convertir una columna de DataFrame a lista
    
    Args:
        df: DataFrame de pandas
        columna: Nombre de la columna a convertir
    
    Returns:
        Lista con los valores de la columna o None si hay error
    """
    try:
        # Verificar que el DataFrame no esté vacío
        if df.empty:
            logger.warning("⚠️ DataFrame vacío")
            return []
        
        # Verificar que la columna existe
        if columna not in df.columns:
            logger.error(f"❌ Columna '{columna}' no encontrada. Columnas disponibles: {list(df.columns)}")
            return None
        
        # Convertir a lista
        lista_valores = df[columna].tolist()
        
        logger.info(f"✅ Columna '{columna}' convertida a lista: {len(lista_valores)} elementos")
        return lista_valores
        
    except Exception as e:
        logger.error(f"❌ Error convirtiendo columna '{columna}': {str(e)}")
        return None

def cargar_datos_parquet(archivo: Union[str, Path], columna_id: str = None) -> Union[pd.DataFrame, List, None]:
    """
    Función combinada que carga un archivo Parquet y opcionalmente convierte una columna a lista
    
    Args:
        archivo: Ruta del archivo Parquet
        columna_id: Nombre de la columna a convertir a lista (opcional)
    
    Returns:
        DataFrame si no se especifica columna_id, List si se especifica, None si hay error
    """
    # Cargar DataFrame
    df = read_parquet(archivo)
    if df is None:
        return None
    
    # Si se especifica una columna, convertirla a lista
    if columna_id:
        return convertir_columna_a_lista(df, columna_id)
    
    return df

def obtener_info_dataframe(df: pd.DataFrame) -> dict:
    """
    Obtener información detallada de un DataFrame
    
    Args:
        df: DataFrame de pandas
    
    Returns:
        Diccionario con información del DataFrame
    """
    try:
        info = {
            'filas': len(df),
            'columnas': len(df.columns),
            'nombres_columnas': list(df.columns),
            'tipos_datos': df.dtypes.to_dict(),
            'memoria_uso': df.memory_usage(deep=True).sum(),
            'valores_nulos': df.isnull().sum().to_dict()
        }
        
        logger.info(f"📊 Información del DataFrame: {info['filas']} filas x {info['columnas']} columnas")
        return info
        
    except Exception as e:
        logger.error(f"❌ Error obteniendo información del DataFrame: {str(e)}")
        return {}

# Mantener compatibilidad con código existente (funciones legacy)
def Read_parquet(archivo):
    """
    Función legacy para mantener compatibilidad
    """
    return read_parquet(archivo)

def convertir_columna_a_lista_legacy(df, columna):
    """
    Función legacy para mantener compatibilidad
    """
    return convertir_columna_a_lista(df, columna)







