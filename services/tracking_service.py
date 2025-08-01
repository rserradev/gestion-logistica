import requests
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde .env
load_dotenv()

API_BASE = "https://bx-tracking.bluex.cl/bx-tracking/v1/tracking-pull/"

# Obtener valores del .env
BX_TOKEN = os.getenv('BX_TOKEN')
BX_USERCODE = os.getenv('BX_USERCODE')
BX_CLIENT_ACCOUNT = os.getenv('BX_CLIENT_ACCOUNT')

def obtener_ultimo_pinchazo(tracking):
    try:
        url = f"{API_BASE}{tracking}"

        headers = {
            "BX-TOKEN": BX_TOKEN,
            "BX-USERCODE": BX_USERCODE,
            "BX-CLIENT-ACCOUNT": BX_CLIENT_ACCOUNT,
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        pinchazos = data.get('data', {}).get('pinchazos', [])

        if pinchazos:
            # Ordenar por fechaHora descendente
            pinchazos.sort(key=lambda x: x['fechaHora'], reverse=True)
            ultimo = pinchazos[0]

            return {
                'orden': tracking,
                'ultimo_pinchazo': ultimo.get('tipoMovimiento', {}).get('descripcion', 'Desconocido'),
                'ultima_fechaHora': ultimo.get('fechaHora', 'No disponible')
            }
        else:
            return {
                'orden': tracking,
                'ultimo_pinchazo': 'Sin pichazos',
                'ultima_fechaHora': 'N/A'
            }

    except Exception as e:
        return {
            'orden': tracking,
            'ultimo_pinchazo': f'Error: {str(e)}',
            'ultima_fechaHora': 'N/A'
        }