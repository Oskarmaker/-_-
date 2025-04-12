class Num:
    def __init__(self, value):
        self.value = value


class Mul:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class PrintVisitor:
    def visit(self, node):
        if isinstance(node, Num):
            return str(node.value)
        if isinstance(node, Mul):
            return f"({self.visit(node.left)} * {self.visit(node.right)})"
        if isinstance(node, Add):
            return f"({self.visit(node.left)} + {self.visit(node.right)})"


class CalcVisitor:
    def visit(self, node):
        if isinstance(node, Num):
            return node.value
        if isinstance(node, Mul):
            return self.visit(node.left) * self.visit(node.right)
        if isinstance(node, Add):
            return self.visit(node.left) + self.visit(node.right)


class StackVisitor:
    def visit(self, node):
        if isinstance(node, Num):
            return f"PUSH {node.value}"
        if isinstance(node, Mul):
            return f"{self.visit(node.left)}\n{self.visit(node.right)}\nMUL"
        if isinstance(node, Add):
            return f"{self.visit(node.left)}\n{self.visit(node.right)}\nADD"


ast = Add(Num(7), Mul(Num(3), Num(2)))
pv = PrintVisitor()
print(pv.visit(ast))
cv = CalcVisitor()
print(cv.visit(ast))
sv = StackVisitor()
print(sv.visit(ast))
