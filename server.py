from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import time


class Message(BaseModel):
    sender: str
    text: str
    created_at: str | None = None

app = FastAPI()

dbconfig = {
  "database": "server_db",
  "user": "root",
  "password": "123456"
}

# Checking DB connection
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
                        "message_id INT NOT NULL AUTO_INCREMENT,"
                        "sender_name VARCHAR(32),"
                        "message_text VARCHAR(64),"
                        "created_at DATE,"
                        "user_messages_count INT,"
                        "PRIMARY KEY (message_id));")
        print('DB Created!')
    cursor.close()
    init_cnx.close()
except mysql.connector.Error as err:
    print(err)


@app.post("/send_message/")
async def send_message(message: Message):

    # Inserting posted data to DB
    cnx = mysql.connector.connect(**dbconfig)
    cursor = cnx.cursor()
    cursor.execute("USE server_db")
    cursor.execute("INSERT INTO Messages(sender_name, message_text, created_at) "
                   f"VALUES ('{message.sender}', '{message.text}', \'{time.strftime('%Y-%m-%d')}\')")
    cnx.commit()
    cursor.close()

    # Getting 10 last messages
    cursor = cnx.cursor(buffered=True)
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
    reversed_dict = {}
    dict_len = len(return_dict)
    for i in range(dict_len):
        reversed_dict[i] = return_dict[dict_len - 1 - i]
    return_dict = reversed_dict

    # Adding message_per_user count to dict returned
    cursor.execute(f"SELECT COUNT(*) FROM Messages WHERE sender_name = '{None}'")

    cursor.close()
    cnx.close()
    return return_dict
