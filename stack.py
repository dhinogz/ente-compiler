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

    def items(self):
        return self.stack

    def first(self):
        if self.stack:
            return self.stack[0]
        else:
            return None

    def __str__(self):
        return str(self.stack)

    def __iter__(self):
        return iter(self.stack)

    def __bool__(self):
        return not self.is_empty()

    def __len__(self):
        return len(self.stack)

    def __reversed__(self):
        return reversed(self.stack)
