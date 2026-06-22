PyMorph 

obfuscator/
├── obfuscator.py               ← сам обфускатор
├── target.py / target_obf.py   ← тестовый пример
└── examples/
    ├── 01_linked_list.py       ← связный список (Node/LinkedList)
    ├── 02_matrix.py            ← умножение/транспонирование матриц
    ├── 03_sorting.py           ← 4 алгоритма сортировки + бенчмарк
    ├── 04_vigenere.py          ← шифр Виженера + частотный анализ
    ├── 05_mini_interpreter.py  ← интерпретатор арифм. выражений (Lexer/Parser)
    └── obf/                    ← обфусцированные версии (все работают корректно)

Все примеры можно запустить через python обфускатор target.py -o out.py, после чего python out.py даёт идентичный с оригиналом вывод.
