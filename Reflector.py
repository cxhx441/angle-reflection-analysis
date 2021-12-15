import math

class Reflector(): 
    def __init__(self, start_coords, end_coords) -> None:
        self.x0_pos, self.y0_pos = start_coords
        self.x1_pos, self.y1_pos = end_coords
        self.start_coords = start_coords
        self.end_coords = end_coords

    def get_start_coords(self): 
        return self.start_coords

    def get_end_coords(self): 
        return self.end_coords

    def get_delta_x(self):
        return abs(self.x1_pos - self.x0_pos)
        
    def get_delta_y(self):
        return abs(self.y1_pos - self.y0_pos)
        
    def get_length(self): 
        return (self.get_delta_x(), self.get_delta_y())


    def get_center_coords(self):
        return ((self.get_delta_x())/2, (self.get_delta_y())/2)

    def get_angle(self): 
        return math.atan2(self.get_delta_x(), self.get_delta_y())

    def rotate(self, pivot_point, angle):
        if pivot_point == self.get_start_coords():
            x0 = pivot_point[0]
            y0 = pivot_point[1]
            x1 = self.get_end_coords()[0]
            y1 = self.get_end_coords()[1]
            x3 = math.cos(angle)(x1-x0) - math.sin(angle)(y1-y0) + x1
            y3 = math.sin(angle)(x1-x0) + math.cos(angle)(y1-y0) + x1
            self.x1_pos = x3
            self.y1_pos = y3
        elif pivot_point == self.get_end_coords():
            x0 = pivot_point[0]
            y0 = pivot_point[1]
            x1 = self.get_start_coords()[0]
            y1 = self.get_start_coords()[1]
            x3 = math.cos(angle)(x1-x0) - math.sin(angle)(y1-y0) + x1
            y3 = math.sin(angle)(x1-x0) + math.cos(angle)(y1-y0) + x1
            self.x0_pos = x3
            self.y0_pos = y3
        elif pivot_point == self.get_center_coords():
            pass 
        else:
            print("error")
        
