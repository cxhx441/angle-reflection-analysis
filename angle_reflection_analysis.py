from Receiver import Receiver
from Source import Source
from Reflector import Reflector
from PIL import Image, ImageDraw, ImageTk

import tkinter
from tkinter import ttk

def get_draw_line_coords(obj):
    x0, y0 = obj.get_start_coords()
    x1, y1 = obj.get_end_coords()
    y0 = room_size[1] - y0
    y1 = room_size[1] - y1
    return (x0, y0, x1, y1)

def get_draw_rect_coords(obj, diagonal_len):
    x, y = r1.get_coords()
    y = room_size[1] - y
    return (x-diagonal_len, y-diagonal_len, x+diagonal_len, y+diagonal_len)

scale = 10

s1_pos = (10, 10)
r1_pos = (140, 10)
ref1_pos0 = (50, 25)
ref1_pos1 = (100, 25)
room_size = (150, 30)

s1 = Source(tuple(x*scale for x in s1_pos))
r1 = Receiver(tuple(x*scale for x in r1_pos))
ref1 = Reflector(tuple(x*scale for x in ref1_pos0), tuple(x*scale for x in ref1_pos1))

room_size = tuple(x*scale for x in room_size)
bckgrnd_clr = (128, 128, 128)
im = Image.new('RGB', room_size, bckgrnd_clr)
draw = ImageDraw.Draw(im)
draw.line((ref1.get_start_coords(), ref1.get_end_coords()), fill = 0)
diagonal_len = 5
draw.rectangle(get_draw_rect_coords(s1, diagonal_len), fill = (0,255,0), outline=(255, 255, 255))
draw.rectangle(get_draw_rect_coords(r1, diagonal_len), fill = (255,0,0), outline=(255, 255, 255))


#tkinterk
top = tkinter.Tk()

canvas_width, canvas_height = room_size
C = tkinter.Canvas(width=canvas_width , height=canvas_height, cursor="cross")
image = Image.new('RGB' , room_size, bckgrnd_clr)
tk_image = ImageTk.PhotoImage(image)

C.create_image(0,0, anchor="nw", image=tk_image)

offset = 20
x, y = s1.get_coords()
y = room_size[1] - y
source = C.create_rectangle(x-offset, y-offset, x+offset, y+offset, fill='#00FF00', activeoutline='red')
x, y = r1.get_coords()
y = room_size[1] - y
receiver = C.create_rectangle(x-offset, y-offset, x+offset, y+offset, fill='#FF0000', activeoutline='red')

reflector = C.create_line(get_draw_line_coords(ref1), fill="purple", width=5, activefill = 'red')

def get_draw_line(obj, diagonal_len):
    x, y = r1.get_coords()
    y = room_size[1] - y
    return (x-diagonal_line, y-diagonal_len, x+diagonal_line, y+diagonal_line)

    
C.pack()
top.mainloop()