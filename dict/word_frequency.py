import os
import sqlite3
import sys
import re

def setup_database():
    """Set up the database and table if they do not already exist."""
    conn = sqlite3.connect("dictionary.db")
    cursor = conn.cursor()
    
    # Create the database table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wordFrequency (
        word TEXT PRIMARY KEY,
        repetitions INT DEFAULT 0
    )
    """)
    conn.commit()
    return conn

def update_word_frequency(conn, word):
    """Update the word frequency in the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT repetitions FROM wordFrequency WHERE word = ?", (word,))
    result = cursor.fetchone()
    
    if result:
        # If the word exists, increment its frequency
        cursor.execute("UPDATE wordFrequency SET repetitions = repetitions + 1 WHERE word = ?", (word,))
    else:
        # If the word doesn't exist, insert it with a frequency of 1
        cursor.execute("INSERT INTO wordFrequency (word, repetitions) VALUES (?, ?)", (word, 1))
    
    conn.commit()

def process_text_file(conn, file_path):
    """Read a text file and update word frequencies in the database."""
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read().lower()  # Convert to lowercase to count words consistently
        words = re.findall(r'\b\w+\b', text)  # Extract words using regex

        for word in words:
            update_word_frequency(conn, word)

def main(folder_path):
    """Main function to process all text files in a folder."""
    # Set up the database connection and table
    conn = setup_database()

    # Process each .txt file in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {file_path}")
            process_text_file(conn, file_path)
    
    conn.close()
    print("Word frequency analysis complete.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python word_frequency.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        sys.exit(1)

    main(folder_path)
