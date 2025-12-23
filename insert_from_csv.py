import csv
from db_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

with open("StudentsPerformance.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute("""
            INSERT INTO performance
            (gender, race_ethnicity, parental_education, lunch,
             test_prep, math_score, reading_score, writing_score)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            row['gender'],
            row['race/ethnicity'],
            row['parental level of education'],
            row['lunch'],
            row['test preparation course'],
            row['math score'],
            row['reading score'],
            row['writing score']
        ))

conn.commit()
conn.close()
print("CSV imported successfully")
