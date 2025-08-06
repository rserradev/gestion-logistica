import os
import pandas as pd
from datetime import datetime
from services.tracking_service import obtener_ultimo_pinchazo

def ejecutar_tracking():
    # Rutas
    fechahora_actual = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    input_file = os.path.join("input", "beetrack_blue_dad_20250806.xlsx")
    output_file = os.path.join("output", f"beetrack_blue_dad_api_{fechahora_actual}.xlsx")

    # Leer archivo de entrada
    df = pd.read_excel(input_file)

    # Validar columna 'orden'
    if 'Orden' not in df.columns:
        raise Exception("❌ La columna 'Orden' no está presente en el archivo Excel.")
    
    # Solo valores unicos
    df_ordenes_unicas = df['Orden'].drop_duplicates()

    # Lista para resultados
    resultados = []

    # Recorrer cada orden y consultar API
    for orden in df_ordenes_unicas:
        # Solo valores unicos
        resultado = obtener_ultimo_pinchazo(orden)
        resultados.append(resultado)
        print(f"✔️ Procesado tracking: {orden}, faltan {len(df_ordenes_unicas) - len(resultados)} ordenes")

    # Exportar resultados a Excel
    df_resultado = pd.DataFrame(resultados)
    df_resultado.to_excel(output_file, index=False)

    print(f"\n✅ Resultados guardados en: {output_file}")