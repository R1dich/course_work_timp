"""
Демонстрационная программа для тестирования обфускатора.
Реализует простое шифрование Цезаря и работу со стеком.
"""

import os
import sys


SECRET_KEY = 13  # ключ шифра Цезаря


def caesar_encrypt(text, shift):
    """Шифрует строку методом Цезаря."""
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - base + shift) % 26 + base)
            result.append(encrypted_char)
        else:
            result.append(char)
    return ''.join(result)


def caesar_decrypt(text, shift):
    """Расшифровывает строку методом Цезаря."""
    return caesar_encrypt(text, -shift)


class SimpleStack:
    """Простой стек на основе списка."""

    def __init__(self):
        self._data = []
        self._size = 0

    def push(self, value):
        self._data.append(value)
        self._size += 1

    def pop(self):
        if self._size == 0:
            raise IndexError("pop from empty stack")
        self._size -= 1
        return self._data.pop()

    def peek(self):
        if self._size == 0:
            raise IndexError("peek at empty stack")
        return self._data[-1]

    def is_empty(self):
        return self._size == 0

    def __len__(self):
        return self._size


def process_messages(messages, key):
    """Шифрует список сообщений и складывает в стек."""
    stack = SimpleStack()
    for msg in messages:
        encrypted = caesar_encrypt(msg, key)
        stack.push(encrypted)
        print(f"  [push] '{msg}' -> '{encrypted}'")
    return stack


def main():
    print("=== Демо: шифр Цезаря + стек ===")

    messages = [
        "Hello, World!",
        "Python is great",
        "Obfuscation test",
    ]

    print(f"\nШифрование с ключом {SECRET_KEY}:")
    stack = process_messages(messages, SECRET_KEY)

    print(f"\nРасшифровка (из стека, LIFO):")
    while not stack.is_empty():
        enc = stack.pop()
        dec = caesar_decrypt(enc, SECRET_KEY)
        print(f"  [pop]  '{enc}' -> '{dec}'")

    print("\nГотово.")


if __name__ == "__main__":
    main()
