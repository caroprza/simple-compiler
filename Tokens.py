from lib2to3.pgen2 import token


class Tokens:
    tokens = None
    index = 0

    def __init__(self):
        self.tokens = []
        self.index = 0


    def append(self, token):
        self.tokens.append(token)

    def peek(self):
        return self.tokens[self.index]


    def next(self):
        if self.index >= len(self.tokens):
            self.index=self.index
        else:
            self.index=self.index+1
