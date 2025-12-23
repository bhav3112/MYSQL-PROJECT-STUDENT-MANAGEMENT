import csv
from db_connection import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM performance")
rows = cursor.fetchall()

headers = [
    "id","gender","race","parent_education",
    "lunch","prep","math","reading","writing"
]

with open("exported_student_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

conn.close()
print("Data exported successfully")
