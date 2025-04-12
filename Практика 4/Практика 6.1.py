OP_NAMES = {0: 'push', 1: 'op', 2: 'call', 3: 'is', 4: 'to', 5: 'exit'}

def not_implemented(vm):
    raise RuntimeError('Not implemented!')

LIB = { # Для быстрого задания большинства операций полезен модуль operator
    '+': not_implemented,
    '-': not_implemented,
    '*': not_implemented,
    '/': not_implemented, # Целочисленный вариант деления
    '%': not_implemented,
    '&': not_implemented,
    '|': not_implemented,
    '^': not_implemented,
    '<': not_implemented,
    '>': not_implemented,
    '=': not_implemented,
    '<<': not_implemented,
    '>>': not_implemented,
    'if': not_implemented,
    'for': not_implemented,
    '.': not_implemented,
    'emit': not_implemented,
    '?': not_implemented,
    'array': not_implemented,
    '@': not_implemented,
    '!': not_implemented
}

def disasm(bytecode):
    ex = bytecode[0]
    pc = 1
    print(ex)
    entry = ['entry:']
    while pc < len(bytecode):
        bcode = bytecode[pc]
        command = bcode & 0b111
        command = OP_NAMES[command]
        num = bcode >> 3
        if command == 'op':
            num = list(LIB.keys())[num]
        entry.append(f'{pc}:\t{command} {num}')
        pc += 1
    return '\n'.join(entry)

print(disasm([116, 4, 2, 2, 5, 4, 5, 80, 129, 5, 10, 18, 17, 5, 28, 280, 34, 26, 161, 5, 5,
 256, 34, 42, 50, 17, 58, 1, 161, 5, 60, 58, 66, 25, 18, 33, 76, 42, 66, 25, 18,
 33, 84, 82, 18, 17, 74, 1, 92, 98, 90, 97, 8, 41, 152, 160, 105, 5, 44, 50,
 232, 113, 5, 10, 106, 68, 50, 456, 113, 18, 25, 5, 60, 34, 42, 50, 17, 58, 1,
 153, 129, 5, 44, 50, 568, 113, 114, 5, 124, 20, 100, 8, 122, 72, 113, 52, 50,
 106, 17, 145, 36, 50, 106, 17, 104, 113, 50, 18, 25, 122, 496, 113, 10, 50,
 648, 113, 5, 0, 107, 32, 11, 48, 115, 696, 131, 137, 24, 24, 130, 5]))
