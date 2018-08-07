class ValidationLink():
    def __init__(self, chain, validation, front=False):
        self.validation = validation
        self.chain = chain
        if not front:
            self.chain.append(self)
        else:
            self.chain.insert(0, self)

    def next(self):
        location = self.chain.index(self)
        if not self.end():
            return self.chain[location + 1]

    def end(self):
        return (self.chain.index(self) + 1 >= len(self.chain))

    def __call__(self, field):
        validator = self.validation(field)
        if not validator.is_valid() or self.end(): return validator
        return self.next()(field)
