import sqlite3

conn = sqlite3.connect('dish.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS dish(
        id INTEGER PRIMARY KEY,
        dish_name TEXT,
        price INTEGER,
        quantity INTEGER)''')

dishes = [
    ('Misal pav',200,10),
    ('Dhokla',100,10),
    ('Pongal',300,10)
]

for dish in dishes:
    cursor.execute('INSERT INTO dish (dish_name,price,quantity) VALUES (?,?,?)',dish)
    
conn.commit()
conn.close()