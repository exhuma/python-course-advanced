# Parallel Execution

This section explains what methods Python offers to run tasks in parallel.

^

## Introduction

Python has several models for parallel code execution:

* Multi-Threading (Module: `threading`)
* Multi-Processing (Module: `multiprocessing`)
* Async I/O (Module: `asyncio`)

Note:

`asyncio` is *not* parallel!
<!-- .element: class="admonition warning" -->

^

## Multithreading & Multiprocessing

Code can be parallelised using different methods:

* Classical subclassing. Starting stopping manually.
* Futures/Promises via "Pools".

Note:

Classical threading/processing is done by subclassing the `Thread` or `Process`
class and implementing a `run()` method. This is a low-level implementaition and
gives a lot of control. It also increases the risk of bugs by implementing it
incorrectly.

A better aproach with is applicable for most use-cases is to use "worker pools"
and submitting jobs to those pools. The common pools for this are
`concurrent.futures.ProcessPoolExecutor` and
`concurrent.futures.ThreadPoolExecutor`).

For multiprocessing, another usful class to spawn workers is
`multiprocessing.Pool`.

^

## The GIL

* Global Interpreter Lock
* Threads hold **one global lock** as long as they do CPU work. The lock is
  released on I/O!
* Problematic when doing CPU-bound concurrency with multiple cores! See
  ([1](http://dabeaz.blogspot.lu/2010/01/python-gil-visualized.html), and
  [2](http://www.dabeaz.com/GIL/gilvis/)).
* Consider using multi-processing instead of multi-threading when needing CPU!

^

## Classical Method Example

```py
from time import sleep
import threading
from random import randint

class MyThread(threading.Thread):

    def run(self):
        for i in range(10):
            print('%s: %3d' % (self.name, i))
            sleep(randint(1, 3))

thread = MyThread()
thread.start()
thread2 = MyThread()
thread2.start()
thread.join()
thread2.join()
```

^

## Futures/Promises Example

```py
import concurrent.futures
import logging
import urllib.request

LOG = logging.getLogger(__name__)
URLS = [
    "http://www.foxnews.com/", "http://www.cnn.com/",
    "http://europe.wsj.com/", "http://www.bbc.co.uk/",
    "http://some-made-up-domain.com/"
]

def load_url(url, timeout):
    "Retrieve a single page and report the URL and contents"

    LOG.info('%r: fetching....', url)
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        output = conn.read()
        LOG.info('%r:  got %d bytes', url, len(output))
        return output
    logging.basicConfig(
        level=logging.INFO, format='LOGGING -> %(thread)s - %(message)s'
    )
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {
            executor.submit(load_url, url, 60): url for url in URLS
        }
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                print('%r page is %d bytes' % (url, len(data)))
```
<!-- .element: class="smallcode" -->

Note:

* Provided by the `concurrent.futures` module.
* Submit tasks to a `concurrent.futures.ProcessPoolExecutor` or a
  `concurrent.futures.ThreadPoolExecutor`.
* Will immediately return promises.
* Consume these promises as you see fit.
* Contains convenience methods like `concurrent.futures.as_completed`
  or `concurrent.futures.wait`.

^

## Async I/O

* Not parallel
* Event-Loop
* Single Threaded

Note:

Using asyncio does **not** mean doing parallel execution! The default asyncio
event-loop *runs in one thread*!

*However:* asyncio makes it possible to suspend code waiting on I/O until the
OS reports that I/O is ready & available. This is done using "selectors"
(\*nix) and "proactors" (Windows).

While I/O is waiting, other code gets a chance to run while still running in
only one thread. This has several advantages:

* No need for synchronisation primitive
* No overhead
* *much* simpler code
* Not subject to the GIL (unless you do threading with ayncio of course).

^

## asyncio example

```py
from asyncio import get_event_loop, sleep, gather

async def fetch(i, sleeptime):
    print(f'Job #{i} is sleeping for {sleeptime}s')
    await sleep(sleeptime)
    print(f'Job #{i} finished')
    return i, sleeptime * 2


async def process(jobs, loop):
    tasks = []
    for i, sleeptime in enumerate(jobs):
        print(f'Adding process #{i}, waiting for {sleeptime}s')
        tasks.append(loop.create_task(fetch(i, sleeptime)))
    result = await gather(*tasks)
    return result

if __name__ == '__main__':
    loop = get_event_loop()
    result = loop.run_until_complete(process([5, 2, 1, 3], loop))
    loop.close()
    for i, jobresult in result:
        print(f'Result for job #{i}: {jobresult}')
```
