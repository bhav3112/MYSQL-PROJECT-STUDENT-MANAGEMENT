import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bhav@321",
        database="student_exam_db"
    )
