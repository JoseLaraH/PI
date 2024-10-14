import pandas as pd

# Cargar el archivo .json
df = pd.read_json('data/output_steam_games.json', lines=True)

# Eliminar las filas que contienen valores NaN
df_cleaned = df.dropna(how='all')

# Guardar el archivo limpio en la carpeta 'data'
df_cleaned.to_json('data/output_steam_games_light.json', orient='records', lines=True)

print("Se han eliminado las filas que contenían solo valores NaN y el archivo limpio se ha guardado en la carpeta 'data'.")
