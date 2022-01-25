'''
TODO Tests...
TODO add better documentation
TODO Pickle the image in the saved file. do this by converting to string/bytes
TODO make it so image_scale gets pickled and updated on load.
TODO make global variable not lists.
TODO add ability to change scale
TODO group buttons in their own grids like fr_buttons for better
TODO allow fractional step movements
TODO add labels for angle/position of each reflector
'''

from geometric_elements import Reflector, Ray, Receiver, Source
from PIL import Image, ImageDraw, ImageTk
import math
import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pickle

def get_draw_line_coords(obj):
    '''returns the scaled coordinates for each end of a line as a tuple, to be drawn on the canvas'''
    x0, y0 = obj.get_start_coords()
    x1, y1 = obj.get_end_coords()
    x0, y0, x1, y1 = (el*scale for el in (x0, y0, x1, y1))
    return (x0, y0, x1, y1)

def rotate_tkinter_line(current_coords, pivot=None, angle=None):
    '''takes a tkinter line coordinates and rotates about the pivot point by the specified angle'''
    if angle == None: # TODO I think this could be handled as a default parameter.
        angle = math.pi/2
    new_x0, new_y0, new_x1, new_y1 = current_coords
    new_x_mid, new_y_mid = ((new_x0 + new_x1)/2, (new_y0 + new_y1)/2)

    #shift the line to the origin
    if pivot == (new_x0, new_y0) or pivot == None: # TODO could probably also be handled as default parameter
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

    # rotate about the origin
    x0 = trans_x0*math.cos(angle) - trans_y0*math.sin(angle)
    x1 = trans_x1*math.cos(angle) - trans_y1*math.sin(angle)
    y0 = trans_x0*math.sin(angle) + trans_y0*math.cos(angle)
    y1 = trans_x1*math.sin(angle) + trans_y1*math.cos(angle)

    # shift back to original positition
    if pivot == (new_x0, new_y0) or pivot == None: # TODO handle as default parameter
        x0 += new_x0
        x1 += new_x0
        y0 += new_y0
        y1 += new_y0
    elif pivot == (new_x1, new_y1):
        x0 += new_x1
        x1 += new_x1
        y0 += new_y1
        y1 += new_y1
    elif pivot == (new_x_mid, new_y_mid):
        x0 += new_x_mid
        x1 += new_x_mid
        y0 += new_y_mid
        y1 += new_y_mid

    return (x0, x1, y0, y1)

def get_draw_rect_coords(obj, diagonal_len):
    '''returns the scaled coordinates for the center of a rectangle, to be drawn on the canvas'''
    x, y = obj.get_coords()
    x, y = (el*scale for el in (x, y))
    return (x-diagonal_len, y-diagonal_len, x+diagonal_len, y+diagonal_len)

def create_rays_2_reflector(source_obj, ref_obj):
    '''creates 3 Ray objects originating from the source and leading to each end + the middle of the specified Reflector object. NOT scaled.'''
    ray_2_start = Ray(source_obj.get_coords(), ref_obj.get_start_coords())
    ray_2_center = Ray(source_obj.get_coords(), ref_obj.get_center_coords())
    ray_2_end = Ray(source_obj.get_coords(), ref_obj.get_end_coords())
    return (ray_2_start, ray_2_center, ray_2_end)

def update_reflected_rays():
    '''generates 3 Ray objects from each source to each reflector. leading to each end and middle of the reflectors.'''
    Ray.rays.clear()
    for source in Source.sources:
        for reflector in Reflector.reflectors:
            Ray(source.get_coords(), reflector.get_start_coords())
            Ray(source.get_coords(), reflector.get_center_coords())
            Ray(source.get_coords(), reflector.get_end_coords())

            #reflector, reflecting rays
            #rotate 90 degrees around either coordinate
            ray_temp = Ray(reflector.get_start_coords(), reflector.get_end_coords())
            ray_temp.rotate(angle=-math.pi/2)
            #translate so one point starts on source
            ray_temp.move(source.get_coords())
            #extend to intersection of ref
                # intersection = get_intersection_of_two_lines(reflector, ray_temp)
            intersection = reflector.get_intersection_of_2_lines(ray_temp)
            ray_temp.set_end_coords(intersection)
            # rotate
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

            reflect_ray_2_start.move(reflector.get_start_coords())
            reflect_ray_2_center.move(reflector.get_center_coords())
            reflect_ray_2_end.move(reflector.get_end_coords())
            for ref_ray in reflected_rays:
                ref_ray.extend(room_size)
            # that is new start point of reflected line.

            # return (ray_2_start, ray_2_center, ray_2_end, reflect_ray_2_start, reflect_ray_2_center, reflect_ray_2_end)

def draw_rays():
    '''first removes all old rays on the screen, then draws new rays from Ray.rays list'''
    for key in drawing_to_internal_data_mapping:
        if isinstance(drawing_to_internal_data_mapping[key], Ray):
            canvas.delete(key)
    color = []
    for idx in range(0, len(Ray.rays), 6):
        if len(color) == 0:
            color = ["yellow", "orange", "blue", "black", "red", "cyan", "magenta", "green"]
        cur_color = color.pop()
        for ray_num in range(6):
            this_ray = Ray.rays[ray_num+idx]
            this_id = canvas.create_line(get_draw_line_coords(this_ray), fill=cur_color, width=3)
            drawing_to_internal_data_mapping[this_id] = this_ray

def draw_all_room_entities():
    '''clears the current item, canvas, mappings between drawing/internal data, images. Then redraws from Source.sources, Reflector.reflectors, Receiver.receivers, Ray.rays, any image file available'''
    current_item.clear()
    canvas.delete("all")
    drawing_to_internal_data_mapping.clear()
    images.clear()
    if len(image_filepaths) != 0:
        draw_image()
    elif len(images) != 0:
        draw_image()
    else:
        canvas.create_rectangle(0, 0, canvas_size[0], canvas_size[1], fill='gray')
    diagonal_len = 20
    for source in Source.sources:
        this_id = canvas.create_rectangle(get_draw_rect_coords(source, diagonal_len), fill='#00FF00', activeoutline='red')
        drawing_to_internal_data_mapping[this_id] = source
    for receiver in Receiver.receivers:
        this_id = canvas.create_rectangle(get_draw_rect_coords(receiver, diagonal_len), fill='#FF0000', activeoutline='red')
        drawing_to_internal_data_mapping[this_id] = receiver
    for reflector in Reflector.reflectors:
        this_id = canvas.create_line(get_draw_line_coords(reflector), fill="purple", width=5, activefill = 'red')
        drawing_to_internal_data_mapping[this_id] = reflector
    update_reflected_rays()
    draw_rays()

def save_file():
    '''pickles a dict containing: scale, roomsize, sources, reflectors, receivers, image_filepath'''
    filepath = asksaveasfilename(defaultextension="pickle")
    if not filepath:
        return

    data = {}
    data['scale'] = scale_and_room_size_list_for_saving[0]
    data['room size'] = scale_and_room_size_list_for_saving[1]
    data['sources'] = Source.sources
    data['reflectors'] = Reflector.reflectors
    data['receivers'] = Receiver.receivers
    if len(image_filepaths) != 0:
        data['image_filepath'] = image_filepaths[0]
    with open(filepath, 'wb') as output_file:
        pickle.dump(data, output_file)

def open_file():
    '''choose the file to open, load json, draw all room entities'''
    filepath = askopenfilename(filetypes=[("Pickle Files", "*.pickle")])
    if not filepath:
        return
    with open(filepath, "rb") as input_file:
        data = pickle.load(input_file)
    load_pickle(data)

    draw_all_room_entities()

def load_pickle(data):
    '''clear all internal data, delete canvas, delete images/image_filepath, load variables from pickled data.'''
    Source.sources.clear()
    Reflector.reflectors.clear()
    Receiver.receivers.clear()
    Ray.rays.clear()
    canvas.delete('all')
    images.clear()
    image_filepaths.clear()
    scale = data['scale']
    room_size = data['room size']

    if 'image_filepath' in data.keys():
        image_filepaths.append(data['image_filepath'])
    scale_and_room_size_list_for_saving = [scale, room_size]
    canvas_size = tuple(x*scale for x in room_size)
    canvas.config(width=canvas_size[0], height=canvas_size[1])
    canvas.create_rectangle(0, 0, canvas_size[0], canvas_size[1], fill='gray')
    canvas.grid(row=0, column=1, sticky='nsew')
    for source in data["sources"]:
        Source.sources.append(source)
    for reflector in data['reflectors']:
        Reflector.reflectors.append(reflector)
    for receiver in data['receivers']:
        Receiver.receivers.append(receiver)

def on_drawing_element_click(event):
    '''update current item to clicked element'''
    if len(current_item) != 0:
        current_item.pop()
    current_item.append(event.widget.find_withtag("current"))
    print(current_item[0])

def on_move_down_button():
    '''update coords in internal data and redraw room'''
    step = move_and_rotate_steps[0]*scale
    canvas.move(current_item[0], 0, abs(step))
    #move data
    cur_int_data_el = drawing_to_internal_data_mapping[current_item[0][0]]
    cur_int_data_el.move_down(abs(step/scale))
    #redraw rays
    update_reflected_rays()
    draw_rays()

def on_move_up_button():
    '''update coords in internal data and redraw room'''
    step = move_and_rotate_steps[0]*scale
    canvas.move(current_item[0], 0, -abs(step))
    #move data
    cur_int_data_el = drawing_to_internal_data_mapping[current_item[0][0]]
    cur_int_data_el.move_up(abs(step/scale))
    #redraw rays
    update_reflected_rays()
    draw_rays()

def on_move_right_button():
    '''update coords in internal data and redraw room'''
    step = move_and_rotate_steps[0]*scale
    canvas.move(current_item[0], abs(step), 0)
    #move data
    cur_int_data_el = drawing_to_internal_data_mapping[current_item[0][0]]
    cur_int_data_el.move_right(abs(step/scale))
    #redraw rays
    update_reflected_rays()
    draw_rays()

def on_move_left_button():
    '''update coords in internal data and redraw room'''
    step = move_and_rotate_steps[0]*scale
    canvas.move(current_item[0], -abs(step), 0)
    #move data
    cur_int_data_el = drawing_to_internal_data_mapping[current_item[0][0]]
    cur_int_data_el.move_left(abs(step/scale))
    #redraw rays
    update_reflected_rays()
    draw_rays()

def on_lcr_choice_LEFT(): # TODO update LCR variable name
    '''update lcr flag based on button clicked'''
    if len(lcr_flag) != 0:
        lcr_flag.clear()
    lcr_flag.append("left")

def on_lcr_choice_CENTER():  # TODO update LCR variable name
    '''update lcr flag based on button clicked'''
    if len(lcr_flag) != 0:
        lcr_flag.clear()
    lcr_flag.append("center")

def on_lcr_choice_RIGHT():  # TODO update LCR variable name
    '''update lcr flag based on button clicked'''
    if len(lcr_flag) != 0:
        lcr_flag.clear()
    lcr_flag.append("right")

def update_drawing_reflector_after_rotation(internal_item):
    '''updates reflector drawing based on internal item coords'''
    start_coords = internal_item.get_start_coords()
    end_coords = internal_item.get_end_coords()
    new_drawing_coords = (start_coords[0]*scale, start_coords[1]*scale, end_coords[0]*scale, end_coords[1]*scale)
    canvas.coords(current_item[0], new_drawing_coords)

def on_rotate_clockwise_button():
    '''CLOCKWISE - updates internal data of reflector based on rotation, updates reflector drawing, updates rays and ray drawings'''
    cur_int_data_el = drawing_to_internal_data_mapping[current_item[0][0]]
    if not isinstance(cur_int_data_el, Reflector):
        return
    step = move_and_rotate_steps[1] #degrees
    step *= math.pi/180 #radians
    if lcr_flag[0] == "left":
        cur_int_data_el.rotate(pivot=cur_int_data_el.get_start_coords(), angle=step)
    elif lcr_flag[0] == "center":
        cur_int_data_el.rotate(pivot=cur_int_data_el.get_center_coords(), angle=step)
    elif lcr_flag[0] == "right":
        cur_int_data_el.rotate(pivot=cur_int_data_el.get_end_coords(), angle=step)
    update_drawing_reflector_after_rotation(cur_int_data_el)
    update_reflected_rays()
    draw_rays()

def on_rotate_counterclockwise_button(): # TODO maybe combine this with the clockwise function
    '''COUNTERCLOCKWISE - updates internal data of reflector based on rotation, updates reflector drawing, updates rays and ray drawings'''
    cur_int_data_el = drawing_to_internal_data_mapping[current_item[0][0]]
    if not isinstance(cur_int_data_el, Reflector):
        return
    step = -move_and_rotate_steps[1] #degrees
    step *= math.pi/180 #radians
    if lcr_flag[0] == "left":
        cur_int_data_el.rotate(pivot=cur_int_data_el.get_start_coords(), angle=step)
    elif lcr_flag[0] == "center":
        cur_int_data_el.rotate(pivot=cur_int_data_el.get_center_coords(), angle=step)
    elif lcr_flag[0] == "right":
        cur_int_data_el.rotate(pivot=cur_int_data_el.get_end_coords(), angle=step)
    update_drawing_reflector_after_rotation(cur_int_data_el)
    update_reflected_rays()
    draw_rays()

def update_move_step():
    '''updates the distance by which an object is moved (also updates the label)'''
    move_and_rotate_steps[0] = int(entry_box.get()) # TODO update this so you can do fractional steps
    step_lable.configure(text=f'{move_and_rotate_steps[0]} (ft), {move_and_rotate_steps[1]} (deg)')

def update_rotate_step():
    '''updates the angle by which an reflector is rotated (also updates the label)'''
    move_and_rotate_steps[1] = int(entry_box.get()) # TODO update this so you can do fractional angles??? (maybe not fractional degrees)
    step_lable.configure(text=f'{move_and_rotate_steps[0]} (ft), {move_and_rotate_steps[1]} (deg)')

def user_draw_source(event):
    '''takes the location of mouse click and creates an unscaled Source object version, redraws everything'''
    insert_at_coords = (canvas.canvasx(event.x)/scale, canvas.canvasy(event.y)/scale)
    Source(insert_at_coords)
    draw_all_room_entities()

def user_draw_start_reflector(event):
    '''handles the start of a reflector drawing. also updates this to be the current item. Only handles drawing, no internal data. '''
    if len(current_item) != 0:
        current_item.clear()
    start_at_coords = (canvas.canvasx(event.x), canvas.canvasy(event.y))
    this_id = canvas.create_line(start_at_coords, start_at_coords, fill="purple", width=5, activefill = 'red')
    current_item.append(this_id)

def user_draw_move_reflector(event):
    '''handles the reflector drawing while the mouse is moving but click hasn't released. Only updates drawing, nothing with internal data'''
    new_coords_end = (canvas.canvasx(event.x), canvas.canvasy(event.y))
    cur_coords = canvas.coords(current_item[0])
    start_coords = (cur_coords[0], cur_coords[1])
    canvas.coords(current_item[0], start_coords[0], start_coords[1], new_coords_end[0], new_coords_end[1])

def user_draw_end_reflector(event):
    '''handles the reflector drawing when mouseclick is released. creates Reflector object based on un-scaled coordinates. '''
    new_coords_end = (canvas.canvasx(event.x), canvas.canvasy(event.y))
    cur_coords = canvas.coords(current_item[0])
    start_coords = (cur_coords[0], cur_coords[1])
    canvas.coords(current_item[0], start_coords[0], start_coords[1], new_coords_end[0], new_coords_end[1])
    Reflector((x/scale for x in start_coords), (x/scale for x in new_coords_end))
    # canvas.delete("all")
    draw_all_room_entities()
    current_item.clear() # TODO maybe I want to keep it active?

def user_draw_receiver(event):
    '''takes the location of mouse click and creates an unscaled Receiver object version, redraws everything'''
    insert_at_coords = (canvas.canvasx(event.x)/scale, canvas.canvasy(event.y)/scale)
    Receiver(insert_at_coords)
    draw_all_room_entities()

def bind_to_draw_source():
    '''unbinds left click/release/motion, binds left click to appropriate function'''
    unbind_all()
    canvas.bind("<ButtonPress-1>", user_draw_source)

def bind_to_draw_reflector():
    '''unbinds left click/release/motion, binds left click/release/motion to appropriate function'''
    unbind_all()
    temp_line = canvas.bind("<ButtonPress-1>", user_draw_start_reflector)
    canvas.bind("<B1-Motion>", user_draw_move_reflector)
    canvas.bind("<ButtonRelease-1>", user_draw_end_reflector)

def bind_to_draw_receiver():
    '''unbinds left click/release/motion, binds left click to appropriate function'''
    unbind_all()
    canvas.bind("<ButtonPress-1>", user_draw_receiver)

def bind_to_element_selector():
    '''unbinds left click/release/motion, binds left click to appropriate function'''
    unbind_all()
    canvas.bind('<Button-1>', on_drawing_element_click)

def unbind_all():
    '''unbinds left click/release/motion'''
    canvas.unbind("<ButtonPress-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

def clear_canvas():
    '''removes all objects from the object variable lists within Reflector/Ray/Source/Receiver classes, clears current_item/images/image_filepaths global vars, then redraws but there is nothing to redraw so blank slate.'''
    Reflector.reflectors.clear()
    Ray.rays.clear()
    Source.sources.clear()
    Receiver.receivers.clear()
    current_item.clear()
    images.clear()
    image_filepaths.clear()
    draw_all_room_entities()

def delete_active_item():
    '''removes the repr of the current item from the current data then redraws the room (which will now not include that item)'''
    print(type(current_item[0]))
    current_item_internal = drawing_to_internal_data_mapping[current_item[0][0]]
    if isinstance(current_item_internal, Source):
        Source.sources.remove(current_item_internal)
    elif isinstance(current_item_internal, Reflector):
        Reflector.reflectors.remove(current_item_internal)
    elif isinstance(current_item_internal, Receiver):
        Receiver.receivers.remove(current_item_internal)
    draw_all_room_entities()

def import_image():
    '''handles importing an image to the background'''
    filepath = askopenfilename(filetypes=[("jpeg", "*.jpg"), ("bitmap", "*.bmp"), ("png", "*.png")])
    if not filepath:
        return
    image_filepaths.clear()
    image_filepaths.append(filepath)
    draw_all_room_entities()

def draw_image(): # TODO clean this up
    '''handles the actual drawing of the imported image'''
    if len(images) != 0:
        image = images[0]
        # with Image.open("/Users/craigharris/Desktop/Screen Shot 2021-05-19 at 20.54.17.png") as image:
        image_width, image_height = (int(x/image_scale) for x in image.size)
        image = image.resize((image_width, image_height), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(image)
        # image_display_width = image_width
        # image_display_height = image_height
        # canvas.create_image(image_display_width/2, image_display_height/2, tag="base_drawing", image=tk_image)
        base_layer = canvas.create_image(0, 0, anchor='nw', tag="base_drawing", image=tk_image)
    else:
        images.clear()
        try:
            with Image.open(image_filepaths[0]) as image:
                image_width, image_height = (int(x/image_scale) for x in image.size)
                image_resize = image.resize((image_width, image_height), Image.LANCZOS)
                tk_image = ImageTk.PhotoImage(image_resize)
                # image_display_width = image_width
                # image_display_height = image_height
                # canvas.create_image(image_display_width/2, image_display_height/2, tag="base_drawing", image=tk_image)
                base_layer = canvas.create_image(0, 0, anchor='nw', tag="base_drawing", image=tk_image)
        except FileNotFoundError:
            if '/' in image_filepaths[0]: # mac paths
                temp_filepath = image_filepaths[0].split('/')[-1]
            elif '\\' in image_filepaths[0]: # windows paths
                temp_filepath = image_filepaths[0].split('\\')[-1]

            with Image.open(temp_filepath) as image:
                image_width, image_height = (int(x/3) for x in image.size)
                image_resize = image.resize((image_width, image_height), Image.LANCZOS)
                tk_image = ImageTk.PhotoImage(image_resize)
                # image_display_width = image_width
                # image_display_height = image_height
                # canvas.create_image(image_display_width/2, image_display_height/2, tag="base_drawing", image=tk_image)
                base_layer = canvas.create_image(0, 0, anchor='nw', tag="base_drawing", image=tk_image)

    images.append(tk_image)  # you need to keep a reference to the tk_image or the garbage collector removes it

image_scale = 2
image_filepaths = []
images = []
move_and_rotate_steps = [1, 1]
lcr_flag = []
drawing_to_internal_data_mapping = {}
current_item = []
scale = 10
room_size = (75.989, 45.38)
# room_size = (120, 90) # TODO delete
scale_and_room_size_list_for_saving = [scale, room_size]

# default rm
s1_pos = (74.007, 45.38-6.773)
r1_pos = (5.102, 45.38-20.266)
r2_pos = (10.824, 45.38-17.093)
r3_pos = (16.574, 45.38-14.468)
r4_pos = (22.407, 45.38-11.926)
r5_pos = (28.785, 45.38-9.885)
r6_pos = (31.838, 45.38-8.231)
ref1_pos0 = (27.511, 45.38-34.238)
ref1_pos1 = (15.604, 45.38-33.137)
ref2_pos0 = (59.351, 45.38-31.253)
ref2_pos1 = (48.198, 45.38-35.313)
ref3_pos0 = (73.362, 45.38-25.586)
ref3_pos1 = (62.188, 45.38-29.653)
ref4_pos0 = (10, 10)
ref4_pos1 = (10, 20)

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
# ref4 = Reflector(ref4_pos0, ref4_pos1)
ref3.rotate(pivot=ref3.get_center_coords(), angle=5*math.pi/180)
ref2.rotate(pivot=ref2.get_start_coords(), angle=-6*math.pi/180)
ref1.rotate(pivot=ref1.get_start_coords(), angle=-6*math.pi/180)
# ref1.move_vertical(-10)

if room_size == None:
    canvas_size = (760, 450)
else:
    canvas_size = tuple(x*scale for x in room_size)

#tkinter
window = tkinter.Tk()
window.title("this is the title2222")

canvas = tkinter.Canvas(width=canvas_size[0], height=canvas_size[1], cursor="cross")

bind_to_element_selector() # default set the left click to select objects

#configure the frame, widgets, buttons
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)
fr_buttons = tkinter.Frame(window)
btn_open = tkinter.Button(fr_buttons, text='Open', command=open_file)
btn_save = tkinter.Button(fr_buttons, text='Save As...', command=save_file)
spacer1 = tkinter.Label(fr_buttons, text='')
btn_draw_source = tkinter.Button(fr_buttons, text='Draw Source', command=bind_to_draw_source)
btn_draw_reflector = tkinter.Button(fr_buttons, text='Draw Reflector', command=bind_to_draw_reflector)
btn_draw_receiver = tkinter.Button(fr_buttons, text='Draw Receiver', command=bind_to_draw_receiver)
spacer2 = tkinter.Label(fr_buttons, text='')
btn_move_active_obj_up = tkinter.Button(fr_buttons, text='Move Up', command=on_move_up_button)
btn_move_active_obj_down = tkinter.Button(fr_buttons, text='Move Down', command=on_move_down_button)
btn_move_active_obj_right = tkinter.Button(fr_buttons, text='Move Right', command=on_move_right_button)
btn_move_active_obj_left = tkinter.Button(fr_buttons, text='Move Left', command=on_move_left_button)
spacer3 = tkinter.Label(fr_buttons, text='')
btn_l = tkinter.Button(fr_buttons, text='L', command=on_lcr_choice_LEFT)
btn_c = tkinter.Button(fr_buttons, text='C', command=on_lcr_choice_CENTER)
btn_r = tkinter.Button(fr_buttons, text='R', command=on_lcr_choice_RIGHT)
btn_rotate_active_obj_clockwise = tkinter.Button(fr_buttons, text='Rotate Clockwise', command=on_rotate_clockwise_button)
btn_rotate_active_obj_counterclockwise = tkinter.Button(fr_buttons, text='Rotate Counterclockwise', command=on_rotate_counterclockwise_button)
btn_updt_move_step = tkinter.Button(fr_buttons, text = "Update Move Step (ft)", command=update_move_step)
btn_updt_angle_step = tkinter.Button(fr_buttons, text = "Update Angle Step (deg)", command=update_rotate_step)
entry_box = tkinter.Entry(fr_buttons, textvariable=5)
step_lable = tkinter.Label(fr_buttons, text=f"{move_and_rotate_steps[0]} (ft), {move_and_rotate_steps[1]} (deg)")
entry_box.insert(0, "input num val & click update")
entry_box.focus()
btn_selector = tkinter.Button(fr_buttons, text = "Select", command=bind_to_element_selector)
spacer4 = tkinter.Label(fr_buttons, text='')
btn_clear_canvas = tkinter.Button(fr_buttons, text = "Clear Canvas", command=clear_canvas)
btn_delete_active_item = tkinter.Button(fr_buttons, text="Delete Active Item", command=delete_active_item)
btn_import_image = tkinter.Button(fr_buttons, text="Import Image", command=import_image)

# place buttons in grid
btn_open.grid(row=0, column=0, columnspan=6,  sticky="ew", padx=5)
btn_save.grid(row=1, column=0, columnspan=6,  sticky="ew", padx=5)
spacer1.grid(row=2, column=0, columnspan=6,  sticky='ew', padx=5)
btn_draw_source.grid(row=3, column=0, columnspan=6,  sticky="ew", padx=5)
btn_draw_reflector.grid(row=4, column=0, columnspan=6,  sticky="ew", padx=5)
btn_draw_receiver.grid(row=5, column=0, columnspan=6,  sticky="ew", padx=5)
spacer2.grid(row=6, column=0, columnspan=6,  sticky='ew', padx=5)
btn_move_active_obj_up.grid(row=7, column=0, columnspan=6, sticky='ew', padx=5)
btn_move_active_obj_down.grid(row=9, column=0, columnspan=6, sticky='ew', padx=5)
btn_move_active_obj_right.grid(row=8, column=3, columnspan=3, sticky='ew', padx=5)
btn_move_active_obj_left.grid(row=8, column=0, columnspan=3, sticky='ew', padx=5)
spacer3.grid(row=11, column=0, columnspan=6,  sticky='ew', padx=5)
btn_l.grid(row=12, column=0, columnspan=2,  sticky='ew', padx=5)
btn_c.grid(row=12, column=2, columnspan=2, sticky='ew', padx=5)
btn_r.grid(row=12, column=4, columnspan=2, sticky='ew', padx=5)
btn_rotate_active_obj_clockwise.grid(row=15, column=0, columnspan=6,  sticky='ew', padx=5)
btn_rotate_active_obj_counterclockwise.grid(row=16, column=0, columnspan=6,  sticky='ew', padx=5)
btn_updt_move_step.grid(row=17, column=0, columnspan=6, sticky='ew', padx=5)
btn_updt_angle_step.grid(row=18, column=0,columnspan=6,  sticky='ew', padx=5)
entry_box.grid(row=19, column=0, columnspan=6, sticky='ew', padx=5)
step_lable.grid(row=20, column=0, columnspan=6, sticky='ew', padx=5)
btn_selector.grid(row = 21, column=0, columnspan=6, sticky='ew', padx=5)
spacer4.grid(row = 22, column=0, columnspan=6, sticky='ew', padx=5)
btn_clear_canvas.grid(row=23, column=0, columnspan=6, sticky='ew', padx=5)
btn_delete_active_item.grid(row=24, column=0, columnspan=6, sticky='ew', padx=5)
btn_import_image.grid(row=25, column=0, columnspan=6, sticky='ew', padx=5)

#place widgets in grid
fr_buttons.grid(row=0, column=0, sticky='ns')
canvas.grid(row=0, column=1, sticky='nsew')


draw_all_room_entities()
window.mainloop()

