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
    entry = ['entry:']
    while pc < len(bytecode):
        bcode = bytecode[pc]
        command = bcode & 0b111
        command = OP_NAMES[command]
        num = bcode >> 3
        if command == 'op':
            num = list(LIB.keys())[num]
        entry.append(f'{command} {num}')
        pc += 1
    return '\n\t'.join(entry)

print(disasm([57, 8440, 129, 8704, 129, 8688, 129, 8600, 129, 8704, 129, 8576, 129, 8672,
 129, 8672, 129, 8576, 129, 256, 129, 8728, 129, 8712, 129, 8696, 129, 8616,
 129, 8768, 129, 8680, 129, 8688, 129, 256, 129, 8592, 129, 8792, 129, 8696,
 129, 8688, 129, 8664, 129, 8680, 129, 8616, 129, 8680, 129, 8576, 129, 264,
 129, 5, 0, 3, 2, 5]))
