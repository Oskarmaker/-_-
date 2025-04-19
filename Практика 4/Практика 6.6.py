OP_NAMES = {0: 'push', 1: 'op', 2: 'call', 3: 'is', 4: 'to', 5: 'exit'}

LIB = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x // y,
    '%': lambda x, y: x % y,
    '&': lambda x, y: x & y,
    '|': lambda x, y: x | y,
    '^': lambda x, y: x ^ y,
    '<': lambda x, y: int(x < y),
    '>': lambda x, y: int(x > y),
    '=': lambda x, y: int(x == y),
    '<<': lambda x, y: x << y,
    '>>': lambda x, y: x >> y,
    'if': None,
    'for': None,
    '.': lambda x: print(x, end=' '),
    'emit': lambda x: print(chr(x), end=''),
    '?': lambda: int(input()),
    'array': lambda size: [0] * size,
    '@': lambda arr, idx: arr[idx],
    '!': lambda val, arr, idx: arr.__setitem__(idx, val)
}


class VM:
    def __init__(self, code):
        self.stack = []
        self.code = code
        self.pc = code[0] + 1
        self.scopes = [{}]  # стек областей видимости
        self.call_stack = []

    def run(self):
        while self.pc < len(self.code):
            cmd = self.code[self.pc]
            op = cmd & 0b111
            arg = cmd >> 3
            op_name = OP_NAMES[op]
            self.pc += 1

            if op_name == 'push':
                self.stack.append(arg)
            elif op_name == 'op':
                self.handle_op(arg)
            elif op_name == 'call':
                self.handle_call(arg)
            elif op_name == 'is':
                self.scopes[-1][arg] = (self.pc, 'function')
            elif op_name == 'to':
                value = self.stack.pop()
                self.scopes[-1][arg] = (value, 'variable')
            elif op_name == 'exit':
                if self.call_stack:
                    self.pc, self.scopes = self.call_stack.pop()
                else:
                    break

    def handle_op(self, arg):
        op_name = list(LIB.keys())[arg]
        if op_name == 'if':
            false_addr = self.stack.pop()
            true_addr = self.stack.pop()
            cond = self.stack.pop()
            if cond:
                self.call_stack.append((self.pc, self.scopes))
                self.pc = true_addr
                self.scopes.append({})
            else:
                self.call_stack.append((self.pc, self.scopes))
                self.pc = false_addr
                self.scopes.append({})
        elif op_name == 'for':
            func_addr = self.stack.pop()
            count = self.stack.pop()
            for i in range(count):
                self.stack.append(i)
                self.call_stack.append((self.pc, self.scopes))
                self.pc = func_addr
                self.scopes.append({})
                # После выполнения функции возвращаемся сюда
                if self.pc < len(self.code):
                    cmd = self.code[self.pc]
                    op = cmd & 0b111
                    if OP_NAMES[op] == 'exit':
                        self.pc, self.scopes = self.call_stack.pop()
        elif op_name == 'array':
            size = self.stack.pop()
            self.stack.append([0] * size)
        elif op_name == '@':
            idx = self.stack.pop()
            arr = self.stack.pop()
            self.stack.append(arr[idx])
        elif op_name == '!':
            idx = self.stack.pop()
            arr = self.stack.pop()
            val = self.stack.pop()
            arr[idx] = val
        else:
            func = LIB[op_name]
            # ... остальные операции ...

    def handle_call(self, arg):
        # Поиск в текущей и родительских областях видимости
        for scope in reversed(self.scopes):
            if arg in scope:
                value, typ = scope[arg]
                if typ == 'function':
                    self.call_stack.append((self.pc, self.scopes))
                    self.pc = value
                    self.scopes.append({})
                    return
                elif typ == 'variable':
                    self.stack.append(value)
                    return
        raise RuntimeError(f"Undefined call: {arg}")

vm = VM([116, 4, 2, 2, 5, 4, 5, 80, 129, 5, 10, 18, 17, 5, 28, 280, 34, 26, 161, 5, 5,
 256, 34, 42, 50, 17, 58, 1, 161, 5, 60, 58, 66, 25, 18, 33, 76, 42, 66, 25, 18,
 33, 84, 82, 18, 17, 74, 1, 92, 98, 90, 97, 8, 41, 152, 160, 105, 5, 44, 50,
 232, 113, 5, 10, 106, 68, 50, 456, 113, 18, 25, 5, 60, 34, 42, 50, 17, 58, 1,
 153, 129, 5, 44, 50, 568, 113, 114, 5, 124, 20, 100, 8, 122, 72, 113, 52, 50,
 106, 17, 145, 36, 50, 106, 17, 104, 113, 50, 18, 25, 122, 496, 113, 10, 50,
 648, 113, 5, 0, 107, 32, 11, 48, 115, 696, 131, 137, 24, 24, 130, 5])
vm.run()