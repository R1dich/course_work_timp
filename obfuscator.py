"""
Python Source Obfuscator
Уровни защиты:
  1. Удаление комментариев и docstring-ов
  2. Переименование локальных переменных/функций/классов (AST-трансформация)
  3. Шифрование строковых литералов (XOR + hex-encode)
  4. Упаковка: zlib-сжатие + base64 + exec-wrapper
"""

import ast
import base64
import builtins
import keyword
import os
import random
import string
import sys
import zlib


# ─────────────────────────── helpers ────────────────────────────

BUILTINS = set(dir(builtins)) | set(keyword.kwlist)

_NAME_CHARS = string.ascii_letters + string.digits + '_'


def _rand_name(length: int = 8) -> str:
    first = random.choice(string.ascii_lowercase + '_')
    rest = ''.join(random.choices(_NAME_CHARS, k=length - 1))
    return first + rest


def _unique_name(existing: set, length: int = 8) -> str:
    while True:
        n = '_' + _rand_name(length) + '_'
        if n not in existing:
            existing.add(n)
            return n


# ─────────────────────────── pass 1: strip comments / docstrings ─

class DocstringStripper(ast.NodeTransformer):
    """Удаляет все docstring-и (строковые литералы как первый statement)."""

    def _strip_body(self, body: list) -> list:
        if (body and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)):
            return body[1:]
        return body

    def visit_Module(self, node):
        node.body = self._strip_body(node.body)
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        node.body = self._strip_body(node.body)
        return self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        node.body = self._strip_body(node.body)
        return self.generic_visit(node)


# ─────────────────────────── pass 2: rename identifiers ──────────

class IdentifierRenamer(ast.NodeTransformer):
    """
    Переименовывает все пользовательские имена (переменные, функции, классы,
    аргументы), НЕ трогая встроенные, импортированные модули и dunder-атрибуты.
    """

    def __init__(self):
        self._mapping: dict[str, str] = {}
        self._used: set[str] = set()
        self._imports: set[str] = set()
        self._globals: set[str] = set()
        self._in_class: int = 0  # depth inside class body

    # ── pre-scan: collect imported names ──
    def _collect_imports(self, tree: ast.AST):
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname or alias.name.split('.')[0]
                    self._imports.add(name)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    name = alias.asname or alias.name
                    self._imports.add(name)

    def _should_rename(self, name: str) -> bool:
        if name.startswith('__') and name.endswith('__'):
            return False
        if name in BUILTINS:
            return False
        if name in self._imports:
            return False
        return True

    def _get(self, name: str) -> str:
        if name not in self._mapping:
            self._mapping[name] = _unique_name(self._used)
        return self._mapping[name]

    def run(self, tree: ast.AST) -> ast.AST:
        self._collect_imports(tree)
        return self.visit(tree)

    # ── visitors ──

    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Store, ast.Load, ast.Del)):
            if self._should_rename(node.id):
                node.id = self._get(node.id)
        return node

    def visit_FunctionDef(self, node):
        # Методы класса вызываются как атрибуты (obj.method()),
        # поэтому их имена переименовывать нельзя.
        if self._in_class == 0 and self._should_rename(node.name):
            node.name = self._get(node.name)
        # rename args
        for arg in node.args.args + node.args.posonlyargs + node.args.kwonlyargs:
            if self._should_rename(arg.arg):
                arg.arg = self._get(arg.arg)
        if node.args.vararg and self._should_rename(node.args.vararg.arg):
            node.args.vararg.arg = self._get(node.args.vararg.arg)
        if node.args.kwarg and self._should_rename(node.args.kwarg.arg):
            node.args.kwarg.arg = self._get(node.args.kwarg.arg)
        return self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        if self._should_rename(node.name):
            node.name = self._get(node.name)
        self._in_class += 1
        self.generic_visit(node)
        self._in_class -= 1
        return node

    def visit_Attribute(self, node):
        # не переименовываем атрибуты объектов (node.attr)
        self.visit(node.value)
        return node

    def visit_keyword(self, node):
        # именованные аргументы вызова — не трогаем
        self.visit(node.value)
        return node

    def visit_Global(self, node):
        node.names = [
            self._get(n) if self._should_rename(n) else n
            for n in node.names
        ]
        return node

    def visit_Nonlocal(self, node):
        node.names = [
            self._get(n) if self._should_rename(n) else n
            for n in node.names
        ]
        return node


# ─────────────────────────── pass 3: encrypt string literals ─────

XOR_KEY = random.randint(1, 255)


def _xor_encrypt(s: str, key: int) -> str:
    return ''.join(f'\\x{(ord(c) ^ key):02x}' for c in s)


class StringEncryptor(ast.NodeTransformer):
    """
    Заменяет строковые константы на вызов bytes(...).decode(),
    где байты зашифрованы XOR с случайным ключом.
    f-строки (JoinedStr) пропускаются — внутри них нельзя размещать вызовы.
    """

    def __init__(self, key: int):
        self._key = key

    def visit_JoinedStr(self, node):
        # f-string: не трансформируем содержимое, возвращаем как есть
        return node

    def visit_Constant(self, node):
        if not isinstance(node.value, str):
            return node
        if not node.value:
            return node
        # Encode to UTF-8 first, then XOR each byte (all values stay in 0..255)
        raw = node.value.encode('utf-8')
        encrypted = bytes(b ^ self._key for b in raw)
        key_node = ast.Constant(value=self._key)
        bytes_node = ast.Constant(value=encrypted)
        # bytes(b ^ KEY for b in ENCRYPTED).decode('utf-8')
        call = ast.Call(
            func=ast.Attribute(
                value=ast.Call(
                    func=ast.Name(id='bytes', ctx=ast.Load()),
                    args=[ast.GeneratorExp(
                        elt=ast.BinOp(
                            left=ast.Name(id='_b', ctx=ast.Load()),
                            op=ast.BitXor(),
                            right=key_node,
                        ),
                        generators=[ast.comprehension(
                            target=ast.Name(id='_b', ctx=ast.Store()),
                            iter=bytes_node,
                            ifs=[],
                            is_async=0,
                        )]
                    )],
                    keywords=[],
                ),
                attr='decode',
                ctx=ast.Load(),
            ),
            args=[ast.Constant(value='utf-8')],
            keywords=[],
        )
        ast.fix_missing_locations(call)
        return call


# ─────────────────────────── pass 4: pack ────────────────────────

def _pack(source: str) -> str:
    compressed = zlib.compress(source.encode('utf-8'), level=9)
    encoded = base64.b85encode(compressed).decode('ascii')
    wrapper = (
        "import zlib,base64\n"
        f"exec(zlib.decompress(base64.b85decode({encoded!r})).decode('utf-8'))\n"
    )
    return wrapper


# ─────────────────────────── pipeline ────────────────────────────

def obfuscate(source: str, *, rename: bool = True,
              encrypt_strings: bool = True, pack: bool = True) -> str:
    tree = ast.parse(source)

    # Pass 1: strip docstrings
    tree = DocstringStripper().visit(tree)
    ast.fix_missing_locations(tree)

    # Pass 2: rename identifiers
    if rename:
        renamer = IdentifierRenamer()
        tree = renamer.run(tree)
        ast.fix_missing_locations(tree)

    # Pass 3: encrypt strings
    if encrypt_strings:
        tree = StringEncryptor(XOR_KEY).visit(tree)
        ast.fix_missing_locations(tree)

    # unparse back to source
    result = ast.unparse(tree)

    # Pass 4: pack
    if pack:
        result = _pack(result)

    return result


# ─────────────────────────── CLI ─────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Python source obfuscator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Уровни защиты (все включены по умолчанию):
  --no-rename          не переименовывать идентификаторы
  --no-encrypt         не шифровать строки
  --no-pack            не упаковывать (zlib+base64)
""")
    parser.add_argument('input', help='входной .py файл')
    parser.add_argument('-o', '--output', help='выходной файл (по умолчанию: <input>_obf.py)')
    parser.add_argument('--no-rename', action='store_true')
    parser.add_argument('--no-encrypt', action='store_true')
    parser.add_argument('--no-pack', action='store_true')
    args = parser.parse_args()

    with open(args.input, encoding='utf-8') as f:
        source = f.read()

    out_path = args.output or (
        os.path.splitext(args.input)[0] + '_obf.py'
    )

    result = obfuscate(
        source,
        rename=not args.no_rename,
        encrypt_strings=not args.no_encrypt,
        pack=not args.no_pack,
    )

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(result)

    in_size = len(source.encode())
    out_size = len(result.encode())
    print(f'[OK] {args.input} -> {out_path}')
    print(f'     Исходный размер : {in_size:>7} байт')
    print(f'     Выходной размер : {out_size:>7} байт')
    print(f'     Степень сжатия  : {out_size / in_size * 100:.1f}%')


if __name__ == '__main__':
    main()
