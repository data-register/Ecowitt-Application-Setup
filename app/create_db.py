import psycopg2

# PostgreSQL connection settings
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB = "ecowitt"
POSTGRES_USER = "ecowitt_user"
POSTGRES_PASSWORD = "ecowitt_password"

# Create database and table
try:
    connection = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    connection.autocommit = True
    cursor = connection.cursor()

    # Create the database if it doesn't exist
    cursor.execute(f"CREATE DATABASE {POSTGRES_DB};")
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
    CREATE TABLE IF NOT EXISTS weather_data (
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
