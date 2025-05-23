import requests
import time
from datetime import datetime


def timer(f: callable, *args, **kwargs):
    print(args)
    print(kwargs)

    now = time.time_ns()
    f()
    print(int(time.time_ns() - now) / 1e9)


def timer_d(f: callable):
    def inner():
        now = time.time_ns()
        f()
        elapsed = (time.time_ns() - now) / 1e9
        return elapsed

    return inner


@timer_d
def fast():
    print("l")


def medium():
    res = requests.get("https://google.com/")
    print(res.content)


def slow():
    counter = 0
    for i in range(10000):
        for j in range(10000):
            counter += 1

    print(counter)


def main():
    # print(type(timer_d))
    # print(type(timer_d(fast)))
    # print(timer_d(fast)())
    # timed_fast = timer_d(fast)
    # print(timed_fast())
    print(fast())*

    # t = 1, 2
    # print(t)
    # print(*t)
    # timer(fast, "hi", 7, x=3, y=True)
    # timer(medium)
    # timer(slow)


if __name__ == '__main__':
    main()
