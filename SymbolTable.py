class SymbolTable:
    def __init__(self):
        self.indexId = 0
        self.table = []

    def add_symbol(self, attributes):
        attributes.setdefault('id', self.indexId)
        self.table.append(attributes)
        self.indexId+=1

    def get_symbol(self, token):
        return self.table.get(token, None)

    def update_symbol(self, token, attributes):
        if token in self.table:
            self.table[token].update(attributes)
