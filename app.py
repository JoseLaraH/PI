from fastapi import FastAPI
import pandas as pd
import json

app = FastAPI()

# Cargar los datos (esto debe ajustarse dependiendo de dónde están ubicados los archivos)
file_path_games = 'data/output_steam_games_light.json'

with open(file_path_games, 'r') as f:
    games_data = [json.loads(line) for line in f.readlines()]

# Convertir los datos de juegos a un DataFrame para un manejo más sencillo
games_df = pd.DataFrame(games_data)

# Función que calcula los ítems y porcentaje de contenido gratis por año para una desarrolladora
def developer(developer):
    # Filtrar juegos por desarrollador
    dev_games = games_df[games_df['developer'] == developer]
    
    # Extraer el año de lanzamiento
    dev_games['release_year'] = pd.to_datetime(dev_games['release_date'], errors='coerce').dt.year
    
    # Calcular la cantidad total de ítems por año
    item_count_per_year = dev_games.groupby('release_year').size().reset_index(name='Cantidad de Items')
    
    # Ajustar el criterio para juegos gratuitos: "Free", "Free to Play", o 0.0
    dev_games['is_free'] = dev_games['price'].apply(lambda x: x in ["Free", "Free to Play"] or x == 0.0)
    
    # Calcular el porcentaje de contenido gratuito por año
    free_content_per_year = dev_games.groupby('release_year')['is_free'].mean().reset_index(name='Contenido Free')
    free_content_per_year['Contenido Free'] = (free_content_per_year['Contenido Free'] * 100).round(2)
    
    # Combinar ambos resultados en un solo DataFrame
    result = pd.merge(item_count_per_year, free_content_per_year, on='release_year', how='left').fillna(0)
    result.columns = ['Año', 'Cantidad de Items', 'Contenido Free']
    
    return result

# Punto de inicio básico
@app.get("/")
def read_root():
    return {"message": "FastAPI app is running!"}

# Función simple de ejemplo
@app.get("/square/{number}")
def square_number(number: int):
    return {"number": number, "square": number ** 2}

# Endpoint que proporciona las estadísticas por desarrolladora
@app.get("/developer/{desarrollador}")
def developer_stats(desarrollador: str):
    # Llamar a la función que calcula los ítems y el contenido gratis por año
    result = developer(desarrollador)
        
    # Convertir el DataFrame en un formato adecuado para devolverlo como JSON
    return result.to_dict(orient='records')