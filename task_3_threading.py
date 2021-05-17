import threading
from threading import Thread


class ThreadCounter():

    def __init__(self, count_value=0):
        self.count_value = count_value
        self.thread_lock = threading.Lock()

    def function(self, arg):
        for _ in range(arg):
            with self.thread_lock:
                self.count_value += 1

    def thread_count(self, threads_num):
        threads = []
        for i in range(threads_num):
            thread = Thread(target=self.function, args=(1000000,))
            threads.append(thread)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        print("----------------------", self.count_value)


if __name__ == '__main__':
    ThreadCounter().thread_count(5)
