import sys

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.length = 0

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.length += 1

    def prepend(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        self.length += 1

    def delete(self, value):
        if self.head is None:
            return False
        if self.head.value == value:
            self.head = self.head.next
            self.length -= 1
            return True
        current = self.head
        while current.next is not None:
            if current.next.value == value:
                current.next = current.next.next
                self.length -= 1
                return True
            current = current.next
        return False

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def reverse(self):
        prev = None
        current = self.head
        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def __len__(self):
        return self.length

    def __contains__(self, value):
        current = self.head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False


def main():
    ll = LinkedList()
    for num in [10, 20, 30, 40, 50]:
        ll.append(num)
    ll.prepend(5)

    print("List:", ll.to_list())
    print("Length:", len(ll))
    print("Contains 30:", 30 in ll)
    print("Contains 99:", 99 in ll)

    ll.delete(30)
    print("After delete(30):", ll.to_list())

    ll.reverse()
    print("Reversed:", ll.to_list())


if __name__ == "__main__":
    main()
