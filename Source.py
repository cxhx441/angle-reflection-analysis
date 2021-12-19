class Source():
    sources = []
    def __init__(self, coords) -> None:
        self.x_pos, self.y_pos = coords
        self.coords = coords
        Source.sources.append(self)

    def get_coords(self):
        return self.coords
