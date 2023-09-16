import numpy as np
import threading
import time
from point import Point
from  container import Container

SIZE = 10000000
THREAD_NUMBER = 24



def is_inside(x: float,y:float)-> bool:
    l = np.sqrt(x*x + y*y)
    return l < 1

def calculate_pi(points):
    inside = 0
    for p in points:
        if is_inside(p.x, p.y):
            inside += 1
    pi = inside / len(points) * 4.0
    return pi

def generate_point():
    p = Point(np.random.random(), np.random.random())
    return p

def run(container):
    points = [generate_point() for i in range(SIZE // THREAD_NUMBER)]
    pi = calculate_pi(points)
    container.pi = pi
    container.event.set()


if __name__ == "__main__":

    t1 = time.time()
    points = [generate_point() for _ in range(SIZE)]
    pi = calculate_pi(points)
    t2 = time.time()
    print(f"Single Threaded: {pi} for {t2 - t1} sec")

    t3 = time.time()
    containers = [Container() for _ in range(THREAD_NUMBER)]
    threads = []

    for container in containers:
        thread = threading.Thread(target=run, args=(container,))
        thread.start()
        threads.append(thread)

    while any(thread.is_alive() for thread in threads):
        pass

    pi = sum(container.pi for container in containers) / THREAD_NUMBER
    t4 = time.time()
    print(f"Multi-Threaded: {pi} for {t4 - t3} sec")
