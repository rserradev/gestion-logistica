import pandas as pd

# Cargar las dos hojas (pestañas) del mismo archivo Excel en DataFrames
file_path = "ordenes_cc_eta_09_octubre_202410101444.xlsx"
df1 = pd.read_excel(file_path, sheet_name="ordenes_cc_gestion_eta_09")
df2 = pd.read_excel(file_path, sheet_name="ordenes_cc_control_eta_09")

# Realizar un inner join entre los DataFrames basándose en las columnas comunes
merged_df = pd.merge(df1, df2, how="inner", left_on=["SC", "SKU"], right_on=["SOLICITUD", "SKU"])

# Mostrar el resultado
print(merged_df)

# Opcional: guardar el resultado en un nuevo archivo Excel
merged_df.to_excel("resultado_merged.xlsx", index=False)