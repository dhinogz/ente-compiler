class Stack:
    def __init__(self, name: str = "Default"):
        self.name = name
        self.stack = []

    def push(self, item: str | int | dict) -> None:
        self.stack.append(item)

    def pop(self) -> str | int | dict | None:
        if self.is_empty():
            return None
        return self.stack.pop()

    def peek(self) -> str | int | dict | None:
        if self.is_empty():
            return None
        return self.stack[-1]

    def last(self) -> str | int | dict | None:
        if self.is_empty():
            return None
        return self.stack[0]

    def is_empty(self) -> bool:
        return len(self.stack) == 0

    def clear(self) -> None:
        self.stack.clear()

    def __str__(self) -> str:
        return str(self.stack)
