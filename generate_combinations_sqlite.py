import itertools
import string
import sys
import sqlite3
import time

def create_database(db_name="BrutePass_tmp.db"):
    """Create a SQLite database if it does not exist."""
    conn = sqlite3.connect(db_name)
    print(f"Database '{db_name}' created and connected.")
    conn.close()

def create_table(db_name="BrutePass_tmp.db"):
    """Create a table named 'passw' with a single column 'passTXT' if it does not exist."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passw (
        passTXT VARCHAR(128) PRIMARY KEY
    )
    """)
    print("Table 'passw' checked/created.")
    conn.commit()
    conn.close()

def insert_data(pass_txt, db_name="BrutePass_tmp.db"):
    
    try:
        """Insert data into the 'passw' table."""
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO passw (passTXT) VALUES (?)", (pass_txt,))
        print(f"Inserted '{pass_txt}' into 'passw'.")
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Already '{pass_txt}' into 'passw'.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        time.sleep(90)
        insert_data(pass_txt)
    finally:
        conn.close()
    
def insert_array_data(pass_arr, db_name="BrutePass_tmp.db"):
    """Insert data into the 'passw' table."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    for pass_txt in pass_arr:
        try:
            cursor.execute("INSERT INTO passw (passTXT) VALUES (?)", (pass_txt,))
            print(f"Inserted '{pass_txt}' into 'passw'.")
        except sqlite3.IntegrityError:
            print(f"Already '{pass_txt}' into 'passw'.")
        except Exception as e:
            print(e.message)
            print(e.args)
            conn.commit()
    conn.commit()
    conn.close()

def generate_combinations(min_length, max_length):
    all_chars = string.printable[:-5]  # Obtener todos los caracteres ASCII imprimibles excepto los últimos cinco (\n, \r, \x0b, \x0c, \x0d)
    for length in range(min_length, max_length + 1):
        for combination in itertools.product(all_chars, repeat=length):
            yield ''.join(combination)

def save_to_bbdd(min_length, max_length):
    pass_arr = []
    j = 0
    for result in generate_combinations(min_length, max_length):
        pass_arr.append(str(result))
        i = 10000
        j = j + 1
        print("generando: " + str(result) + "\t" + str(int(pc(len(pass_arr), i))) + "% (bloque de " + str(i) +" generados).")
        if(len(pass_arr)>i):
            print("insert calling")
            insert_array_data(pass_arr)
            pass_arr = []
        if(j>10000000):
            j = 0
            export_table_to_final_db()
    if(len(pass_arr)>0):
        print("insert calling")
        insert_array_data(pass_arr)

def count_passw_entries(db_name="BrutePass_tmp.db"):
    """
    Execute a query to count the number of entries in the 'passw' table in the SQLite database.

    Args:
    db_name (str): The name of the SQLite database file. Default is 'BrutePass_tmp.db'.

    Returns:
    int: The count of entries in the 'passw' table.
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(passTXT) FROM passw;")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

def pc(a, b):
    if(a>b):
        tmp=a
        a=b
        b=a
    tmp = (a/b)*100
    return tmp

def export_table_to_final_db(temp_db="BrutePass_tmp.db", final_db="BrutePass.db"):
    """
    Export the 'passw' table from the temporary database to the final database.
    
    Args:
    temp_db (str): The name of the temporary database. Default is 'BrutePass_tmp.db'.
    final_db (str): The name of the final database. Default is 'BrutePass.db'.
    """
    try:
        
        print(f"Exporting table 'passw' from {temp_db} to {final_db}.")
        # Connect to both databases
        conn_temp = sqlite3.connect(temp_db)
        conn_final = sqlite3.connect(final_db)
        cursor_temp = conn_temp.cursor()
        cursor_final = conn_final.cursor()

        # Create the 'passw' table in the final database if it doesn't exist
        cursor_final.execute("""
        CREATE TABLE IF NOT EXISTS passw (
            passTXT VARCHAR(128) PRIMARY KEY
        )
        """)

        # Select all data from the 'passw' table in the temporary database
        cursor_temp.execute("SELECT passTXT FROM passw")
        rows = cursor_temp.fetchall()

        # Insert the data into the 'passw' table in the final database
        cursor_final.executemany("INSERT OR IGNORE INTO passw (passTXT) VALUES (?)", rows)

        # Commit the changes and close the connections
        conn_final.commit()
        conn_temp.close()
        conn_final.close()
        print(f"Table 'passw' exported successfully from {temp_db} to {final_db}.")

    except sqlite3.Error as e:
        print(f"An error occurred during export: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python generate_combinations.py min_length max_length ")
        sys.exit(1)

    min_l = int(sys.argv[1])
    max_l = int(sys.argv[2])

    if min_l < 1 or max_l < min_l:
        print("Los argumentos deben ser positivos y max_length debe ser mayor o igual que min_length.")
        sys.exit(1)

    # Create the database
    create_database()
    create_database(db_name="BrutePass.db")

    # Create the table
    create_table()
    create_table(db_name="BrutePass.db")
    
    save_to_bbdd(min_l, max_l)
    
    # Export the table to the final database
    export_table_to_final_db()
