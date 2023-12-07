"""
@Time    : 2023-11-08 11:43
@Author  : BEACON
@File    : 队列_链表.py
"""

'''用链表实现队列'''


# 定义结点类
class Node:
    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node


class Queue:
    """
    链表的第一个元素是队列的头部，链表的最后一个元素是对列的尾部
    """

    def __init__(self, size):
        self.head = None
        self.rear = None
        self.length = 0
        self.size = size

    def is_empty(self):
        return self.length == 0

    def length(self):
        return self.length

    def push(self, data):
        """
        添加一个元素data到队列尾部
        创建一个新的结点
        将新的结点添加到链表的尾部（链表的尾部既队列的尾部）
            将原来的尾结点的next属性指向新的结点
            将队列的rear（原来的尾结点）属性指向新的结点
        队列长度加1
        特殊情况下：
        如果链表为空
        那么就是添加到链表的头部  具体操作如下：
        1.将队列的head属性指向新的结点
        2.将队列的rear属性指向新的结点 （因为在空的队列中台添加一个对象那么这个对象既是队首又是队尾）
        """
        if self.length == self.size:
            raise ValueError('队列已经满了')
        node = Node(data)
        if self.is_empty():
            self.head = node
            self.rear = node
        else:
            self.rear.next = node  # 将原来的尾结点的next属性指向新的结点
            self.rear = node  # 将队列的rear（原来的尾结点）属性指向新的结点
        self.length += 1

    def pop(self):
        """抛出队首元素也就是链表的第一个结点"""
        '''
        创建一个变量指向头节点(用于后续的返回)
        将链表的head属性指向原来头节点的下一个结点
        '''
        if self.is_empty():
            raise ValueError('队列为空')
        value = self.head.data
        if self.length == 1:
            self.head = None
            self.rear = None
            # print(f'队列的头部结点是{self.rear}')
        else:
            self.head = self.head.next
            self.length -= 1
        return value

    def peek(self):
        if self.is_empty():
            raise ValueError('队列为空')
        return self.head.data


if __name__ == '__main__':
    queue = Queue(3)
    queue.push(1)
    queue.push(2)
    queue.push(3)
    print(queue.pop())
    queue.push(4)
    print(queue.peek())
    print(queue.pop())
    print(queue.pop())
    print(queue.pop())
