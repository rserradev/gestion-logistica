import pandas as pd
import json

def convertir_json_a_excel(json_file, excel_file):
    # Cargar el archivo JSON
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Extraer los datos de la clave "history"
    history_data = data["history"]

    # Extraer datos de 'items' y aplanar la estructura
    df = pd.json_normalize(history_data, record_path=["items"], meta=[
        "id", "identificador_ruta", "identificador_vehiculo", "guia", "hoja_ruta", "rut_emp", 
        "desc_emp", "fecha_estimada", "fecha_llegada", "estado", "sub_estado", "destino", 
        "usuario_movil", "id_cliente", "nombre_cliente", "direccion_cliente", "telefono_cliente", 
        "correo_cliente", "numsolgui", "fectrantsl", "fecdesfis", "fecemigui", "tipogui", "depto", 
        "codregi", "codciud", "codcomu", "desc_comuna", "localventa", "localdespa", "jornada", 
        "fecsoldes", "asn_id", "do_id", "quien_recibe", "codigo_autorizacion", "expectativa", 
        "do_line_id", "completado", "created_at", "updated_at"], errors="ignore")

    # Extraer datos de 'attempts', que es un diccionario
    attempts_data = [{**record["attempts"], "id": record["id"]} for record in history_data if "attempts" in record]
    attempts_df = pd.DataFrame(attempts_data)

    # Fusionar ambos DataFrames por el ID
    df_final = df.merge(attempts_df, on="id", how="left")

    # Ordenar las columnas como en el JSON original
    json_order = list(history_data[0].keys())
    json_order.remove("items")
    json_order.remove("attempts")
    json_order.extend(["sku", "cartonid", "cantidad_despachada", "cantidad_entregada"])
    json_order.extend(["numero_intentos", "fecha_intento", "fecha_actualizacion"])
    
    # Aplicar el orden
    df_final = df_final[json_order]

    # Guardar en un archivo Excel
    df_final.to_excel(excel_file, index=False)
    
    print(f"✅ Conversión completada. Archivo guardado en: {excel_file}")

# 📌 Ruta del archivo JSON y el archivo de salida en Excel
json_file = "response.json"  # Reemplázalo con tu archivo JSON
excel_file = "historial_ordenado.xlsx"  # Nombre del archivo de salida

# Ejecutar la conversión
convertir_json_a_excel(json_file, excel_file)
