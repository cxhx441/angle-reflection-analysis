class Receiver():
    receivers = []

    # def __init__(self, args) -> None:
    #     if isinstance(args, Receiver):
    #         receiver = args
    #         Receiver((receiver.get_coords))
    #     else:
    #         coords = args
    #         self.x_pos, self.y_pos = coords
    #         self.coords = coords
    #         Receiver.receivers.append(self)

    def __init__(self, coords) -> None:
        self.x_pos, self.y_pos = coords
        self.coords = coords
        Receiver.receivers.append(self)
    def get_coords(self):
        return self.coords
