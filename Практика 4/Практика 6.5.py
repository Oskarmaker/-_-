class VM:
    def __init__(self, code):
        self.stack = []
        self.pc = 0
        self.code = code
        self.global_scope = {}
        self.scopes = [{}]
        self.call_stack = []
        self.OP_NAMES = {0: 'push', 1: 'op', 2: 'call', 3: 'is', 4: 'to', 5: 'exit'}
        self.LIB = {
            '+': self.summ,
            '-': self.sub,
            '*': self.mul,
            '/': self.div,
            '%': self.mod,
            '&': self.bit_and,
            '|': self.bit_or,
            '^': self.bit_xor,
            '<': self.lt,
            '>': self.gt,
            '=': self.eq,
            '<<': self.shl,
            '>>': self.shr,
            'if': self.if_,
            'for': self.for_,
            '.': self.output,
            'emit': self.emit,
            '?': self.cond,
            'array': self.array,
            '@': self.fetch,
            '!': self.store
        }

    def summ(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a + b)

    def sub(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a - b)

    def mul(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a * b)

    def div(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a // b)

    def mod(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a % b)

    def bit_and(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a & b)

    def bit_or(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a | b)

    def bit_xor(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a ^ b)

    def shl(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a << b)

    def shr(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(a >> b)

    def lt(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(1 if a < b else 0)

    def gt(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(1 if a > b else 0)

    def eq(self):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(1 if a == b else 0)

    def if_(self):
        false_branch = self.stack.pop()
        true_branch = self.stack.pop()
        condition = self.stack.pop()
        branch = true_branch if condition else false_branch
        self.call_stack.append((self.pc, self.scopes))
        self.pc = branch
        self.scopes.append({})

    def for_(self):
        end = self.stack.pop()
        start = self.stack.pop()
        var = self.stack.pop()
        body = self.stack.pop()
        for i in range(start, end):
            self.scopes[-1][var] = ('var', i)
            self.call(body)

    def cond(self):
        cases = self.stack.pop()
        for condition, action in cases:
            if condition:
                self.call(action)
                return

    def emit(self):
        print(chr(self.stack.pop()), end='')

    def output(self):
        print(self.stack.pop(), end=' ')

    def array(self):
        size = self.stack.pop()
        self.stack.append([0] * size)

    def fetch(self):
        addr = self.stack.pop()
        self.stack.append(self.stack[addr])

    def store(self):
        value = self.stack.pop()
        addr = self.stack.pop()
        self.stack[addr] = value

    def call(self, arg):
        for scope in reversed(self.scopes):
            if arg in scope:
                value_type, value = scope[arg]
                break
        else:
            if arg in self.global_scope:
                value_type, value = self.global_scope[arg]
            else:
                raise RuntimeError(f"Unknown call target: {arg}")

        if value_type == 'func':
            self.call_stack.append((self.pc, self.scopes))
            self.pc = value
            self.scopes.append({})
        elif value_type == 'var':
            self.stack.append(value)
        else:
            raise RuntimeError(f"Unknown value type: {value_type}")

    def is_(self, arg):
        if not self.stack:
            raise RuntimeError("Empty stack when defining function")
        addr = self.stack.pop()
        self.global_scope[arg] = ('func', addr)

    def to(self, arg):
        if not self.stack:
            raise RuntimeError("Empty stack when assigning variable")
        value = self.stack.pop()
        self.scopes[-1][arg] = ('var', value)

    def exit(self):
        if self.call_stack:
            self.pc, self.scopes = self.call_stack.pop()
            self.scopes.pop()
        else:
            self.pc = len(self.code)

    def run(self):
        if not self.code:
            return
        self.pc = self.code[0] + 1
        while self.pc < len(self.code):
            instruction = self.code[self.pc]
            opcode = instruction & 0b111
            arg = instruction >> 3
            if opcode == 0:
                self.stack.append(arg)
            elif opcode == 1:
                op_name = list(self.LIB.keys())[arg % len(self.LIB)]
                self.LIB[op_name]()
            elif opcode == 2:
                self.call(arg)
            elif opcode == 3:
                self.is_(arg)
            elif opcode == 4:
                self.to(arg)
            elif opcode == 5:
                self.exit()
                if self.pc >= len(self.code):
                    break

            self.pc += 1


if __name__ == "__main__":
    bytecode = [17, 8, 5, 2, 2, 8, 9, 10, 17, 5, 4, 2, 16, 65, 0, 16, 105, 5, 72, 11, 40, 10,
 121, 5]

    vm = VM(bytecode)
    vm.run()