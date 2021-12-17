import math

class Reflector():
    def __init__(self, start_coords, end_coords) -> None:
        self.x0, self.y0 = start_coords
        self.x1, self.y1 = end_coords


    def get_start_coords(self):
        return (self.x0, self.y0)

    def get_end_coords(self):
        return (self.x1, self.y1)

    def set_start_coords(self, new_start):
        self.x0, self.y0 = new_start

    def set_end_coords(self, new_end):
        (self.x1, self.y1) = new_end

    def get_delta_x(self):
        return abs(self.x1 - self.x0)

    def get_delta_y(self):
        return abs(self.y1 - self.y0)

    def get_slope_intercept_form(self):
        x, y = self.get_start_coords()
        m = self.get_slope()
        b = y - m*x
        return (m, b)

    def get_length(self):
        return (self.get_delta_x(), self.get_delta_y())

    def get_center_coords(self):
        return ((self.x0 + self.x1)/2, (self.y0 + self.y1)/2)

    def get_angle(self):
        return math.atan2(self.get_delta_x(), self.get_delta_y())

    def get_slope(self):
        return (self.y1-self.y0) / (self.x1-self.x0)

    def rotate(self,pivot=None, angle=None):
        if angle == None:
            angle = math.pi/2
        new_x0, new_y0 = self.get_start_coords()
        new_x1, new_y1 = self.get_end_coords()
        new_x_mid, new_y_mid = self.get_center_coords()
        if pivot == (new_x0, new_y0) or pivot == None:
            trans_x0 = new_x0 - new_x0
            trans_x1 = new_x1 - new_x0
            trans_y0 = new_y0 - new_y0
            trans_y1 = new_y1 - new_y0
        elif pivot == (new_x1, new_y1):
            trans_x0 = new_x0 - new_x1
            trans_x1 = new_x1 - new_x1
            trans_y0 = new_y0 - new_y1
            trans_y1 = new_y1 - new_y1
        elif pivot == (new_x_mid, new_y_mid):
            trans_x0 = new_x0 - new_x_mid
            trans_x1 = new_x1 - new_x_mid
            trans_y0 = new_y0 - new_y_mid
            trans_y1 = new_y1 - new_y_mid

        self.x0 = trans_x0*math.cos(angle) - trans_y0*math.sin(angle)
        self.x1 = trans_x1*math.cos(angle) - trans_y1*math.sin(angle)
        self.y0 = trans_x0*math.sin(angle) + trans_y0*math.cos(angle)
        self.y1 = trans_x1*math.sin(angle) + trans_y1*math.cos(angle)

        if pivot == (new_x0, new_y0) or pivot == None:
            self.x0 += new_x0
            self.x1 += new_x0
            self.y0 += new_y0
            self.y1 += new_y0
        elif pivot == (new_x1, new_y1):
            self.x0 += new_x1
            self.x1 += new_x1
            self.y0 += new_y1
            self.y1 += new_y1
        elif pivot == (new_x_mid, new_y_mid):
            self.x0 += new_x_mid
            self.x1 += new_x_mid
            self.y0 += new_y_mid
            self.y1 += new_y_mid

    def copy(self):
        return Reflector(self.get_start_coords(), self.get_end_coords())

    def move(self, destination_coord):
        movement_coords = (destination_coord[0] - self.get_start_coords()[0], destination_coord[1] - self.get_start_coords()[1])
        new_start_coords = (self.get_start_coords()[0] + movement_coords[0], self.get_start_coords()[1] + movement_coords[1])
        new_end_coords = (self.get_end_coords()[0] + movement_coords[0], self.get_end_coords()[1] + movement_coords[1])
        self.set_start_coords(new_start_coords)
        self.set_end_coords(new_end_coords)
    # def rotate(self, pivot_point, angle):
    #     if pivot_point == self.get_start_coords():
    #         x0 = pivot_point[0]
    #         y0 = pivot_point[1]
    #         x1 = self.get_end_coords()[0]
    #         y1 = self.get_end_coords()[1]
    #         x3 = math.cos(angle)*(x1-x0) - math.sin(angle)*(y1-y0) + x1
    #         y3 = math.sin(angle)*(x1-x0) + math.cos(angle)*(y1-y0) + x1
    #         self.x1 = x3
    #         self.y1 = y3
    #     elif pivot_point == self.get_end_coords():
    #         x0 = pivot_point[0]
    #         y0 = pivot_point[1]
    #         x1 = self.get_start_coords()[0]
    #         y1 = self.get_start_coords()[1]
    #         x3 = math.cos(angle)*(x1-x0) - math.sin(angle)*(y1-y0) + x1
    #         y3 = math.sin(angle)*(x1-x0) + math.cos(angle)*(y1-y0) + x1
    #         self.x0 = x3
    #         self.y0 = y3
    #     elif pivot_point == self.get_center_coords():
    #         pass
    #     else:
    #         print("error")

