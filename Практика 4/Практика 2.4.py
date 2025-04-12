def struct(*fields):
    class Struct:
        __slots__ = fields

        def __init__(self, **kwargs):
            for field in fields:
                setattr(self, field, kwargs.get(field))

        def __repr__(self):
            values = ", ".join(f"{f}={getattr(self, f)!r}" for f in fields)
            return f"Struct({values})"

    Struct.__name__ = f"Struct({','.join(fields)})"
    return Struct


Point = struct('x', 'y')
p = Point(x=1, y=2)
assert p.x == 1
assert p.y == 2
assert repr(p) == "Struct(x=1, y=2)"
assert type(p).__name__ == "Struct(x,y)"