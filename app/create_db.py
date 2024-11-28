import psycopg2
import os

# PostgreSQL connection settings
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Create database and table
try:
    # Connect to PostgreSQL
    connection = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    connection.autocommit = True
    cursor = connection.cursor()

    # Create the database if it doesn't exist
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{POSTGRES_DB}';")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {POSTGRES_DB} OWNER {POSTGRES_USER};")
    cursor.close()
    connection.close()

    # Connect to the new database and create the table
    connection = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    cursor = connection.cursor()

    # Create a table to store weather data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS public.weather_data (
        id SERIAL PRIMARY KEY,
        data JSONB NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    connection.commit()
    cursor.close()
    connection.close()
    print("Database and table created successfully.")
except Exception as e:
    print(f"Error creating database or table: {e}")
