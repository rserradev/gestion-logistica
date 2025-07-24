import win32com.client
import re
import openpyxl

def extract_info_from_email(email):
    carga_pattern = r"Número de carga:\s*(\d+)"
    orden_pattern = r"Orden afectada:\s*(\d+)"
    lpn_pattern = r"LPN afectado:\s*(\w+)"
    os_pattern = r"OS generada:\s*(\d+)"

    carga_match = re.search(carga_pattern, email.Body)
    orden_match = re.search(orden_pattern, email.Body)
    lpn_match = re.search(lpn_pattern, email.Body)
    os_match = re.search(os_pattern, email.Body)

    if carga_match and orden_match and lpn_match and os_match:
        carga = carga_match.group(1)
        orden_afectada = orden_match.group(1)
        lpn_afectado = lpn_match.group(1)
        os_generada = os_match.group(1)
        received_time = email.ReceivedTime.strftime("%Y-%m-%d %H:%M:%S")  # Agregar fecha y hora recibido
        return carga, orden_afectada, lpn_afectado, os_generada, received_time
    else:
        return None

def process_emails_in_folder(folder):
    data = []
    for item in folder.Items:
        if item.Class == 43:  # Verificar si es un correo
            info = extract_info_from_email(item)
            if info:
                data.append(info)
    return data

def write_to_excel(data):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Número de carga", "Orden afectada", "LPN afectado", "OS generada", "Fecha y hora recibido"])
    for carga, orden_afectada, lpn_afectado, os_generada, received_time in data:
        ws.append([carga, orden_afectada, lpn_afectado, os_generada, received_time])
    wb.save("data.xlsx")

def main():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    folder_name = "Dispatcher (PRC)"
    carpetas_folder = outlook.Folders.Item("ronaldo.serra@cencosud.cl").Folders.Item("Carpetas")
    dispatcher_folder = carpetas_folder.Folders.Item(folder_name)
    data = process_emails_in_folder(dispatcher_folder)
    if data:
        write_to_excel(data)
        print("Datos extraídos y guardados en 'data.xlsx'.")
    else:
        print("No se encontraron datos en los correos electrónicos.")

if __name__ == "__main__":
    main()
