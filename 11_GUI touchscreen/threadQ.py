import threading
import time


class ThreadedQueue:
    def __init__(self, items=None):
        self.items = items or []

    def enqueue(self, item):
        """Add an item to the end of the queue."""
        self.items.append(item)

    def enqueue_dict(self, items_dict:dict):
        """Add items from a dictionary to the end of the queue."""
        for item in items_dict.values():
            self.items.append(item)

    def dequeue(self):
        """Remove and return the first item from the queue."""
        if not self.is_empty():
            return self.items.pop(0)
        else:
            raise IndexError("Cannot dequeue from an empty queue")

    def is_empty(self):
        """Check if the queue is empty."""
        return len(self.items) == 0

    def size(self):
        """Return the number of items in the queue."""
        return len(self.items)

    def procQ(self):
        """Process each item in the queue by calling them in a new thread."""
        threads = []
        for item in self.items:
            t = threading.Thread(target=item)
            threads.append(t)
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

    def testfunc(self):
        for i in range(10):
            print(i)
            time.sleep(1)


if __name__ == "__main__":
    Q = ThreadedQueue()

