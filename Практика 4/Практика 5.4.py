width = 700
scale_y = 50


class SVG:
    def __init__(self):
        self.data = ''

    def line(self, x1, y1, x2, y2, color):
        self.data += f'<line x1="{"%.6f" % x1}" y1="{"%.6f" % y1}" x2="{"%.6f" % x2}" y2="{"%.6f" % y2}" stroke="{color}" />\n'

    def circle(self, cx, cy, r, color):
        self.data += f'<circle cx="{"%.6f" % cx}" cy="{"%.6f" % cy}" r="{"%.6f" % r}" fill="{color}" />\n'

    def save(self, name, w, h):
        self.data = f'<svg version="1.1" width="{"%.6f" % w}" height="{"%.6f" % h}" xmlns="http://www.w3.org/2000/svg">\n' + self.data + '</svg>'
        with open(name, 'w') as f:
            f.write(self.data)


class Tree:
    def __init__(self, val, *children):
        self.val = val
        self.children = children
        self.x = 0
        self.y = 0


class TreeVisualizer:
    def __init__(self):
        self.current_x = 0
        self.svg = SVG()
        self.mx = 0

    def visualize(self, node, y=10, x=width//2):
        node.x = x
        node.y = y
        num = y//scale_y
        l = len(node.children)
        for i, child in enumerate(node.children):
            if i < l // 2:
                self.visualize(child, node.y + scale_y, node.x - width // self.mx ** (num + 1 + 1 / self.mx) * (l // 2 - i))
            elif i == l//2 and l % 2 == 1:
                self.visualize(child, node.y + scale_y, node.x)
            else:
                if l % 2 == 0:
                    self.visualize(child, node.y + scale_y, node.x + width // self.mx ** (num + 1 + 1 / self.mx) * (i - l // 2 + 1))
                else:
                    self.visualize(child, node.y + scale_y, node.x + width // self.mx ** (num + 1 + 1 / self.mx) * (i - l // 2))

    def find_n(self, root):
        if len(root.children) > self.mx: self.mx = len(root.children)
        for child in root.children:
            self.find_n(child)

    def create_pic(self, node):

        for child in node.children:
            self.svg.line(node.x, node.y, child.x, child.y, "black")
            self.create_pic(child)
        self.svg.circle(node.x, node.y, 3, "red")
        return self.svg


tree2 = Tree(2, Tree(6), Tree(7, Tree(14)))
tree3 = Tree(3, Tree(8), Tree(9), Tree(10, Tree(15), Tree(16)))
tree5 = Tree(5, Tree(11), Tree(12), Tree(13, Tree(17), Tree(18), Tree(19)))
tree = Tree(1, tree2, tree3, Tree(4), tree5)

tv = TreeVisualizer()
tv.find_n(tree)
print(tv.mx)
tv.visualize(tree)
tv.create_pic(tree).save('tree.svg', width, 300)
