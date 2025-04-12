width = 500
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
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.x = 0
        self.y = 0


class TreeVisualizer:
    def __init__(self):
        self.current_x = 0
        self.svg = SVG()

    def visualize(self, node, y=10, x=width//2):
        node.x = x
        node.y = y
        num = y//scale_y
        if node.left:
            self.visualize(node.left, node.y + scale_y, node.x - width//2**(num + 2))
        if node.right:
            self.visualize(node.right, node.y + scale_y, node.x + width//2**(num + 2))

    def create_pic(self, node):
        self.svg.circle(node.x, node.y, 3, "red")
        if node.left:
            self.svg.line(node.x, node.y, node.left.x, node.left.y, "black")
            self.create_pic(node.left)

        if node.right:
            self.svg.line(node.x, node.y, node.right.x, node.right.y, "black")
            self.create_pic(node.right)
        return self.svg



tree_2 = Tree(2, Tree(3, Tree(4), Tree(5)), Tree(6, Tree(7)))
tree_8 = Tree(8, Tree(9, Tree(10), Tree(11, Tree(12), Tree(13))), Tree(14))
tree = Tree(1, tree_2, tree_8)

tv = TreeVisualizer()
tv.visualize(tree)
tv.create_pic(tree).save('tree.svg', width, 300)
