class Source():
    sources = []
    def __init__(self, coords) -> None:
        self.x_pos, self.y_pos = coords
        Source.sources.append(self)

    def get_coords(self):
        return self.x_pos, self.y_pos

    def move_up(self, y):
        self.y_pos -= y

    def move_down(self, y):
        self.y_pos += y

    def move_right(self, x):
        self.x_pos += x

    def move_left(self, x):
        self.x_pos -= x
