import threading


class Container:
    def __init__(self):
        self.pi = 0
        self.event = threading.Event()