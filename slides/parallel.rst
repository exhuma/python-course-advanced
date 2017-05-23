Parallel Execution
==================

This section explains what methods Python offers to run tasks in parallel.


Introduction
------------

Python has several models for parallel code execution:

* Classical subclassing and starting stopping manually.
* Futures (Promises)
* Explicit coroutines via ``async``/``await`` (since Python 3.5)

Both the "classical" and "futures" approach can be run in multiple processes or
threads. Coroutines are primarily used for asynchronous I/O like network or
disk access which is very well supported in :py:mod:`asyncio`. Coroutines *can*
of course be used for other kinds of parallel execution.


The GIL
-------

* Global Interpreter Lock
* Threads hold **one global lock** as long as they do CPU work. The lock is
  released on I/O!
* Problematic when doing CPU-bound concurrency with multiple cores! See (`1
  <http://dabeaz.blogspot.lu/2010/01/python-gil-visualized.html>`_, and `2
  <http://www.dabeaz.com/GIL/gilvis/>`_).
* Consider using multi-processing instead of multi-threading when needing CPU!


Classical Method
----------------

* Provided by the two modules :py:mod:`threading` and
  :py:mod:`multiprocessing`.
* Subclasing either :py:class:`threading.Thread` or
  :py:mod:`multiprocessing.Process`.

.. nextslide::
    :increment:

.. code-block:: python

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


Futures/Promises
----------------

* Provided by the :py:mod:`concurrent.futures` module.
* Submit tasks to a :py:class:`~concurrent.futures.ProcessPoolExecutor` or a
  :py:class:`~concurrent.futures.ThreadPoolExecutor`.
* Will immediately return promises.
* Consume these promises as you see fit.
* Contains convenience methods like :py:func:`~concurrent.futures.as_completed`
  or :py:func:`~concurrent.futures.wait`.

.. nextslide::
    :increment:

.. code-block:: python
    :class: smaller

    import concurrent.futures
    import logging
    import urllib.request

    LOG = logging.getLogger(__name__)
    URLS = ['http://www.foxnews.com/', 'http://www.cnn.com/',
            'http://europe.wsj.com/', 'http://www.bbc.co.uk/',
            'http://some-made-up-domain.com/']

    # Retrieve a single page and report the URL and contents
    def load_url(url, timeout):
        LOG.info('%r: fetching....', url)
        with urllib.request.urlopen(url, timeout=timeout) as conn:
            output = conn.read()
            LOG.info('%r:  got %d bytes', url, len(output))
            return output

    # continuing on next slide...

.. nextslide::
    :increment:

.. code-block:: python
    :class: smaller

    # ... continued from previous slide

    logging.basicConfig(level=logging.INFO,
                        format='LOGGING -> %(thread)s - %(message)s')
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                print('%r page is %d bytes' % (url, len(data)))
