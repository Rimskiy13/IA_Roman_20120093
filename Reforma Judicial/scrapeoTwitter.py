import snscrape.modules.twitter as sntwitter
import json
import time
from datetime import datetime, timedelta

def scrape_tweets_with_content_to_json(query, max_tweets_per_day=50, days_to_scrape=7, output_file="tweets_contenido.json"):

    tweets_data = []

    # Cargar datos existentes para evitar duplicados
    try:
        with open(output_file, "r", encoding="utf-8") as file:
            tweets_data = json.load(file)
    except FileNotFoundError:
        print("Archivo JSON no encontrado. Se creará uno nuevo.")
    
    # Convertir tweets ya guardados a un conjunto de IDs para evitar duplicados
    existing_tweet_ids = {tweet.get("id") for tweet in tweets_data}

    # Rango de fechas
    today = datetime.now()
    for day_offset in range(days_to_scrape):
        date_until = today - timedelta(days=day_offset)
        date_since = date_until - timedelta(days=1)

        print(f"Buscando tweets desde {date_since.date()} hasta {date_until.date()}...")

        # Agregar filtro de fechas al query
        date_query = f"{query} since:{date_since.date()} until:{date_until.date()}"
        tweets_fetched = 0

        try:
            for i, tweet in enumerate(sntwitter.TwitterSearchScraper(date_query).get_items()):
                # Limitar la cantidad de tweets por día
                if tweets_fetched >= max_tweets_per_day:
                    break
                
                # Evitar duplicados
                if tweet.id in existing_tweet_ids:
                    continue

                # Extraer contenido
                links = [word for word in tweet.content.split() if word.startswith("http")]
                tweet_data = {
                    "id": tweet.id,
                    "fecha": str(tweet.date),
                    "usuario": tweet.user.username,
                    "contenido": tweet.content,
                    "enlaces": links
                }
                tweets_data.append(tweet_data)
                existing_tweet_ids.add(tweet.id)
                tweets_fetched += 1

                # Retraso entre tweets para evitar detección
                time.sleep(1)

        except Exception as e:
            print(f"Error al procesar los tweets: {e}. Reintentando...")
            time.sleep(5)  # Pausa para reintentar

        print(f"{tweets_fetched} tweets recopilados para el rango {date_since.date()} - {date_until.date()}.")

    # Guardar los tweets en un archivo JSON
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(tweets_data, json_file, ensure_ascii=False, indent=4)

    print(f"Tweets guardados en {output_file}")


# Ejemplo de uso
query = "reforma judicial"
max_tweets_per_day = 20  # Ajusta según tus necesidades
days_to_scrape = 90  # Últimos 90 días

scrape_tweets_with_content_to_json(query, max_tweets_per_day, days_to_scrape, output_file="tweets_contenido.json")
