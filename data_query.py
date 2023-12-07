# """循环队列"""
class Data_Query:

    def __init__(self, size):
        self.__size = size
        self.__items = [None] * self.__size
        self.__length = 0
        self.__head = 0

    def is_empty(self):
        return self.__length == 0

    def is_full(self):
        return self.__length == self.__size

    def length(self):
        return self.__length

    def reset(self):
        self.__length = 0
        self.__head = 0

    def push(self, data):
        if self.__length < self.__size:
            idx = (self.__length + self.__head) % self.__size
            self.__items[idx] = data
            self.__length += 1

    def pop(self):  # 弹出队首元素
        if self.is_empty():
            raise ValueError('队列为空')
        res = self.__items[self.__head]
        self.__head = (self.__head + 1) % self.__size
        self.__length -= 1
        return res
