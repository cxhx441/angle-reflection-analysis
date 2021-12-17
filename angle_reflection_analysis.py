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
    reflect_ray_2_start.set_end_coords(ref1.get_start_coords())
    reflect_ray_2_center.set_end_coords(ref1.get_center_coords())
    reflect_ray_2_end.set_end_coords(ref1.get_end_coords())

    reflected_rays = (reflect_ray_2_start, reflect_ray_2_center, reflect_ray_2_end)
    for ref_ray in reflected_rays:
        ref_ray.extend(room_size)

    reflect_ray_2_start.move(ref1.get_start_coords())
    reflect_ray_2_center.move(ref1.get_center_coords())
    reflect_ray_2_end.move(ref1.get_end_coords())
    # that is new start point of reflected line.

    rays = (ray_2_start, ray_2_center, ray_2_end, reflect_ray_2_start, reflect_ray_2_center, reflect_ray_2_end)

    return (ray_2_start, ray_2_center, ray_2_end, reflect_ray_2_start, reflect_ray_2_center, reflect_ray_2_end)

def draw_rays(rays):
    #draw them
    ray1_2_ref = canvas.create_line(get_draw_line_coords(rays[0]), fill="yellow", width=3)
    ray2_2_ref = canvas.create_line(get_draw_line_coords(rays[1]), fill="yellow", width=3)
    ray3_2_ref = canvas.create_line(get_draw_line_coords(rays[2]), fill="yellow", width=3)
    ref_ray1_2_ref = canvas.create_line(get_draw_line_coords(rays[3]), fill="yellow", width=2)
    ref_ray2_2_ref = canvas.create_line(get_draw_line_coords(rays[4]), fill="yellow", width=2)
    ref_ray3_2_ref = canvas.create_line(get_draw_line_coords(rays[5]), fill="yellow", width=2)

    return (ray1_2_ref, ray2_2_ref, ray3_2_ref, ref_ray1_2_ref, ref_ray2_2_ref, ref_ray3_2_ref)

scale = 10

room_size = (85, 43)
# room_size = (160, 43) # TODO delete this
s1_pos = (84.5, 8.75)
r1_pos = (32, 11)
ref1_pos0 = (66, 31.83)
ref1_pos1 = (55, 35.83)

# get_reflector_to_edge

s1 = Source(s1_pos)
r1 = Receiver(r1_pos)
ref1 = Reflector(ref1_pos0, ref1_pos1)
ref1.rotate(pivot=ref1.get_center_coords(), angle=11*math.pi/180)
rays1 = get_reflected_rays(s1, ref1)

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
rays = draw_rays(rays1)

canvas.pack()
top.mainloop()
