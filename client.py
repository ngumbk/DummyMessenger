import asyncio
import aiohttp
import random
import time
#import resource

URL = 'http://127.0.0.1:8000/send_message/'
SENDER_NAMES = ['Andrey', 'Jenya', 'Yulia', 'Igor', 'Nikita', 'Sanya', 'Lera', 'Dima', 'Katya', 'Ilya']


async def make_request(sender, text):
    async with aiohttp.ClientSession() as session:
        data = {"sender": sender,
                "text": text}
        async with session.post(URL, json=data) as response:
            return await response.text()


async def run_multiple_requests():
    # Creating coroutines, containing 100 tasks each
    background_tasks = []
    for _ in range(1):
        group_tasks = set()
        for _ in range(100):
            task = asyncio.create_task(make_request(SENDER_NAMES[random.randint(0, 9)],
                                                    'alo' * random.randint(1, 5)))
            group_tasks.add(task)
            task.add_done_callback(group_tasks.discard) 
        background_tasks.append(group_tasks)
    
    # Executing groups of tasks
    results = []
    for group_task in background_tasks:
        group_results = await asyncio.gather(*group_task)
        for result in group_results:
            print(result, '\n\n')
            results.append(result)

    return results


async def main():
    print('Using 1 server replica')
    start_time = time.time()
    results = await run_multiple_requests()
    print(f'Time for 100 requests in 1 coroutine: {time.time() - start_time} sec.')
    #print(results)

#soft_limit, hard_limit = resource.getrlimit(resource.RLIMIT_NOFILE)
#resource.setrlimit(resource.RLIMIT_NOFILE, (10000, hard_limit))
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
