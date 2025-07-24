# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

# Configuracion de las bases de datos
DATABASES = {
    'SCP': {
        'ENGINE': 'mysql+pymysql',
        'NAME': os.getenv('SCP_DB_NAME'),
        'USER': os.getenv('SCP_DB_USER'),
        'PASSWORD': os.getenv('SCP_DB_PASSWORD'),
        'HOST': os.getenv('SCP_DB_HOST'),
        'PORT': os.getenv('SCP_DB_PORT', '3306'),
    }
}

# Contruccion de la conexion
def build_connection_string(db_config: dict) -> str:
    """
    Construye la cadena de conexión para una base de datos
    """
    return f"{db_config['ENGINE']}://{db_config['USER']}:{db_config['PASSWORD']}@{db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}"