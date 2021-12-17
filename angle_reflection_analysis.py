from Receiver import Receiver
from Source import Source
from Reflector import Reflector
from Ray import Ray
from PIL import Image, ImageDraw, ImageTk
import math

import tkinter
from tkinter import ttk

def get_draw_line_coords(obj):
    x0, y0 = obj.get_start_coords()
    x1, y1 = obj.get_end_coords()
    x0, y0, x1, y1 = (el*scale for el in (x0, y0, x1, y1)) 
    y0 = canvas_size[1] - y0
    y1 = canvas_size[1] - y1
    return (x0, y0, x1, y1)

def get_draw_rect_coords(obj, diagonal_len):
    x, y = obj.get_coords()
    x, y = (el*scale for el in (x, y)) 
    y = canvas_size[1] - y
    return (x-diagonal_len, y-diagonal_len, x+diagonal_len, y+diagonal_len)

def create_rays_2_reflector(source_obj, ref_obj):
    ray_2_start = Ray(source_obj.get_coords(), ref_obj.get_start_coords())
    ray_2_center = Ray(source_obj.get_coords(), ref_obj.get_center_coords())
    ray_2_end = Ray(source_obj.get_coords(), ref_obj.get_end_coords())
    return (ray_2_start, ray_2_center, ray_2_end)
def draw_s_to_reflector(rays):
    ray1 = canvas.create_line(get_draw_line_coords(rays_2_panel[0]), fill="yellow", width=3)
    ray2 = canvas.create_line(get_draw_line_coords(rays_2_panel[1]), fill="yellow", width=3)
    ray3 = canvas.create_line(get_draw_line_coords(rays_2_panel[2]), fill="yellow", width=3)

def angle_between_2_lines(line0, line1): 
    m0 = line0.get_slope()
    m1 = line1.get_slope()
    return math.degrees(math.atan((m1-m0)/(1+(m1*m0))))

def intersection_of_two_lines(line0, line1): 
    m0, b0 = line0.get_slope_intercept_form()
    m1, b1 = line1.get_slope_intercept_form()
    x_int = (b1 - b0)/(m0-m1)
    return (x_int, m0*x_int + b0)

scale = 10

room_size = (85, 43)
s1_pos = (84.5, 8.75)
r1_pos = (32, 11)
ref1_pos0 = (66, 31.83)
ref1_pos1 = (55, 35.83)

# get_reflector_to_edge

s1 = Source(s1_pos)
r1 = Receiver(r1_pos)
ref1 = Reflector(ref1_pos0, ref1_pos1)
#rotate 90 degrees around either coordinate
ref1.rotate(angle=-math.pi/2)
#translate so one point starts on source
#extend to intersection of ref
#get length of this extenssion, 
# make end point twice as far away
# get intersection of that new end point to the receiver and the reflection panel, 
# that is new start point of reflected line. 
rays = create_rays_2_reflector(s1, ref1)
print(ref1.get_start_coords())
print(ref1.get_center_coords())
print(ref1.get_end_coords())

canvas_size = tuple(x*scale for x in room_size)

#tkinter
top = tkinter.Tk()

canvas = tkinter.Canvas(width=canvas_size[0], height=canvas_size[1], cursor="cross")
image = Image.new('RGB' , canvas_size, (128, 128, 128))
tk_image = ImageTk.PhotoImage(image)

canvas.create_image(0,0, anchor="nw", image=tk_image)

diagonal_len = 20
source = canvas.create_rectangle(get_draw_rect_coords(s1, diagonal_len), fill='#00FF00', activeoutline='red')
receiver = canvas.create_rectangle(get_draw_rect_coords(r1, diagonal_len), fill='#FF0000', activeoutline='red')
reflector = canvas.create_line(get_draw_line_coords(ref1), fill="purple", width=5, activefill = 'red')
ray1 = canvas.create_line(get_draw_line_coords(rays[0]), fill="yellow", width=3)
ray2 = canvas.create_line(get_draw_line_coords(rays[1]), fill="yellow", width=3)
ray3 = canvas.create_line(get_draw_line_coords(rays[2]), fill="yellow", width=3)

canvas.pack()
top.mainloop()
# print(angle_between_2_lines(rays[0], ref1))