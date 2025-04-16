import sqlite3
import csv

# Connect to SQLite database
connection = sqlite3.connect('database.db')

# Create a cursor object
cursor = connection.cursor()

# Create the CustomerData table
table_info = """
CREATE TABLE IF NOT EXISTS CustomerData(
    CustomerID TEXT PRIMARY KEY,
    Name TEXT,
    Segment TEXT,
    Country TEXT,
    City TEXT
);
"""
cursor.execute(table_info)

# Path to the CSV file
csv_file_path = r'C:\Users\singh\Downloads\Customer Data.csv'

# Insert records from the CSV file into the table
with open(csv_file_path, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        cursor.execute('''
            INSERT OR IGNORE INTO CustomerData (CustomerID, Name, Segment, Country, City)
            VALUES (?, ?, ?, ?, ?)
        ''', row)

# Display the records in the CustomerData table
print("The records in the CustomerData table are:")

data = cursor.execute('''SELECT * FROM CustomerData''')

for row in data:
    print(row)

# Close the connection
connection.commit()
connection.close()