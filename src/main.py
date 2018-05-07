
def method1():
    from threading import Thread
    import sys
    from queue import Queue
    import urllib.request
    import time
    timeout = 30
    concurrent = 200

    def doWork():
        while True:
            url = q.get()
            jsonResponse = getStatus(url)
            #print(jsonResponse)
            #doSomethingWithResult(status, url)
            q.task_done()

    def getStatus(url):
        try:
            conn = urllib.request.urlopen(url, timeout = timeout)
            jsonResponse = conn.readline().decode("utf-8")
            conn.close()
            return jsonResponse
            #return res.status, ourl
        except:
            return "error", url

    def doSomethingWithResult(status, url):
        print(status, url)

    q = Queue(concurrent)
    startTime = time.time()
    for i in range(concurrent):
        t = Thread(target=doWork)
        t.daemon = True
        t.start()
    try:
        [q.put("https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid=" +
            str(i) + "&format=json") for i in range(1, 500)]
        q.join()
    except KeyboardInterrupt:
        sys.exit(1)
    endTime = time.time()
    print(endTime - startTime)








def method2():
    import time
    import concurrent.futures
    import urllib.request

    # URLS = ['http://www.foxnews.com/',
    #         'http://www.cnn.com/',
    #         'http://europe.wsj.com/',
    #         'http://www.bbc.co.uk/',
    #         'http://some-made-up-domain.com/']

    urls = ["https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid=" +
            str(i) + "&format=json" for i in range(1, 500)]

    # Retrieve a single page and report the url and contents
    def load_url(url: str, timeout: int):
        conn = urllib.request.urlopen(url, timeout=timeout)
        return conn.readline().decode("utf-8")


    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(load_url, url, 30): url for url in urls}
        startTime = time.time()
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                #print(data)
            except Exception as exception:
                print('%r generated an exception: %s' % (url, exception))
            # else:
            #     print('%r page is %d bytes' % (url, len(data)))
    endTime = time.time()
    print(endTime - startTime)





def method3():
    # modified fetch function with semaphore
    import random
    import asyncio
    from aiohttp import ClientSession
    import time

    async def fetch(url, session):
        async with session.get(url) as response:
            delay = response.headers.get("DELAY")
            date = response.headers.get("DATE")
            #print("{}:{} with delay {}".format(date, response.url, delay))
            return await response.read()


    async def bound_fetch(sem, url, session):
        # Getter function with semaphore.
        async with sem:
            await fetch(url, session)


    async def run(r):
        url = "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid={}&format=json"
        #url = "http://localhost:8080/{}"
        tasks = []
        # create instance of Semaphore
        sem = asyncio.Semaphore(1000)

        # Create client session that will ensure we dont open new connection
        # per each request.
        async with ClientSession() as session:
            for i in range(r):
                # pass Semaphore and session to every GET request
                task = asyncio.ensure_future(bound_fetch(sem, url.format(i), session))
                tasks.append(task)

            responses = asyncio.gather(*tasks)
            await responses

    number = 500
    loop = asyncio.get_event_loop()

    future = asyncio.ensure_future(run(number))
    startTime = time.time()
    loop.run_until_complete(future)
    print(time.time() - startTime)

method3()
