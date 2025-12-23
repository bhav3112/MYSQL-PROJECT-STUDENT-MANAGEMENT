CREATE DATABASE student_exam_db;
USE student_exam_db;

CREATE TABLE performance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gender VARCHAR(10),
    race_ethnicity VARCHAR(30),
    parental_education VARCHAR(60),
    lunch VARCHAR(20),
    test_prep VARCHAR(20),
    math_score INT,
    reading_score INT,
    writing_score INT
);

