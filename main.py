# main.py
from datetime import datetime
from services.export_abastecimiento_tienda import export_abastecimiento_tienda

def main():
    print("Iniciando a la hora: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    fecha_inicio = datetime(2025, 7, 1)
    fecha_fin = datetime(2025, 7, 23)
    export_abastecimiento_tienda(fecha_inicio, fecha_fin, "output/abastecimiento_tienda_julio.csv")
    print("Finalizado a la hora: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
if __name__ == "__main__":
    main()