import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Adding some sample data to test search and stats
sample_items = [
    ('Dark Chocolate', 'Rich 70% cocoa bar', 'Dessert', 5),
    ('Milk Chocolate', 'Creamy and sweet', 'Dessert', 4),
    ('Espresso Beans', 'Dark roasted coffee beans', 'Drinks', 5),
    ('Green Tea', 'Organic sencha leaves', 'Drinks', 3),
    ('Sourdough Bread', 'Freshly baked loaf', 'Bakery', 4),
]

cur.executemany("INSERT INTO items (name, description, category, rating) VALUES (?, ?, ?, ?)", sample_items)

connection.commit()
connection.close()
print("Database initialized!")