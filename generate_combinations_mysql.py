import itertools
import string
import sys
import mysql.connector
import time
from multiprocessing import Pool, cpu_count

# MySQL connection details (adjust as necessary)
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = ""  # Change this to your MySQL root password
DB_NAME = "BrutePass_tmp"

def create_database():
    """Create a MySQL database if it does not exist."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' created or already exists.")
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sys.exit(1)

def create_table():
    """Create a table named 'passw' with a single column 'passTXT' if it does not exist."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS passw (
            passTXT VARCHAR(128) PRIMARY KEY
        )
        """)
        print("Table 'passw' checked/created.")
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sys.exit(1)

def insert_array_data(pass_arr):
    """Insert a batch of data into the 'passw' table."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        for pass_txt in pass_arr:
            try:
                cursor.execute("INSERT INTO passw (passTXT) VALUES (%s)", (pass_txt,))
                print(f"Inserted '{pass_txt}' into 'passw'.")
            except mysql.connector.IntegrityError:
                print(f"Already '{pass_txt}' in 'passw'.")
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
        sys.exit(1)

def generate_combinations(length):
    """Generate all combinations of printable characters of a specific length."""
    all_chars = string.printable[:-5]  # All printable characters except control ones
    return (''.join(combination) for combination in itertools.product(all_chars, repeat=length))

def process_combinations(length):
    """Generate and save combinations for a specific length."""
    print(f"Processing combinations of length {length}")
    pass_arr = []
    for result in generate_combinations(length):
        pass_arr.append(result)
        if len(pass_arr) >= 1000000:
            print(f"Inserting batch for length {length}...")
            insert_array_data(pass_arr)
            pass_arr = []

    if len(pass_arr) > 0:
        print(f"Inserting final batch for length {length}...")
        insert_array_data(pass_arr)

def count_passw_entries():
    """Count the number of entries in the 'passw' table."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(passTXT) FROM passw;")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
        return None

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python generate_combinations.py min_length max_length")
        sys.exit(1)

    min_l = int(sys.argv[1])
    max_l = int(sys.argv[2])

    if min_l < 1 or max_l < min_l:
        print("Arguments must be positive, and max_length must be greater or equal to min_length.")
        sys.exit(1)

    # Create the database and table
    create_database()
    create_table()

    # Use multiprocessing to process each length in parallel
    lengths = list(range(min_l, max_l + 1))
    pool = Pool(cpu_count())  # Create a pool of processes
    pool.map(process_combinations, lengths)
    pool.close()
    pool.join()

    # Optionally count the number of inserted entries
    count = count_passw_entries()
    print(f"Total entries in the database: {count}")
