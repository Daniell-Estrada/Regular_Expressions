class RegexModel:
    def __init__(self):
        self.data = []
        self.con = None
        self.cur = None

    def get(self, _index=None):
        if _index:
            return self.data[_index]
        return self.data

    def add(self, _value):
        self.data.append(_value)

    def update(self, index, value):
        self.data[index] = value

    def delete(self, index):
        self.data.pop(index)
