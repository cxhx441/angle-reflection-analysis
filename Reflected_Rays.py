
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

def angle_between_2_lines(line0, line1):
    m0 = line0.get_slope()
    m1 = line1.get_slope()
    return math.degrees(math.atan((m1-m0)/(1+(m1*m0))))

def get_intersection_of_two_lines(line0, line1):
    m0, b0 = line0.get_slope_intercept_form()
    m1, b1 = line1.get_slope_intercept_form()
    x_int = (b1 - b0)/(m0-m1)
    return (x_int, m0*x_int + b0)

def get_reflected_rays(source, reflector):
    #source to reflector
    ray_2_start = Ray(source.get_coords(), reflector.get_start_coords())
    ray_2_center = Ray(source.get_coords(), reflector.get_center_coords())
    ray_2_end = Ray(source.get_coords(), reflector.get_end_coords())

    #reflector, reflecting rays
    #rotate 90 degrees around either coordinate
    ray_temp = Ray(reflector.get_start_coords(), reflector.get_end_coords())
    ray_temp.rotate(angle=-math.pi/2)
    #translate so one point starts on source
    ray_temp.move(source.get_coords())
    #extend to intersection of ref
    intersection = get_intersection_of_two_lines(reflector, ray_temp)
    ray_temp.set_end_coords(intersection)
    #get length of this extenssion,OR JUST ROTATE?
    # make end point twice as far away OR JUST ROTATE?
    ray_temp.rotate(pivot=ray_temp.get_end_coords(), angle=math.pi)
    # get intersection of that new end point to the receiver and the reflection panel,
    reflect_ray_2_start = ray_temp.copy()
    reflect_ray_2_center = ray_temp.copy()
    reflect_ray_2_end = ray_temp.copy()
    Ray.rays.remove(ray_temp)
    reflect_ray_2_start.set_end_coords(reflector.get_start_coords())
    reflect_ray_2_center.set_end_coords(reflector.get_center_coords())
    reflect_ray_2_end.set_end_coords(reflector.get_end_coords())
    reflected_rays = (reflect_ray_2_start, reflect_ray_2_center, reflect_ray_2_end)

    for ref_ray in reflected_rays:
        ref_ray.extend(room_size)

    reflect_ray_2_start.move(reflector.get_start_coords())
    reflect_ray_2_center.move(reflector.get_center_coords())
    reflect_ray_2_end.move(reflector.get_end_coords())
    # that is new start point of reflected line.

    # return (ray_2_start, ray_2_center, ray_2_end, reflect_ray_2_start, reflect_ray_2_center, reflect_ray_2_end)

def draw_rays(ray, ray_color):
    canvas.create_line(get_draw_line_coords(ray), fill=ray_color, width=3)

scale = 10

room_size = (75.989, 45.38)
s1_pos = (74.007, 6.773)
r1_pos = (5.102, 20.266)
r2_pos = (10.824, 17.093)
r3_pos = (16.574, 14.468)
r4_pos = (22.407, 11.926)
r5_pos = (28.785,9.885)
r6_pos = (31.838, 8.231)
ref1_pos0 = (27.511, 34.238)
ref1_pos1 = (15.604, 33.137)
ref2_pos0 = (59.351, 31.253)
ref2_pos1 = (48.198,35.313)
ref3_pos0 = (73.362, 25.586)
ref3_pos1 = (62.188, 29.653)

# get_reflector_to_edge

s1 = Source(s1_pos)
r1 = Receiver(r1_pos)
r2 = Receiver(r2_pos)
r3 = Receiver(r3_pos)
r4 = Receiver(r4_pos)
r5 = Receiver(r5_pos)
r6 = Receiver(r6_pos)
ref1 = Reflector(ref1_pos0, ref1_pos1)
ref2 = Reflector(ref2_pos0, ref2_pos1)
ref3 = Reflector(ref3_pos0, ref3_pos1)
# ref3.rotate(pivot=ref3.get_center_coords(), angle=-5*math.pi/180)
# ref2.rotate(pivot=ref2.get_start_coords(), angle=6*math.pi/180)
# ref1.rotate(pivot=ref1.get_start_coords(), angle=6*math.pi/180)
# ref1.move_vertical(10)

for source in Source.sources:
    for reflector in Reflector.reflectors:
        get_reflected_rays(source, reflector)

canvas_size = tuple(x*scale for x in room_size)

#tkinter
top = tkinter.Tk()

canvas = tkinter.Canvas(width=canvas_size[0], height=canvas_size[1], cursor="cross")
image = Image.new('RGB' , tuple(math.ceil(x) for x in canvas_size), (128, 128, 128))
tk_image = ImageTk.PhotoImage(image)

canvas.create_image(0,0, anchor="nw", image=tk_image)

diagonal_len = 20
for source in Source.sources:
    canvas.create_rectangle(get_draw_rect_coords(source, diagonal_len), fill='#00FF00', activeoutline='red')
for receiver in Receiver.receivers:
    canvas.create_rectangle(get_draw_rect_coords(receiver, diagonal_len), fill='#FF0000', activeoutline='red')
for reflector in Reflector.reflectors:
    canvas.create_line(get_draw_line_coords(reflector), fill="purple", width=5, activefill = 'red')

color = []
for idx in range(0, len(Ray.rays), 6):
        if len(color) == 0:
            color = ["yellow", "orange", "blue"]
        cur_color = color.pop()
        for ray_num in range(6):
            new_var = draw_rays(Ray.rays[ray_num+idx], cur_color)

canvas.pack()
top.mainloop()
