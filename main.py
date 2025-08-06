import sys
from datetime import datetime
from services.export_abastecimiento_tienda import export_abastecimiento_tienda, export_traspasos_tienda
from scripts.fetch_tracking import ejecutar_tracking

def run_tracking():
    print("🔎 Ejecutando tracking...")
    ejecutar_tracking()

def run_abastecimiento_tienda():
    print("📦 Exportando abastecimiento tienda...")
    fecha_inicio = datetime(2025, 7, 1)
    fecha_fin = datetime(2025, 7, 31)
    export_abastecimiento_tienda(fecha_inicio, fecha_fin, "output/abastecimiento_tienda_julio.csv")

def run_traspasos_tienda():
    print("📦 Exportando traspasos tienda...")
    fecha_inicio = datetime(2025, 7, 1)
    fecha_fin = datetime(2025, 7, 31)
    export_traspasos_tienda(fecha_inicio, fecha_fin, "output/traspasos_tienda_julio.csv")

def show_help():
    print("""
🛠️ Comandos disponibles:

  tracking        → Ejecuta la exportación de tracking
  abastecimiento_tienda  → Exporta abastecimiento por rango fijo (julio)
  traspasos_tienda → Exporta traspasos tienda por rango fijo (julio)
  help            → Muestra esta ayuda

📌 Uso:
  python main.py tracking
  python main.py abastecimiento_tienda
  python main.py traspasos_tienda
""")

def main():
    print("⏱️ Iniciando:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if len(sys.argv) < 2:
        show_help()
        return

    comando = sys.argv[1].lower()

    if comando == "tracking":
        run_tracking()
    elif comando == "abastecimiento_tienda":
        run_abastecimiento_tienda()
    elif comando == "traspasos_tienda":
        run_traspasos_tienda()
    else:
        show_help()

    print("✅ Finalizado:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main()
