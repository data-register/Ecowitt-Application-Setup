from flask import Flask, jsonify
import requests
import psycopg2
import os
import json

app = Flask(__name__)

# PostgreSQL connection settings
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Ecowitt API settings
API_URL = "https://api.ecowitt.net/api/v3/device/real_time?application_key=61759DF4094EBA1A61E070A285A2DAF7&api_key=fe33f769-d487-433c-a31d-8e504df4076f&mac=48:E7:29:5F:72:44&call_back=all"

# Function to store data in PostgreSQL
def store_data_to_postgres(data):
    try:
        connection = psycopg2.connect(host=POSTGRES_HOST, port=POSTGRES_PORT, database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD)
        cursor = connection.cursor()
    
        # Insert the data into the table
        cursor.execute(
            "INSERT INTO weather_data (data) VALUES (%s);",
            [json.dumps(data)]
        )

        # Commit and close the connection
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error storing data to PostgreSQL: {e}")

# Endpoint to trigger data fetch and store
@app.route('/fetch_store', methods=['GET'])
def fetch_and_store():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        # Store data to PostgreSQL
        store_data_to_postgres(data)
        return jsonify({"message": "Data fetched and stored successfully."})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching data from Ecowitt API: {e}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
