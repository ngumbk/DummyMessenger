from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import time


class Message(BaseModel):
    sender: str
    text: str

app = FastAPI()

dbconfig = {
  "database": "server_db",
  "user": "root",
  "password": "root"
}

# Checking DB connection
try:
    init_cnx = mysql.connector.connect(
        host='db_mysql',
        port='33060',
        user='root',
        password='root'
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


# DB I/O function
async def execute_db_query(query, cursor_buffered=False):
    cnx = mysql.connector.connect(**dbconfig)
    try:
        cursor = cnx.cursor(buffered=cursor_buffered)
        cursor.execute("USE server_db")
        cursor.execute(query)
        result = cursor.fetchall()
        cnx.commit()
        return result
    except Exception as e:
        print("Error executing query:", e)
    finally:
        if cnx:
            cnx.close()


@app.get("/")
async def get_root():
    try:
        entries_count = await execute_db_query("SELECT COUNT (*) FROM Messages", cursor_buffered=True)
        return {"Messages entries": entries_count[0][0]}
    except Exception as e:
        return {"Error": e}


@app.post("/send_message/")
async def send_message(message: Message):

    # Blocking DB table
    await execute_db_query("LOCK TABLES Messages WRITE")

    # Getting user_messages_count
    user_messages_count = await execute_db_query(f"SELECT COUNT(*) FROM Messages WHERE sender_name = '{message.sender}'")
    user_messages_count = user_messages_count[0][0] + 1

    # Inserting posted data to DB
    await execute_db_query("INSERT INTO Messages(sender_name, message_text, created_at, user_messages_count) "
                        f"VALUES ('{message.sender}', '{message.text}', \'{time.strftime('%Y-%m-%d')}\', {user_messages_count})")

    # Getting 10 last messages
    entries_count = await execute_db_query("SELECT COUNT(*) FROM Messages", cursor_buffered=True)
    entries_count = entries_count[0][0]

    last_10_messages = await execute_db_query("SELECT * FROM Messages ORDER BY message_id DESC LIMIT 10")
    return_dict = {}
    if entries_count < 10:
        for i in range(entries_count):
            return_dict[i] = last_10_messages[i]
    else:
        for i in range(10):
            return_dict[i] = last_10_messages[i]
    reversed_dict = {}
    dict_len = len(return_dict)
    for i in range(dict_len):
        reversed_dict[i] = return_dict[dict_len - 1 - i]
    return_dict = reversed_dict

    await execute_db_query("UNLOCK TABLES")
    return return_dict
