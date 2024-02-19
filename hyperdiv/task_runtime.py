from concurrent.futures import ThreadPoolExecutor
import asyncio
import threading


class TaskRuntime:
    def __init__(self, pool_max_workers, executor=None):
        self.threadpool = executor or ThreadPoolExecutor(max_workers=pool_max_workers)
        self.ioloop = asyncio.new_event_loop()
        self.thread_futures = []  # Store futures for threadpool tasks

        self.ioloop_thread = threading.Thread(target=self._start_ioloop)
        self.ioloop_thread.start()

    def _start_ioloop(self):
        asyncio.set_event_loop(self.ioloop)
        self.ioloop.run_forever()

    def run_on_ioloop(self, coro):
        asyncio.run_coroutine_threadsafe(coro, self.ioloop)

    def run_in_threadpool(self, fn):
        future = self.threadpool.submit(fn)
        self.thread_futures.append(future)
        self._cleanup_thread_futures()
        return future

    def _cleanup_thread_futures(self):
        # Remove completed futures
        self.thread_futures = [f for f in self.thread_futures if not f.done()]

    def is_empty(self):
        self._cleanup_thread_futures()

        # Check if all threadpool futures are done
        if self.thread_futures:
            return False

        async def check_ioloop_tasks():
            current_task = asyncio.current_task(self.ioloop)
            return not any(
                t != current_task and not t.done()
                for t in asyncio.all_tasks(self.ioloop)
            )

        # Run the check as a coroutine on the event loop
        loop_check_future = asyncio.run_coroutine_threadsafe(
            check_ioloop_tasks(), self.ioloop
        )
        return loop_check_future.result()

    def shutdown(self):
        self.threadpool.shutdown()
        self.ioloop.call_soon_threadsafe(self.ioloop.stop)
