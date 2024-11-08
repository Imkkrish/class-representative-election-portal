import mysql.connector
from mysql.connector import errorcode

# Database configurations
config = {
    'user': 'root',
    'password': 'MySQL123',  # Update with your MySQL password
    'host': 'localhost'
}

# SQL statements to create the database and tables
DB_NAME = 'voting_app'

TABLES = {
    'candidates': (
        "CREATE TABLE IF NOT EXISTS candidates ("
        "  candidate_id INT AUTO_INCREMENT PRIMARY KEY,"
        "  name VARCHAR(50) NOT NULL,"
        "  candidate_username VARCHAR(25) NOT NULL UNIQUE,"
        "  password VARCHAR(255) NOT NULL,"  # Store hashed password
        "  image VARCHAR(255) DEFAULT NULL,"  # Path to candidate's image
        "  department VARCHAR(50) NOT NULL,"
        "  enroll_year VARCHAR(9) NOT NULL,"  # Expected format: '2023-2024'
        "  election_vision TEXT NOT NULL"
        ")"
    ),
    'users': (
        "CREATE TABLE IF NOT EXISTS users ("
        "  userid INT AUTO_INCREMENT PRIMARY KEY,"
        "  name VARCHAR(50) NOT NULL,"
        "  username VARCHAR(25) NOT NULL UNIQUE,"
        "  password VARCHAR(255) NOT NULL,"  # Store hashed password
        "  about TEXT DEFAULT NULL,"
        "  has_voted BOOLEAN DEFAULT FALSE"
        ")"
    ),
    'votes': (
        "CREATE TABLE IF NOT EXISTS votes ("
        "  vote_id INT AUTO_INCREMENT PRIMARY KEY,"
        "  candidate_id INT NOT NULL,"
        "  user_id INT NOT NULL,"
        "  FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id) ON DELETE CASCADE,"
        "  FOREIGN KEY (user_id) REFERENCES users(userid) ON DELETE CASCADE"
        ")"
    ),
}

def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        print(f"Database '{DB_NAME}' created successfully.")
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")
        exit(1)

def connect_to_database():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Check if database exists
        cursor.execute(f"SHOW DATABASES LIKE '{DB_NAME}'")
        db_exists = cursor.fetchone()
        
        if not db_exists:
            create_database(cursor)
        else:
            print(f"Database '{DB_NAME}' already exists.")

        # Connect to the voting_app database
        connection.database = DB_NAME

        # Create tables if they do not exist
        for table_name, table_sql in TABLES.items():
            cursor.execute(table_sql)
            print(f"Table '{table_name}' checked/created successfully.")
        
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(err)

if __name__ == "__main__":
    connect_to_database()
