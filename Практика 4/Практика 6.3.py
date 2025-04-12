class VM:
    def __init__(self, code):
        self.stack = []
        self.pc = 0
        self.code = code
        self.scope = {}
        self.call_stack = []
        self.OP_NAMES = {0: 'push', 1: 'op', 2: 'call', 3: 'is', 4: 'to', 5: 'exit'}
        self.LIB = {
            '+': self.summ,
            '-': self.not_implemented,
            '*': self.not_implemented,
            '/': self.not_implemented,  # Целочисленный вариант деления
            '%': self.not_implemented,
            '&': self.not_implemented,
            '|': self.not_implemented,
            '^': self.not_implemented,
            '<': self.not_implemented,
            '>': self.not_implemented,
            '=': self.not_implemented,
            '<<': self.not_implemented,
            '>>': self.not_implemented,
            'if': self.not_implemented,
            'for': self.not_implemented,
            '.': self.output,
            'emit': self.emit,
            '?': self.not_implemented,
            'array': self.not_implemented,
            '@': self.not_implemented,
            '!': self.not_implemented
        }

    def not_implemented(self):
        raise RuntimeError('Not implemented!')

    def summ(self):
        ans = self.stack.pop() + self.stack.pop()
        self.stack.append(ans)

    def emit(self):
        print(chr(self.stack.pop()), end='')
    def output(self):
        for i in self.stack:
            print(i, '\n')

    def call(self, arg):
        if arg not in self.scope:
            raise RuntimeError(f"Unknown call target: {arg}")
        value_type, value = self.scope[arg]
        if value_type == 'func':
            self.call_stack.append(self.pc)
            self.pc = value
        elif value_type == 'var':
            self.stack.append(value)
        else:
            raise RuntimeError(f"Unknown value type in scope: {value_type}")

    def is_(self, arg):
        if not self.stack:
            raise RuntimeError("Empty stack when defining function")
        addr = self.stack.pop()
        self.scope[arg] = ('func', addr)

    def run(self):
        ex = self.code[0]
        self.pc = 1
        while self.pc < len(self.code):
            bcode = self.code[self.pc]
            op = self.OP_NAMES[bcode & 0b111]
            num = bcode >> 3
            # Декодирование команды, работа с pc
            if op == 'push':
                self.stack.append(num)
            elif op == 'op':
                self.LIB[list(self.LIB.keys())[num]]()
            elif op == 'exit':
                break
            self.pc += 1


vm = VM([57, 8440, 129, 8704, 129, 8688, 129, 8600, 129, 8704, 129, 8576, 129, 8672,
 129, 8672, 129, 8576, 129, 256, 129, 8728, 129, 8712, 129, 8696, 129, 8616,
 129, 8768, 129, 8680, 129, 8688, 129, 256, 129, 8592, 129, 8792, 129, 8696,
 129, 8688, 129, 8664, 129, 8680, 129, 8616, 129, 8680, 129, 8576, 129, 264,
 129, 5, 0, 3, 2, 5])
vm.run()