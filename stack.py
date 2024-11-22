class Stack:
    def __init__(self, name: str = "Default"):
        self.name = name
        self.stack = []

    def append(self, item):
        self.stack.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.stack.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.stack[-1]

    def last(self):
        if self.is_empty():
            return None
        return self.stack[0]

    def is_empty(self):
        return len(self.stack) == 0

    def clear(self):
        self.stack.clear()

    def __str__(self):
        return str(self.stack)
