import sqlite3
from bs4 import BeautifulSoup
from tqdm import tqdm

# Connect to the SQLite database (creates a new database if it does not exist)
conn = sqlite3.connect('database/store_data.db')
cursor = conn.cursor()

# Create a table to store the store information
cursor.execute('''CREATE TABLE IF NOT EXISTS stores
                (store_name TEXT, prefecture_name TEXT, full_address TEXT, phone_number TEXT)''')

progress = tqdm(total=111, desc="Processing", unit="step")

for step_num in range(1, 111):  # Loop through steps 1 to 110
    progress.update()

    file_path = f'html_data/step_{step_num}.html'
    try:
        with open(file_path, 'r') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        result_items = soup.find_all('section', class_='result-item')

        for item in result_items:
            store_name = item.find('span').text.strip()
            address = item.find('p', class_='result-item_address').text.strip()
            prefecture_name = address.split()[0]
            full_address = ''.join(address.split()[1:])
            phone_number = item.find('dl', class_='result-item_tel').find('a').text.strip()

            # Check if the store with the same name and phone number already exists
            cursor.execute('SELECT * FROM stores WHERE store_name=? AND phone_number=?',
                           (store_name, phone_number))
            existing_record = cursor.fetchone()

            if existing_record is None:  # If no match found, insert the store information
                cursor.execute('INSERT INTO stores VALUES (?, ?, ?, ?)',
                               (store_name, prefecture_name, full_address, phone_number))
                conn.commit()

    except FileNotFoundError:
        print(f"File {file_path} not found. Skipping...")

# Close the database connection
conn.close()
progress.update()
progress.close()
