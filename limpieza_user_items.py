import json

# Ruta del archivo original y el archivo nuevo
input_file = 'data/australian_users_items.json'
output_file = 'data/finish_australian_users_items.json'

# Leer el archivo con codificación utf-8
with open(input_file, 'r', encoding='utf-8') as file:
    data = file.read()

# Reemplazar comillas simples por comillas dobles
data = data.replace("'", '"')

# Guardar el archivo nuevo con codificación utf-8
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(data)

print(f"Archivo guardado correctamente como {output_file}")
