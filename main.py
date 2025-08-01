import sys
from datetime import datetime
from services.export_abastecimiento_tienda import export_abastecimiento_tienda
from scripts.fetch_tracking import ejecutar_tracking

def run_tracking():
    print("🔎 Ejecutando tracking...")
    ejecutar_tracking()

def run_abastecimiento():
    print("📦 Exportando abastecimiento tienda...")
    fecha_inicio = datetime(2025, 7, 1)
    fecha_fin = datetime(2025, 7, 23)
    export_abastecimiento_tienda(
        fecha_inicio,
        fecha_fin,
        "output/abastecimiento_tienda_julio.csv"
    )

def show_help():
    print("""
🛠️ Comandos disponibles:

  tracking        → Ejecuta la exportación de tracking
  abastecimiento  → Exporta abastecimiento por rango fijo (julio)
  help            → Muestra esta ayuda

📌 Uso:
  python main.py tracking
  python main.py abastecimiento
""")

def main():
    print("⏱️ Iniciando:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if len(sys.argv) < 2:
        show_help()
        return

    comando = sys.argv[1].lower()

    if comando == "tracking":
        run_tracking()
    elif comando == "abastecimiento":
        run_abastecimiento()
    else:
        show_help()

    print("✅ Finalizado:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main()
