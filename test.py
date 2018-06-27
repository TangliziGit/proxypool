import queue

class Item:
    def __init__(self, a, b):
        self.a=a
        self.b=b

    def __lt__(self, other):
        return self.a<other.a

    # def __cmp__(self, other):
    #    return self.a<other.a

que=queue.PriorityQueue()
que.put(Item(123, 123))
que.put(Item(12, 12))
print(que.get().a)
