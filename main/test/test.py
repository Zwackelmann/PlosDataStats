class Test:
    def __init__(self, foo):
        self.foo = foo

    def sayFoo(self):
        return self.foo * 3

l = [("sayFoo", True), ("foo", False)]

x1 = Test("hallo")

for att, call in l:
    if call:
        x = getattr(x1, att)()
    else:
        x = getattr(x1, att)

    print x
