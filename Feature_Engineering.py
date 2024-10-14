import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import ast
import json
import os

# Descargar el lexicon de VADER si no está descargado
nltk.download('vader_lexicon')

# Inicializar el analizador de sentimientos
sia = SentimentIntensityAnalyzer()

def get_sentiment(text):
    """Retorna 0 (malo), 1 (neutral) o 2 (positivo) basado en el texto."""
    if not text or not isinstance(text, str):
        return 1  # Neutral
    score = sia.polarity_scores(text)['compound']
    return 2 if score >= 0.05 else 0 if score <= -0.05 else 1

def process_reviews(input_path, output_path):
    """Procesa el archivo de reseñas aplicando análisis de sentimiento."""
    with open(input_path, 'r', encoding='utf-8') as fin, \
         open(output_path, 'w', encoding='utf-8') as fout:
        for line_num, line in enumerate(fin, 1):
            try:
                # Convertir la línea a un diccionario
                record = ast.literal_eval(line)
                
                # Aplicar análisis de sentimiento a cada reseña
                for review in record.get('reviews', []):
                    review['sentiment_analysis'] = get_sentiment(review.get('review', ''))
                    review.pop('review', None)  # Eliminar el campo original
                
                # Escribir el registro modificado en el archivo de salida
                json.dump(record, fout, ensure_ascii=False)
                fout.write('\n')
            except (ValueError, SyntaxError) as e:
                print(f"Error en línea {line_num}: {e}")

    print(f"Archivo procesado y guardado en: {output_path}")

def main():
    input_file = 'data/australian_user_reviews.json'
    output_file = 'data/finish_australian_user_reviews.json'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    process_reviews(input_file, output_file)

if __name__ == "__main__":
    main()
