class HTML:
    def __init__(self):
        self.code = []
        self.context = []

    def __getattr__(self, tag_name):
        def tag_handler(*args, **kwargs):
            content = args[0] if args else None
            return Tag(self, tag_name, content)
        return tag_handler

    def add_tag(self, tag):
        if self.context:
            self.context[-1].add_child(tag)
        else:
            self.code.append(tag)
        return tag

    def body(self):
        return self.add_tag(Tag(self, 'body'))

    def div(self):
        return self.add_tag(Tag(self, 'div'))

    def p(self, content=None):
        return self.add_tag(Tag(self, 'p', content))

    def get_code(self):
        return '\n'.join(tag.render(0) for tag in self.code)


class Tag:
    def __init__(self, html, name, content=None):
        self.html = html
        self.name = name
        self.content = content
        self.children = []
        self.ident = 0

    def __enter__(self):
        self.html.context.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.html.context.pop()

    def add_child(self, tag):
        self.children.append(tag)

    def render(self, indent_level):
        indent = '\t' * indent_level
        if self.content and not self.children:
            return f"{indent}<{self.name}>{self.content}</{self.name}>"
        parts = [f"{indent}<{self.name}>"]
        if self.content:
            parts.append(f"\t{indent}{self.content}")
        for child in self.children:
            parts.append(child.render(indent_level + 1))
        parts.append(f"{indent}</{self.name}>")
        return '\n'.join(parts)



html = HTML()
with html.body():
    with html.div():
        with html.div():
            html.p('Первая строка.')
            html.p('Вторая строка.')
        with html.div():
            html.p('Третья строка.')

print(html.get_code())
