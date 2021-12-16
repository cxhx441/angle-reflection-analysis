from Receiver import Receiver
from Source import Source
from Reflector import Reflector
from PIL import Image, ImageDraw, ImageTk

import tkinter
from tkinter import ttk


class Editor(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.canvas_width, self.canvas_height = room_size
        self.canvas = tkinter.Canvas(self, width=self.canvas_width , height=self.canvas_height, cursor="cross")
        self.image = Image.new('RGB' , room_size, bckgrnd_clr)

        self.image = Image.open('fake_image.png')
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.config(scrollregion=(0, 0, self.canvas_width, self.canvas_height)) #giving scrollbars

        self.canvas.create_image(0,0, anchor="nw", image=self.tk_image)
        self.draw_shapes()

        

    def draw_shapes(self):
        offset = 20
        self.source = self.canvas.create_rectangle(x-offset, y-offset, x+offset, y+offset, fill='#00FF00', activeoutline='red')
        self.receiver = self.canvas.create_rectangle(x-offset, y-offset, x+offset, y+offset, fill='#FF0000', activeoutline='red')
        x0, y0 = tuple((x*scale for x in ref1.get_start_coords()))
        x1, y1 = tuple((x*scale for x in ref1.get_end_coords()))
        self.reflector = self.canvas.create_line(x0, y0, x1, y1, fill="purple", width=5)

scale = 10

s1_pos = (10, 10)
r1_pos = (140, 10)
ref1_pos0 = (50, 25)
ref1_pos1 = (100, 25)
room_size = (150, 30)

s1 = Source(tuple(x*scale for x in s1_pos))
r1 = Receiver(tuple(x*scale for x in r1_pos))
ref1 = Reflector(tuple(x*scale for x in ref1_pos0), tuple(x*scale for x in ref1_pos1))

# room_size = (250*scale, 125*scale)
room_size = tuple(x*scale for x in room_size)
bckgrnd_clr = (128, 128, 128)
im = Image.new('RGB', room_size, bckgrnd_clr)
draw = ImageDraw.Draw(im)
draw.line((ref1.get_start_coords(), ref1.get_end_coords()), fill = 0)

x, y = s1.get_coords()
y = room_size[1]-y
thick = 5*scale
draw.rectangle((x - thick, y - thick, x + thick, y + thick), fill = (0,255,0), outline=(255, 255, 255))

x, y = r1.get_coords()
y = room_size[1]-y
thick = 5*scale
draw.rectangle((x - thick, y - thick, x + thick, y + thick), fill = (255,0,0), outline=(255, 255, 255))

im.show()


top = tkinter.Tk()
# mainApp.pack(side="top", fill="both", expand = True)

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
x0, y0 = ref1.get_start_coords()
x1, y1 = ref1.get_end_coords()
y0 = room_size[1] - y0
y1 = room_size[1] - y1
reflector = C.create_line(x0, y0, x1, y1, fill="purple", width=5)

C.pack()
top.mainloop()

# class Main_Application(tkinter.Frame):
#     def __init__(self, parent):
#             tkinter.Frame.__init__(self) # , parent
#             self.parent = parent
#             self.editor = Editor(self)

# def main(): 
#     root = tkinter.Tk()
#     mainApp = Main_Application(root)
#     # mainApp.pack(side="top", fill="both", expand = True)
#     mainApp.pack()
#     # root.geometry('+0+0')
#     root.mainloop()

# if __name__ == '__main__':
#     main()