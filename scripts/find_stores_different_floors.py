import sqlite3
import re

# Connect to your SQLite database
conn = sqlite3.connect('database/store_data.db')
cursor = conn.cursor()

# Step 1: Select rows with the same store_name that match the pattern for full_address
query = """
SELECT store_name, store_type, full_address
FROM stores
WHERE full_address GLOB '*[0-9]F*'
AND store_name IN (
    SELECT store_name
    FROM stores
    GROUP BY store_name
    HAVING COUNT(*) > 1
)
"""
cursor.execute(query)
results = cursor.fetchall()

# Step 2: Compare full_address fields that match the pattern
# Function to extract numerical parts of an address followed by 'F'
def extract_numeric_with_F(address):
    matches = re.findall(r'(\d+F)', address)
    return matches[0] if matches else ''

# Dictionary to store addresses by store_name
addresses = {}
for store_name, store_type, full_address in results:
    if store_name not in addresses:
        addresses[store_name] = []
    addresses[store_name].append((store_type, full_address))

# Step 3: Find differences that have the numeric pattern followed by 'F'
for store_name, stores in addresses.items():
    if len(stores) > 1:
        for i in range(len(stores)):
            for j in range(i + 1, len(stores)):
                store_type1, addr1 = stores[i]
                store_type2, addr2 = stores[j]
                numF1 = extract_numeric_with_F(addr1)
                numF2 = extract_numeric_with_F(addr2)
                if numF1 != numF2 and all(char.isdigit() or char == 'F' for char in numF1 + numF2):
                    print(f"Store '{store_name}' (Type: {store_type1} & {store_type2}) has the following address differences with numeric pattern 'xF':")
                    print(f"Address 1: {addr1} (Type: {store_type1})")
                    print(f"Address 2: {addr2} (Type: {store_type2})")
                    print()

# Close the connection
conn.close()
