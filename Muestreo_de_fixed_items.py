import json
import random
import os
import ijson

def reservoir_sampling_json_array(input_file, output_file, sample_size):
    """
    Realiza muestreo aleatorio simple (Reservoir Sampling) de un archivo JSON que contiene una lista de objetos.
    
    Args:
        input_file (str): Ruta al archivo JSON de entrada.
        output_file (str): Ruta al archivo JSON de salida.
        sample_size (int): Número de registros a muestrear.
    """
    reservoir = []
    total_records = 0

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            # Utilizar ijson para iterar sobre cada elemento de la lista JSON
            objects = ijson.items(infile, 'item')
            for i, obj in enumerate(objects, 1):
                if i <= sample_size:
                    reservoir.append(obj)
                else:
                    j = random.randint(1, i)
                    if j <= sample_size:
                        reservoir[j - 1] = obj
                total_records += 1

        if total_records < sample_size:
            print(f"Advertencia: El archivo de entrada tiene solo {total_records} registros, que es menor que el tamaño de la muestra solicitado ({sample_size}).")
            sample_size = total_records

        # Escribir la muestra en el archivo de salida como una lista JSON
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(reservoir, outfile, ensure_ascii=False, indent=4)

        print(f"Muestreo completado. Se han guardado {len(reservoir)} registros en '{output_file}'.")
        print(f"Total de registros procesados: {total_records}")

    except FileNotFoundError:
        print(f"Error: El archivo de entrada '{input_file}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def main():
    # Definir rutas de entrada y salida
    input_file = os.path.join('data', 'fixed_australian_users_items.json')
    output_file = os.path.join('data', 'sampled_australian_users_items.json')
    sample_size = 1000  # Número de registros a muestrear

    print(f"Comenzando el muestreo de '{input_file}' para obtener {sample_size} registros...")
    reservoir_sampling_json_array(input_file, output_file, sample_size)

if __name__ == "__main__":
    main()
