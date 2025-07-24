import pandas as pd
from sqlalchemy import create_engine
import time
import os

# Configuración de la conexión a la base de datos
DB_USER = "sgladmin"
DB_PASSWORD = "eHewYYk6nmwknnsn"
DB_HOST = "sgl.cfqgmxknp1yx.us-east-1.rds.amazonaws.com"
DB_PORT = 3306
DB_DATABASE = "informes"

# Crear el motor de conexión
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}")

# Leer el archivo Excel y obtener la columna GUIA
def leer_excel_y_columnas(ruta_excel, columna):
    if not os.path.exists(ruta_excel):
        raise FileNotFoundError(f"El archivo {ruta_excel} no existe.")
    
    df = pd.read_excel(ruta_excel)
    
    if columna not in df.columns:
        raise ValueError(f"La columna '{columna}' no existe en el archivo Excel.")
    
    return df[columna].dropna().unique()  # Elimina duplicados y valores nulos

# Consultar la base de datos para múltiples guías
def consultar_base_datos_multiple(solicitud, consulta):
    solicitud_str = "', '".join(map(str, solicitud))  # Formatear las guías en una lista separada por comas
    consulta_formateada = consulta.format(solicitud=solicitud_str)
    with engine.connect() as connection:
        return pd.read_sql_query(consulta_formateada, connection)

# Guardar datos en pestañas del Excel
def guardar_en_excel(df, ruta_excel, sheet_name):
    mode = "a" if os.path.exists(ruta_excel) else "w"
    with pd.ExcelWriter(ruta_excel, engine="openpyxl", mode=mode) as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

# Dividir lista en lotes
def dividir_en_lotes(lista, tamanio_lote):
    for i in range(0, len(lista), tamanio_lote):
        yield lista[i:i + tamanio_lote]

# Programa principal
def main():
    ruta_excel = "CC_Complementar2.xlsx"  # Cambia a la ruta de tu archivo
    columna = "CUSTOMERORDERNBR"    # Cambia al nombre de tu columna
    sheet_output = "Query1_Results"      # Nombre de la pestaña en el Excel
    batch_size = 100  # Tamaño del lote ajustable

    print("Leyendo archivo Excel...")
    solicitud = leer_excel_y_columnas(ruta_excel, columna)

    # Consulta SQL
    consulta1 = "SELECT * FROM informes.kpi_cc_cumplimiento_historicos WHERE sc IN ('{solicitud}')"

    # Resultados combinados
    resultados_query1 = []

    print("Iniciando proceso de extracción de datos...")
    start_time = time.time()
    
    for idx, lote in enumerate(dividir_en_lotes(solicitud, batch_size), 1):
        print(f"Procesando lote {idx} ({len(lote)} guías)...")
        df1 = consultar_base_datos_multiple(lote, consulta1)

        if not df1.empty:
            resultados_query1.append(df1)

    # Combinar resultados
    if resultados_query1:
        df_combined = pd.concat(resultados_query1, ignore_index=True)
        print(f"Guardando resultados en '{sheet_output}'...")
        guardar_en_excel(df_combined, ruta_excel, sheet_output)
        print("Datos guardados correctamente.")
    else:
        print("No se encontraron datos para las guías proporcionadas.")

    print(f"Proceso completado en {time.time() - start_time:.2f} segundos.")

if __name__ == "__main__":
    main()
