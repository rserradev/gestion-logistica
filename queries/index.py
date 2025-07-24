import requests
import pandas as pd
from tabulate import tabulate

# URL de la API
url = 'https://apis.digital.gob.cl/fl/feriados'

# Encabezados comunes (ajusta según los que uses en Postman)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Connection': 'keep-alive',
}

try:
    # Hacer una solicitud a la API
    response = requests.get(url, headers=headers, timeout=10)
    # Verificar que la solicitud fue exitosa
    response.raise_for_status()
    # Procesar la respuesta JSON
    datos = response.json()
    # Convertir los datos en un DataFrame de pandas
    df = pd.DataFrame(datos)
    # Especificar el orden deseado de las columnas
    columnas_ordenadas = ['fecha', 'nombre', 'tipo', 'irrenunciable', 'comentarios', 'leyes']
    # Reestructurar el DataFrame con las columnas ordenadas
    df = df.reindex(columns=columnas_ordenadas)
    # Guardar los datos en un archivo Excel
    archivo_excel = 'feriados.xlsx'
    df.to_excel(archivo_excel, index=False)
    print(f'Archivo guardado en {archivo_excel}')
    # Mostrar los datos en la consola
    print(df)
except requests.exceptions.HTTPError as http_err:
    print(f'Error HTTP: {http_err}')
except requests.exceptions.ConnectionError as conn_err:
    print(f'Error de conexión: {conn_err}')
except requests.exceptions.Timeout as timeout_err:
    print(f'Error de tiempo de espera: {timeout_err}')
except requests.exceptions.RequestException as req_err:
    print(f'Error en la solicitud: {req_err}')
except Exception as e:
    print(f'Error inesperado: {e}')