from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import time


class Message(BaseModel):
    sender: str
    text: str

app = FastAPI()

dbconfig = {
  "host": "db_mysql",
  "database": "server_db",
  "user": "db_user",
  "password": "user-password"
}

# Checking DB connection
try:
    init_cnx = mysql.connector.connect(
        host='db_mysql',
        user='db_user',
        password='user-password'
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
        print("Yes, Container is being rebuilt!")
    cursor.close()
    init_cnx.close()
except mysql.connector.Error as err:
    print("On init_cnx:", err)


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


# Get root function, just to check if app is connected to DB
@app.get("/")
async def get_root():
    try:
        check_cnx = mysql.connector.connect(**dbconfig)
        cursor = check_cnx.cursor()
        cursor.execute("SHOW DATABASES LIKE 'server_db'")
        if cursor.fetchone() != None:
            return {"Message": "Database initialized. Table exists"}
        else:
            return {"Message": "Database initialized. Table not exists"}
        
    except Exception as e:
        return {"Database not initialized. Exception raised": e}
    finally:
        check_cnx.close()


@app.post("/send_message/")
async def send_message(message: Message):

    cnx = mysql.connector.connect(**dbconfig)
    cnx.start_transaction()
    try:
        cursor = cnx.cursor()

        # Locking the Messages table
        cursor.execute("LOCK TABLES Messages WRITE")

        # Getting user_messages_count
        cursor.execute("SELECT COUNT(*)"
                       f"FROM Messages WHERE sender_name = '{message.sender}'")
        user_messages_count = cursor.fetchone()[0] + 1

        # Inserting posted data to DB
        cursor.execute("INSERT INTO Messages(sender_name, message_text,"
                                "created_at, user_messages_count) VALUES ("
                                f"'{message.sender}', '{message.text}',"
                                f"\'{time.strftime('%Y-%m-%d')}\',"
                                f"{user_messages_count})")
        
        cnx.commit()

        # Getting 10 last messages
        cursor.execute(
            "SELECT * FROM Messages ORDER BY message_id DESC LIMIT 10")
        last_10_messages = cursor.fetchall()

        return_dict = {i: message_data for i,
                       message_data in enumerate(last_10_messages[::-1])}

        return return_dict
    except Exception as e:
        cnx.rollback()
        print("Error sending message:", e)
        raise
    finally:
        cursor.execute("UNLOCK TABLES")
        cnx.close()
