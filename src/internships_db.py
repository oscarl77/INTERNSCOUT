import mysql.connector as mysql

internships_db = mysql.connect(
    host = "localhost",
    user = "oscar",
    password = "Oscar0511",
    database = "internships_db"
)

print(internships_db)