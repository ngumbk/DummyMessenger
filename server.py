from fastapi import FastAPI
from pydantic import BaseModel

import mysql.connector
import time


app = FastAPI()

try:
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456'
    )
    print(mydb)

    cursor = mydb.cursor()
    cursor.execute("SHOW DATABASES LIKE 'server_db'")
    if cursor.fetchone() == None:
        # create db
        cursor.execute("CREATE DATABASE server_db")
        cursor.execute("USE server_db")
        cursor.execute("CREATE TABLE Messages ("
                        "message_id int NOT NULL AUTO_INCREMENT,"
                        "sender_name varchar(40),"
                        "message_text varchar(140),"
                        "message_time timestamp,"
                        "PRIMARY KEY (message_id));")
    cursor.close()
    print('DB Created!')
except mysql.connector.Error as err:
    print(err)

class Message(BaseModel):
    name: str
    text: str
    time: str #time.strftime('%Y-%m-%d %H:%M:%S')


# Returns DB connection
@app.get("/")
def read_root():
    return {"Hello": "World",
            "mydb": str(mydb)}



@app.post("/send_message")
def post_message(sender: str, message: str):
    return {"sender_name": Message.name, "message_text": Message.text}
