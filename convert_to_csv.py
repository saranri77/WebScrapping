import pandas as pd
import mysql.connector


conn = mysql.connector.connect(
    user='root',
    password='#Sarajj9636',
    database='LAPTOPS'
)
cursor = conn.cursor()

query = 'SELECT * FROM asus'
cursor.execute(query)

rows = cursor.fetchall()
columns = [col[0] for col in cursor.description]

df = pd.DataFrame(rows, columns=columns)

# Drop rows with null values
df = df.dropna()
df.to_csv('laptops.csv', index=False)

cursor.close()
conn.close()
