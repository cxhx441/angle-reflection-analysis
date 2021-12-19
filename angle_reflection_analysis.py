#TODO make it so that the objects have the correct dimensions, but the drawing scales

from Receiver import Receiver
from Source import Source
from Reflector import Reflector
from PIL import Image, ImageDraw, ImageTk

import tkinter
from tkinter import ttk

def get_draw_line_coords(obj):
    x0, y0 = ref1.get_start_coords()
    x1, y1 = ref1.get_end_coords()
    y0 = room_size[1] - y0
    y1 = room_size[1] - y1
    return (x0, y0, x1, y1)

def get_draw_rect_coords(obj, diagonal_length):
    x, y = obj.get_coords()
    y = room_size[1] - y
    return (x-diagonal_length, y-diagonal_length, x+diagonal_length, y+diagonal_length)

scale = 10

# x, y in whatever units
room_size = (85, 45)
s1_pos = (83, 9)
r1_pos = (25, 14)
ref1_pos0 = (55, 35)
ref1_pos1 = (66, 32)

# creating objects at scaling
room_size = tuple(x*scale for x in room_size)
s1 = Source(tuple(x*scale for x in s1_pos))
r1 = Receiver(tuple(x*scale for x in r1_pos))
ref1 = Reflector(tuple(x*scale for x in ref1_pos0), tuple(x*scale for x in ref1_pos1))

#tkinter
top = tkinter.Tk()

room_offset = 40
canvas_width, canvas_height = tuple((x+room_offset for x in room_size))
canvas = tkinter.Canvas(width=canvas_width , height=canvas_height, cursor="cross")
image = Image.new('RGB' , (canvas_width, canvas_height), (128, 128, 128))
tk_image = ImageTk.PhotoImage(image)

#room, canvas
canvas.create_image(0,0, anchor="nw", image=tk_image)
canvas.create_rectangle(0 + room_offset, 0 + room_offset, room_size[0], room_size[1])

#sources, receivers, reflectors
diagonal_length = 15
source = canvas.create_rectangle(get_draw_rect_coords(s1, diagonal_length), fill='#00FF00', activeoutline='red')
receiver = canvas.create_rectangle(get_draw_rect_coords(r1, diagonal_length), fill='#FF0000', activeoutline='red')
reflector = canvas.create_line(get_draw_line_coords(ref1), fill="purple", width=3, activefill="red")

canvas.pack()
top.mainloop()
