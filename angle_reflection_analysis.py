from Receiver import Receiver
from Source import Source
from Reflector import Reflector
from PIL import Image, ImageDraw

scale = 10
r1 = Receiver((240*scale, 10*scale))
s1 = Source((10*scale, 10*scale))
ref1 = Reflector((75*scale, 30*scale), (175*scale, 30*scale))

room_size = (250*scale, 125*scale)
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