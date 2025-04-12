class class1:
    def __init__(self):
        self.num = 1


class class2(class1):
    def __init__(self):
        self.num = 2


class class3(class2):
    def __init__(self):
        self.num = 3


get_inheritance = lambda cls: ' -> '.join(c.__name__ for c in cls.__mro__)
print(get_inheritance(class3))