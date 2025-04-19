import ast
mp = 'example_module.py'
with open('example_module.py', 'r', encoding='utf-8') as f:
    ms = f.read()

s = ''
md = ast.parse(ms)
a = mp.split('.')[0]
s += f'# Модуль {a}\n\n'
s += ast.get_docstring(md) + '\n\n'
for node in md.body:
    if isinstance(node, ast.ClassDef):
        s += f'## Класс {node.name}\n\n'
        s += ast.get_docstring(node) + '\n\n'
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                s += f'* **Метод** `{item.name}('


                l = len(item.args.args)
                for i, el in enumerate(item.args.args):
                    if i == l - 1:
                        s += el.arg
                    else:
                        s += el.arg + ', '
                    if el.annotation is not None:
                        s += ': ' + el.annotation.id
                if item.returns is not None:
                    s += ') -> ' + item.returns.id + '`\n\n'
                else:
                    s += ')`\n\n'
                s += ast.get_docstring(item) + '\n\n'
    elif isinstance(node, ast.FunctionDef):
        s += f'## Функция {node.name}\n\n'
        s += f'Сигнатура: `{node.name}('
        l = len(node.args.args)
        for i, el in enumerate(node.args.args):
            if i == l - 1:
                s += el.arg
            else:
                s += el.arg + ', '
            if el.annotation is not None:
                s += ': ' + el.annotation.id
        if node.returns is not None:
            s += ') -> ' + node.returns.id + '`\n\n'
        else:
            s += ')`\n\n'
        s += ast.get_docstring(node) + '\n\n'
print(s)