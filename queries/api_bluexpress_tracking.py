import requests
import pandas as pd
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox

def fetch_guide_data(guide_number):
    """Fetch guide data from the API with required headers."""
    url = f"https://bx-tracking.bluex.cl/bx-tracking/v1/tracking-pull/{guide_number}"

    # Headers necesarios para la API
    headers = {
        "BX-TOKEN": "6139a866186c720e5b4cc36a42f309f1",            # Reemplaza con tu token
        "BX-USERCODE": "14802",      # Reemplaza con tu código de usuario
        "BX-CLIENT-ACCOUNT": "81201000-15-8"  # Reemplaza con tu cuenta de cliente
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            messagebox.showerror(
                "Error", f"API Error: {response.status_code} - {response.text}"
            )
            return None
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")
        return None

def save_to_excel(all_data, file_path):
    """Save data to an Excel file."""
    try:
        main_data_list = []
        pinchazos_data_list = []

        for data in all_data:
            if not data:
                continue

            # Extract main data
            main_data = {
                "ID Especie Valorada": data["data"].get("idEspecieValorada"),
                "Nro OS": data["data"].get("nroOS"),
                "Fecha Creación": data["data"].get("fechaCreacion"),
                "Número Referencia": data["data"].get("numeroReferencia"),
                "Cuenta Corriente": data["data"].get("ctaCte"),
                "Origen Dirección": data["data"].get("origen", {}).get("direccion"),
                "Destino Dirección": data["data"].get("destino", {}).get("direccion"),
                "Tipo Servicio": data["data"].get("nombreTipoServicio"),
                "Peso Físico": data["data"].get("pesoFisico"),
                "Peso Volumen": data["data"].get("pesoVolumen"),
                "Valor Flete": data["data"].get("valorFlete"),
                "Cantidad Piezas": data["data"].get("cantidadPiezas"),
                "Macro Estado Actual": data["data"].get("macroEstadoActual"),
                "Fecha Macro Estado": data["data"].get("fechaMacroEstadoActual"),
            }
            main_data_list.append(main_data)

            # Extract pinchazos (movements)
            pinchazos = data["data"].get("pinchazos", [])
            for p in pinchazos:
                pinchazos_data = {
                    "Nro OS": data["data"].get("nroOS"),
                    "Código Movimiento": p.get("tipoMovimiento", {}).get("codigo"),
                    "Descripción Movimiento": p.get("tipoMovimiento", {}).get("descripcion"),
                    "Código Pieza": p.get("codigoPieza"),
                    "Fecha Hora": p.get("fechaHora"),
                    "Cantidad Piezas": p.get("cantidadPiezas"),
                    "Observación": p.get("observacion"),
                }
                pinchazos_data_list.append(pinchazos_data)

        # Save to Excel
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            pd.DataFrame(main_data_list).to_excel(writer, sheet_name="Main Data", index=False)
            pd.DataFrame(pinchazos_data_list).to_excel(writer, sheet_name="Pinchazos", index=False)

        messagebox.showinfo("Success", f"File saved successfully at {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving file: {e}")

def process_guides():
    """Process the guide numbers and generate the Excel."""
    guide_numbers = guide_entry.get()
    if not guide_numbers:
        messagebox.showwarning("Input Error", "Ingresar las guias separadas por comas.")
        return

    guide_numbers = [g.strip() for g in guide_numbers.split(",")]
    all_data = []

    for guide_number in guide_numbers:
        data = fetch_guide_data(guide_number)
        if data:
            all_data.append(data)

    if all_data:
        # Ask where to save the file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
        )
        if file_path:
            save_to_excel(all_data, file_path)

# Set up the GUI
root = Tk()
root.title("Guide to Excel Exporter")
root.geometry("500x250")

Label(root, text="Enter Guide Numbers (comma-separated):", font=("Arial", 12)).pack(pady=10)
guide_entry = Entry(root, width=50, font=("Arial", 12))
guide_entry.pack(pady=5)

Button(root, text="Process Guides", command=process_guides, font=("Arial", 12)).pack(pady=20)

root.mainloop()
