from datetime import datetime, timedelta
import pandas as pd 
from db.engine import get_engine
from queries.query_abastecimiento_tienda import get_abastecimiento_tienda

def export_abastecimiento_tienda(fecha_inicio: str, fecha_fin: str, ruta_salida="output/abastecimiento_tienda.csv"):
    engine = get_engine('SCP') # Obtener engine de SCP
    df_total = pd.DataFrame() # DataFrame acumulador
    dia_actual = fecha_inicio

    while dia_actual <= fecha_fin:
        desde = dia_actual.strftime("%Y-%m-%d 00:00:00")
        hasta = dia_actual.strftime("%Y-%m-%d 23:59:59")
        print(f"🔎 Consultando data para el día: {dia_actual.strftime('%Y-%m-%d')}")

        query = get_abastecimiento_tienda(desde, hasta)
        df_dia = pd.read_sql(query, engine)

        if not df_dia.empty:
            df_total = pd.concat([df_total, df_dia]) # Concatenar data
            print(f"✅ Data agregada para el día: {dia_actual.strftime('%Y-%m-%d')}")
        else:
            print(f"Sin resultados para el día: {dia_actual.strftime('%Y-%m-%d')}")

        dia_actual += timedelta(days=1)

    df_total.to_csv(ruta_salida, index=False)
    print(f"✅ Data exportada exitosamente a: {ruta_salida}")