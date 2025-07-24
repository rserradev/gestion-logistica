import pandas as pd
from sqlalchemy import create_engine
import time

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
    df = pd.read_excel(ruta_excel)
    return df[columna].dropna().unique()  # Elimina duplicados y valores nulos

# Consultar la base de datos para múltiples guías
def consultar_base_datos_multiple(guias, consulta):
    guias_str = "', '".join(map(str, guias))  # Formatear las guías en una lista separada por comas
    consulta_formateada = consulta.format(guias=guias_str)
    with engine.connect() as connection:
        df = pd.read_sql_query(consulta_formateada, connection)
    return df

# Guardar datos en pestañas del Excel
def guardar_en_excel(df1, df2, ruta_excel):
    with pd.ExcelWriter(ruta_excel, engine="openpyxl", mode="a") as writer:
        df1.to_excel(writer, sheet_name="Query1", index=False)
        df2.to_excel(writer, sheet_name="Query2", index=False)

# Función para dividir la lista en lotes
def dividir_en_lotes(lista, tamanio_lote):
    for i in range(0, len(lista), tamanio_lote):
        yield lista[i:i + tamanio_lote]

# Programa principal
def main():
    ruta_excel = "Copia de Detalle Spread.xlsx"  # Cambia a la ruta de tu archivo
    columna_guia = "GUIAS"

    guias = leer_excel_y_columnas(ruta_excel, columna_guia)

    # Escribe tus consultas SQL
    consulta1 = "SELECT * FROM informes.kpi_dad_historicos WHERE nguia IN ('{guias}')"
    consulta2 = "SELECT * FROM informes.kpi_seguimientos WHERE nguia IN ('{guias}')"

    # Recolectar resultados
    resultados_query1 = []
    resultados_query2 = []

    # Dividir las guías en lotes de 50 para procesarlas
    lotes = dividir_en_lotes(guias, 50)

    start_time = time.time()  # Iniciar medición de tiempo

    for idx, lote in enumerate(lotes, 1):
        print(f"Procesando lote {idx} de {len(guias)//50 + 1} (Guías {((idx-1)*50 + 1)} - {min(idx*50, len(guias))})")

        # Consultar base de datos para el lote de guías
        df1 = consultar_base_datos_multiple(lote, consulta1)
        df2 = consultar_base_datos_multiple(lote, consulta2)

        # Verificar que los resultados no estén vacíos
        if not df1.empty:
            resultados_query1.append(df1)
        if not df2.empty:
            resultados_query2.append(df2)

    # Combinar los resultados en un solo DataFrame por query
    df_query1 = pd.concat(resultados_query1, ignore_index=True) if resultados_query1 else pd.DataFrame()
    df_query2 = pd.concat(resultados_query2, ignore_index=True) if resultados_query2 else pd.DataFrame()

    # Guardar los datos en nuevas pestañas del archivo original
    guardar_en_excel(df_query1, df_query2, ruta_excel)

    # Mostrar el tiempo total de ejecución
    print(f"Datos guardados correctamente en {time.time() - start_time:.2f} segundos.")

if __name__ == "__main__":
    main()
