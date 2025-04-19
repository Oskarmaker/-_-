class VM:
    def __init__(self, code):
        self.stack = []
        self.code = code
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
            'emit': self.not_implemented,
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

    def output(self):
        for i in self.stack:
            print(i, '\n')

    def run(self):
        ex = self.code[0]
        pc = 1
        while pc < len(self.code):
            bcode = self.code[pc]
            op = self.OP_NAMES[bcode & 0b111]
            num = bcode >> 3
            # Декодирование команды, работа с pc
            if op == 'push':
                self.stack.append(num)
            elif op == 'op':
                self.LIB[list(self.LIB.keys())[num]]()
            elif op == 'exit':
                break
            pc += 1


vm = VM([0, 16, 16, 1, 121, 5])
vm.run()
