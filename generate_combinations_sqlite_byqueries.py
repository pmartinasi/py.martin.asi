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
    for result in generate_combinations(min_length, max_length):
        pass_arr.append(str(result))
        i = 1000000
        print("generando: " + str(result) + "\t" + str(int(pc(len(pass_arr), i))) + "% (bloque de " + str(i) +" generados).")
        if(len(pass_arr)>i):
            print("insert calling")
            insert_array_data(pass_arr)
            pass_arr = []
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

def export_table_to_final_db(temp_db="BrutePass_tmp.db", final_db="BrutePass.db", selectquery="SELECT passTXT FROM passw"):
    """
    Export the 'passw' table from the temporary database to the final database.
    
    Args:
    temp_db (str): The name of the temporary database. Default is 'BrutePass_tmp.db'.
    final_db (str): The name of the final database. Default is 'BrutePass.db'.
    """
    try:
        print("   ")
        print("   ")
        print(f"Exporting table 'passw' from {temp_db} to {final_db}.")
        print(f"query: {selectquery}")
        # Connect to both databases
        if(final_db==temp_db):
            conn_final = sqlite3.connect(final_db)
            cursor_final = conn_final.cursor()
        else:
            conn_temp = sqlite3.connect(temp_db)
            conn_final = sqlite3.connect(final_db)
            cursor_temp = conn_temp.cursor()
            cursor_final = conn_final.cursor()
            
        print("conected to database.")

        # Create the 'passw' table in the final database if it doesn't exist
        cursor_final.execute("""
        CREATE TABLE IF NOT EXISTS passw (
            passTXT VARCHAR(128) PRIMARY KEY
        )
        """)

        print("recovering data.")
        # Select all data from the 'passw' table in the temporary database
        
        if(final_db==temp_db):
            cursor_final.execute(selectquery)
            rows = cursor_final.fetchall()
        else:
            cursor_temp.execute(selectquery)
            rows = cursor_temp.fetchall()
            
        #rows = cursor_temp.fetchall()
        print("Data recovered from {temp_db}. Now inserting into {final_db}.")

        # Insert the data into the 'passw' table in the final database
        cursor_final.executemany("INSERT OR IGNORE INTO passw (passTXT) VALUES (?)", rows)
        print("OK")
        
        # Commit the changes and close the connections
        if(final_db!=temp_db):
            conn_temp.close()
        conn_final.commit()
        conn_final.close()
        print(f"Table 'passw' exported successfully from {temp_db} to {final_db}.")

    except sqlite3.Error as e:
        print(f"An error occurred during export: {e}")

if __name__ == '__main__':
    export_table_to_final_db(temp_db="BrutePass.db", final_db="BrutePass.db", selectquery="SELECT concat(p1.passTXT, p2.passTXT) as passTXTJoin FROM passw as p1 INNER JOIN passw p2;")
