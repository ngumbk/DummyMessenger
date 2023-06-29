from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector


class Message(BaseModel):
    name: str
    text: str

app = FastAPI()

dbconfig = {
  "database": "server_db",
  "user": "root",
  "password": "123456"
}

try:
    init_cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456'
    )
    cursor = init_cnx.cursor()
    cursor.execute("SHOW DATABASES LIKE 'server_db'")
    if cursor.fetchone() == None:
        # Create DB in case one doesn't exist
        cursor.execute("CREATE DATABASE server_db")
        cursor.execute("USE server_db")
        cursor.execute("CREATE TABLE Messages ("
                        "message_id int NOT NULL AUTO_INCREMENT,"
                        "sender_name varchar(32),"
                        "message_text varchar(64),"
                        "PRIMARY KEY (message_id));")
        print('DB Created!')
    cursor.close()
    cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool",
                                                          pool_size=3,
                                                          **dbconfig)
except mysql.connector.Error as err:
    print(err)


@app.post("/send_message/")
async def send_message(message: Message):
    cnx1 = cnxpool.get_connection()
    cursor = cnx1.cursor()
    cursor.execute("USE server_db")
    cursor.execute("INSERT INTO Messages(sender_name, message_text) "
                   f"VALUES ('{message.name}', '{message.text}')")
    cnx1.commit()
    cursor.close()
    cnx1.close()

    # Getting last 10 messages
    cnx2 = cnxpool.get_connection()
    cursor = cnx2.cursor()
    cursor.execute("SELECT COUNT(*) FROM Messages")
    entries_count = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM Messages ORDER BY message_id DESC LIMIT 10")
    return_dict = {}
    if entries_count < 10:
        for i in range(entries_count):
            return_dict[i] = cursor.fetchone()
    else:
        for i in range(10):
            return_dict[i] = cursor.fetchone()
    print(*return_dict.items(), sep='\n')
    reversed_dict = {}
    for i in range(10):
        reversed_dict[i] = return_dict[9 - i]
    return reversed_dict
