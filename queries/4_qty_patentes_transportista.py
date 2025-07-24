import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from sqlalchemy import create_engine
import numpy as np

# Conexión
DB_USER = "sglRonaldo"
DB_PASSWORD = "sglRonaldo022025"
DB_HOST = "sgl.cfqgmxknp1yx.us-east-1.rds.amazonaws.com"
DB_PORT = 3306
DB_DATABASE = "beetrack"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}")

fecha_inicio = '2025-06-01'
fecha_fin = datetime.now().date().strftime('%Y-%m-%d')

query = """
    SELECT DISTINCT
        dh.delivery_end_dttm as fecha_compromiso,
        dh.alias as transportista,
        COUNT(DISTINCT dd.trailer_number) as patentes_unicas
    FROM beetrack.dispatch_hdrs dh
    JOIN beetrack.dispatch_dtls dd
        ON dd.shipmentdocument = dh.shipmentdocument
    WHERE 1 = 1
        AND (dd.shipmentdocument_type IN (0, 5) OR dd.shipmentdocument_type IS NULL)
        AND dd.order_type NOT IN ("Pickup", "PuntoRetiro")
        AND dh.alias IN ('PIPAU', 'ATTAM', 'SPREAD')
        AND dh.delivery_end_dttm BETWEEN %(fecha_inicio)s AND %(fecha_fin)s
    GROUP BY dh.delivery_end_dttm, dh.alias
    ORDER BY dh.delivery_end_dttm
"""

df = pd.read_sql(query, engine, params={
    'fecha_inicio': fecha_inicio,
    'fecha_fin': fecha_fin
})

# Primero aseguramos que 'fecha_compromiso' sea datetime
df['fecha_compromiso'] = pd.to_datetime(df['fecha_compromiso'])

# Obtenemos las fechas únicas ordenadas para el eje X
fechas = sorted(df['fecha_compromiso'].unique())
labels = [fecha.strftime('%d-%m') for fecha in fechas]

# Obtenemos transportistas únicos
transportistas = df['transportista'].unique()

# Creamos un índice para las fechas
x = np.arange(len(fechas))

# Parámetros para la figura
num_transportistas = len(transportistas)
fig_width = 0.3
group_gap = 1.0

fig, ax = plt.subplots(figsize=(14,7))

# Graficar cada transportista con su desplazamiento en x para agrupar barras
for i, transportista in enumerate(transportistas):
    # Filtramos datos por transportista
    df_t = df[df['transportista'] == transportista]
    
    # Creamos lista con cantidad de patentes por fecha (llenamos con 0 si no hay datos para esa fecha)
    patentes = []
    for fecha in fechas:
        valor = df_t[df_t['fecha_compromiso'] == fecha]['patentes_unicas']
        patentes.append(valor.values[0] if not valor.empty else 0)
    
    # Posición de barras para este transportista
    positions = (np.arange(len(fechas)) * group_gap) - (fig_width * num_transportistas / 2) + i * fig_width + fig_width / 2
    
    rects = ax.bar(positions, patentes, fig_width, label=transportista)
    ax.bar_label(rects, padding=3)
    
    # Etiquetas encima de barras
    ax.bar_label(rects, padding=3)

# Configuraciones del eje X con las fechas
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=80)

ax.set_ylabel('Patentes únicas')
ax.set_xlabel('Fecha de compromiso')
ax.set_title('Patentes únicas por compromiso de transportista')
ax.legend(title='Transportista', loc='upper left')
ax.grid(True, axis='y')
fig.tight_layout()

plt.show()