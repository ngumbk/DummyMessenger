import requests

URL = 'http://127.0.0.1:8000/send_message/'

requests.post(url=URL, json={"sender": "Andrey",
                             "text": "Privet Vsem"})
for i in range(1, 5):
    requests.post(url=URL, json={"sender": "Andrey",
                                "text": "Alo" * i})
    requests.post(url=URL, json={"sender": "Jenya",
                                "text": "Govorite ..." * i})
requests.post(url=URL, json={"sender": "Sanya",
                            "text": "Menya opyat zachmorili :("})
    

