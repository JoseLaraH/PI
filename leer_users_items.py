import ast
import json

def process_file(input_path, output_path):
    data_list = []
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue  # Saltar líneas vacías
                try:
                    # Evaluar la línea como un literal de Python
                    data = ast.literal_eval(line)
                    data_list.append(data)
                except Exception as e:
                    print(f"Error al procesar la línea {line_number}: {e}")
                    print(f"Línea problemática: {line}")
                    return
        # Guardar la lista de diccionarios en un archivo JSON
        with open(output_path, 'w', encoding='utf-8') as f_out:
            json.dump(data_list, f_out, indent=2, ensure_ascii=False)
        print(f"Archivo JSON creado exitosamente en '{output_path}'")
    except Exception as e:
        print(f"Ocurrió un error al procesar el archivo: {e}")

# Uso de la función
process_file('data/australian_users_items.json', 'data/fixed_australian_users_items.json')

