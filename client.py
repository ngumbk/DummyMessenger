import asyncio
import aiohttp
import requests
import random
import time
import sys

URLS = ['http://127.0.0.1:8081/send_message/',
        'http://127.0.0.1:8082/send_message/'] 
SENDER_NAMES = ['Andrey', 'Jenya', 'Yulia', 'Igor', 'Nikita', 'Sanya',
                'Lera', 'Dima', 'Katya', 'Ilya']


async def make_request(sender, text):
    async with aiohttp.ClientSession() as session:
        data = {"sender": sender,
                "text": text}
        async with session.post(random.choice(URLS), json=data) as response:
            return await response.text()


async def make_100_requests():
    group_tasks = set()
    for _ in range(100):
        task = asyncio.create_task(make_request(random.choice(SENDER_NAMES),
                                                'alo' * random.randint(1, 5)))
        group_tasks.add(task)
        task.add_done_callback(group_tasks.discard) 
    return group_tasks


async def run_multiple_requests():
    # Creating coroutines, containing 100 tasks each
    coroutines = []
    for _ in range(50):
        group_tasks = await make_100_requests()
        coroutines.append(group_tasks)
    
    # Executing groups of tasks
    results = []
    for group_task in coroutines:
        group_results = await asyncio.gather(*group_task)
        results.extend(group_results)

    return results


async def check_server_availability(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Server is accessible.", end='\n\n')
    except requests.exceptions.RequestException as e:
        print("Server is not accessible.", e)
        sys.exit()


async def main():
    print('Checking server 1:')
    await check_server_availability('http://127.0.0.1:8081/')
    print('Checking server 2:')
    await check_server_availability('http://127.0.0.1:8082/')
    print('Start testing. Please, wait.')
    
    # Testing 5000 requests from 50 coros
    start_time = time.time()
    await run_multiple_requests()
    time_100 = time.time() - start_time
    print(f'Time for 5000 requests in 50 coroutines: {time_100} sec.')
    
    # Testing 1 request & Bandwidth
    start_time = time.time()
    requests.post(URLS[0], json={"sender": random.choice(SENDER_NAMES),
                             "text": 'alo' * random.randint(1, 5)})
    time_1 = time.time() - start_time
    print(f'Time for 1 request: {time_1} sec.'
          f'\nBandwidth: {5000 / time_100} requests/sec.')


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
