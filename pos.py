class Pos:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
    def x(self):
        return self.columns
    def y(self):
        return self.rows       