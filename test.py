import mysql.connector
import json


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


def check_db_common_entries():
    entries_count = execute_db_query("SELECT COUNT(*) FROM Messages;")[0][0]
    unique_id_count = execute_db_query(
        "SELECT COUNT(DISTINCT message_id) AS unique_ids FROM Messages;")[0][0]
    if entries_count == unique_id_count:
        print('Total DB entries match!')
    else:
        print('Total DB entries don\'t match!')
        print('Total DB entries:', entries_count)
        print('Total entries with unique message_id:', unique_id_count)


def check_db_sender_entries(sender_name):
    entries_count = execute_db_query("SELECT COUNT(*) AS msgs_from_user "
                                      "FROM Messages WHERE sender_name "
                                      f"= '{sender_name}';")[0][0]
    entries_with_unique_msg_count = execute_db_query(
        "SELECT COUNT(DISTINCT sender_name, user_messages_count) AS "
        "msgs_with_unique_n FROM Messages "
        f"WHERE sender_name = '{sender_name}';")[0][0]
    if entries_count == entries_with_unique_msg_count:
        return True
    else:
        print('.' * 24)
        print(f"Numbers don't match for {sender_name}!\n"
              "Total entries/Entries with unique user_msg_count: "
              f"{entries_count}/{entries_with_unique_msg_count}")
        print('.' * 24, end='\n\n')
        return False


def check_db_doubles():
    sender_name = input("Which sender you want to check for doubles?\n")
    doubles = execute_db_query("SELECT message_id, sender_name, created_at,"
                        "user_messages_count FROM Messages WHERE sender_name = "
                        f"'{sender_name}' AND user_messages_count IN ("
                        "SELECT user_messages_count FROM Messages WHERE " 
                        f"sender_name = '{sender_name}' GROUP BY "
                        "user_messages_count HAVING COUNT(*) > 1);")
    print('  id  | sender |           date           | user_msg_count')
    print(*doubles, sep='\n')


def check_id_sequence_in_responses():
    try:
        with open('responses.json') as file:
            data = json.load(file)
            wrong_sequences_ids = []

            for response_key in data:
                # print(response_key, end='///')
                id_sequence = []
                for msg_key in data[response_key]:
                    if str.isnumeric(msg_key):
                        id_sequence.append(data[response_key][msg_key][0])
                # print(id_sequence)

                first_n = id_sequence[0]
                normal_sequence = [first_n + i for i in range(len(id_sequence))]
                # print(key, end='*///')
                # print(normal_sequence)

                if id_sequence != normal_sequence:
                    wrong_sequences_ids.append(response_key)

            if len(wrong_sequences_ids) == 0:
                print('All ID sequences are ok!')
            else:
                print('Some ID sequences are not ok! '
                      'Those sequences\' IDs:', wrong_sequences_ids)
                
            return None
    except TypeError as e:
        print('Exception using json file:', e)
        return None


def check_response_last_msg():
    try:
        with open('responses.json') as file:
            data = json.load(file)
            wrong_responses_ids = []
            
            for response_key in data:
                ids_sequence = [msg_key for msg_key in data[response_key]]
                last_n = ids_sequence[-2]

                message_sent = data[response_key]['Message_sent'][0]
                last_message_in_response = data[response_key][last_n][0]
                if last_message_in_response != message_sent:
                    wrong_responses_ids.append(response_key)
            if len(wrong_responses_ids) == 0:
                print('All last messages in responses are ok!')
            else:
                print('Some last messages in responses are not ok! '
                      'Those responses\' IDs:', wrong_responses_ids)
                
            return None
    except TypeError as e:
        print('Exception using json file:', e)
        return None


def main():
    print('\nCHECKING RESPONSE ID SEQUENCES\n' + '-' * 24)
    check_id_sequence_in_responses()
    print('-' * 24, end='\n\n')
    
    print('CHECKING THAT SENT MSG IS THE LAST IN THE RESPONSE\n' + '-' * 24)
    check_response_last_msg()
    print('-' * 24, end='\n\n')

    print('COMMON DB DATA\n' + '-' * 24)
    check_db_common_entries()
    print('-' * 24, end='\n\n')

    print('CHECKING ENTRIES FOR EACH SENDER\'S NAME\n' + '-' * 24)
    names_check = []
    for name in SENDER_NAMES:
        res = check_db_sender_entries(name)
        names_check.append(res)
    if names_check == [True for _ in range(10)]:
        print('All senders have correct msgs counters!')
        print('-' * 24, end='\n\n')
    else:
        print('Some senders have incorrect msgs counters! Check above.')
        print('-' * 24, end='\n\n')
        while True:
            response = input('Want to check doubles\' ids? (Y/N)\n')
            if response in 'Yy':
                check_db_doubles()
            elif response in 'Nn':
                print('Okay. Bye!')
                break
            else:
                print('No such option as', response, end='\n\n')


if __name__ == '__main__':
    main()
