import threading

a = 0
r_lock = threading.RLock()


def function(arg):
    global a
    with r_lock:
        for _ in range(arg):
            a += 1


def main():
    threads = []
    for i in range(5):
        thread = threading.Thread(target=function, args=(1000000,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print("----------------------", a)


main()
