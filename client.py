import asyncio
import aiohttp
import requests
import random
import time
import sys
import json

URLS = ['http://127.0.0.1:8081/send_message/',
        'http://127.0.0.1:8082/send_message/']
SENDER_NAMES = ['Andrey', 'Jenya', 'Yulia', 'Igor', 'Nikita', 'Sanya',
                'Lera', 'Dima', 'Katya', 'Ilya']


async def make_request(sender, text, index):
    async with aiohttp.ClientSession() as session:
        data = {"sender": sender,
                "text": text}
        try:
            async with session.post(random.choice(URLS), json=data) as response:
                response_text = await response.text()
                return index, response_text
        except aiohttp.ClientError as e:
            error_message = f"Error occurred for request {index}: {str(e)}"
            return index, error_message


async def make_100_requests(start_index):
    group_tasks = []
    for i in range(start_index, start_index + 100):
        sender = random.choice(SENDER_NAMES)
        text = 'alo' * random.randint(1, 5)
        task = asyncio.create_task(make_request(sender, text, i))
        group_tasks.append(task)
        # done_callback is commented, since it causes responses deletion 
        #task.add_done_callback(group_tasks.remove)
    return group_tasks


async def run_multiple_requests():
    # Creating coroutines, containing 100 tasks each
    coroutines = []
    start_index = 1
    for _ in range(50):
        group_tasks = await make_100_requests(start_index)
        coroutines.append(group_tasks)
        start_index += 100

    # Executing groups of tasks
    results = {}
    for group_task in coroutines:
        group_results = await asyncio.gather(*group_task)
        for index, response in group_results:
            results[index] = response if response is not None else "No response"

    return results


async def check_server_availability(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Server is accessible.", end='\n\n')
    except requests.exceptions.RequestException as e:
        print("Server is not accessible.", e)
        sys.exit()


def save_responses_to_file(responses):
    with open('responses.json', 'w') as file:
        json.dump(responses, file)


async def main():
    print('Checking server 1:')
    await check_server_availability('http://127.0.0.1:8081/')
    print('Checking server 2:')
    await check_server_availability('http://127.0.0.1:8082/')
    print('Start testing. Please, wait.')
    
    # Testing 5000 requests from 50 coros
    start_time = time.time()
    responses = await run_multiple_requests()
    time_100 = time.time() - start_time
    print(f'Time for 5000 requests in 50 coroutines: {time_100} sec.')
    
    # Testing 1 request & Bandwidth
    start_time = time.time()
    requests.post(URLS[0], json={"sender": random.choice(SENDER_NAMES),
                             "text": "single request here"})
    time_1 = time.time() - start_time
    print(f'Time for 1 request: {time_1} sec.'
          f'\nBandwidth: {5000 / time_100} requests/sec.')
    
    save_responses_to_file(responses)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
