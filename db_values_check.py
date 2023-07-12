import mysql.connector


SENDER_NAMES = ['Andrey', 'Jenya', 'Yulia', 'Igor', 'Nikita', 'Sanya',
                'Lera', 'Dima', 'Katya', 'Ilya']
dbconfig = {
  "host": "localhost",
  "database": "server_db",
  "user": "db_user",
  "password": "user-password"
}


# DB I/O function
def execute_db_query(query, cursor_buffered=False):
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


def check_common_entries():
    entries_count = execute_db_query("SELECT COUNT(*) FROM Messages;")[0][0]
    print('Total DB entries:', entries_count)
    unique_id_count = execute_db_query(
        "SELECT COUNT(DISTINCT message_id) AS unique_ids FROM Messages;")[0][0]
    print('Total entries with unique message_id:', unique_id_count)


def check_sender_entries(sender_name):
    entries_count = execute_db_query("SELECT COUNT(*) AS msgs_from_user "
                                      "FROM Messages WHERE sender_name "
                                      f"= '{sender_name}';")[0][0]
    entries_with_unique_msg_count = execute_db_query(
        "SELECT COUNT(DISTINCT sender_name, user_messages_count) AS "
        "msgs_with_unique_n FROM Messages "
        f"WHERE sender_name = '{sender_name}';")[0][0]
    print("All sender's entries count:", entries_count)
    print("Unique user_messages_count entries count:",
          entries_with_unique_msg_count)
    if entries_count == entries_with_unique_msg_count:
        print("These stack good")
    else:
        print("Whoops, numbers don't match")


def check_doubles():
    sender_name = input("Which sender you want to check for doubles?\n")
    doubles = execute_db_query("SELECT message_id, sender_name, created_at,"
                        "user_messages_count FROM Messages WHERE sender_name = "
                        f"'{sender_name}' AND user_messages_count IN ("
                        "SELECT user_messages_count FROM Messages WHERE " 
                        f"sender_name = '{sender_name}' GROUP BY "
                        "user_messages_count HAVING COUNT(*) > 1);")
    print('  id  | sender |           date           | user_msg_count')
    print(*doubles, sep='\n')


def main():
    print('CHECKING COMMON ENTRIES\n' + '-' * 24)
    check_common_entries()
    print('-' * 24, end='\n\n')

    print('CHECKING ENTRIES FOR EACH SENDER\'S NAME\n' + '-' * 24)
    for name in SENDER_NAMES:
        print(f'Entries for sender {name}:')
        check_sender_entries(name)
        print('.' * 24, end='\n\n')
    
    while True:
        response = input('Wish to check doubles\' ids? (Y/N)\n')
        if response in 'Yy':
            check_doubles()
        elif response in 'Nn':
            print('Okay. Bye!')
            break
        else:
            print('No such option as', response, end='\n\n')


if __name__ == '__main__':
    main()
