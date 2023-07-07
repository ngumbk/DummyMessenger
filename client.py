import asyncio
import aiohttp
import requests
import random
import time
#import resource

URLS = ['http://127.0.0.1:8081/send_message/', 'http://127.0.0.1:8082/send_message/'], 
SENDER_NAMES = ['Andrey', 'Jenya', 'Yulia', 'Igor', 'Nikita', 'Sanya', 'Lera', 'Dima', 'Katya', 'Ilya']


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
    for _ in range(1):
        group_tasks = await make_100_requests()
        coroutines.append(group_tasks)
    
    # Executing groups of tasks
    results = []
    for group_task in coroutines:
        group_results = await asyncio.gather(*group_task)
        results.extend(group_results)

    return results


async def main():
    print('Using 1 server replica')

    # Testing 100 requests from one coro
    start_time = time.time()
    await run_multiple_requests()
    time_100 = time.time() - start_time
    print(f'Time for 100 requests in 1 coroutine: {time_100} sec.')
    
    # Testing 1 request & Bandwidth
    start_time = time.time()
    requests.post(URLS[0], json={"sender": random.choice(SENDER_NAMES),
                             "text": 'alo' * random.randint(1, 5)})
    time_1 = time.time() - start_time
    print(f'Time for 1 request: {time_1} sec.\nBandwidth: {100 / time_100} requests/sec.')

#soft_limit, hard_limit = resource.getrlimit(resource.RLIMIT_NOFILE)
#resource.setrlimit(resource.RLIMIT_NOFILE, (10000, hard_limit))
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
