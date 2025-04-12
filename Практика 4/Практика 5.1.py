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


svg = SVG()

svg.line(10, 10, 60, 10, color='black')
svg.line(60, 10, 60, 60, color='black')
svg.line(60, 60, 10, 60, color='black')
svg.line(10, 60, 10, 10, color='black')

svg.circle(10, 10, r=5, color='red')
svg.circle(60, 10, r=5, color='red')
svg.circle(60, 60, r=5, color='red')
svg.circle(10, 60, r=5, color='red')

svg.save('pic.svg', 100, 100)
