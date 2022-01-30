import tkinter as tk
from Room import Room
from geometric_elements import Ray


class DrawingArea(tk.Canvas):
    """
    TODO
    The drawings area frame
    """
    def __init__(self, container):
        super().__init__(container, cursor="dot")
        self.container = container
        # create sunken look
        self['relief'] = 'sunken'
        self['borderwidth'] = 2
        self['bg'] = 'gray'

        self._draw_room()

    def _draw_room(self):

        self._draw_image()

        diagonal_len = 20
        print(self.container.test_var)
        for source in self.container.room.get_sources():
            this_id = self.create_rectangle(self._get_draw_rect_coords(source, diagonal_len), fill='#00FF00', activeoutline='red')
            self.container.drawing_to_internal_data_mapping[this_id] = source

        for receiver in self.container.room.get_receivers():
            this_id = self.create_rectangle(self._get_draw_rect_coords(receiver, diagonal_len), fill='#FF0000', activeoutline='red')
            self.container.drawing_to_internal_data_mapping[this_id] = receiver

        for reflector in self.container.room.get_reflectors():
            this_id = self.create_line(self._get_draw_line_coords(reflector), fill="purple", width=5, activefill = 'red')
            self.container.drawing_to_internal_data_mapping[this_id] = reflector
        
        rays_list = self.container.room.get_rays()
        for ray in rays_list:
            self._draw_rays(rays_list)

    
    def _get_draw_rect_coords(self, obj, diagonal_len):
        """
        returns the scaled coordinates for the center of a rectangle, to be drawn on the canvas
        """
        x, y = obj.get_coords()
        x, y = (el*self.container.pixel_per_foot_scale for el in (x, y))
        return (x-diagonal_len, y-diagonal_len, x+diagonal_len, y+diagonal_len)

    def _get_draw_line_coords(self, obj):
        """
        returns the scaled coordinates for each end of a line as a tuple, to be drawn on the canvas
        """
        x0, y0 = obj.get_start_coords()
        x1, y1 = obj.get_end_coords()
        x0, y0, x1, y1 = (el*self.container.pixel_per_foot_scale for el in (x0, y0, x1, y1))
        return (x0, y0, x1, y1)
    
    def _draw_rays(self, rays_list):
        '''first removes all old rays on the screen, then draws new rays from Ray.rays list'''
        for key in self.container.drawing_to_internal_data_mapping:
            if isinstance(self.container.drawing_to_internal_data_mapping[key], Ray):
                self.delete(key)
        color = []
        for idx in range(0, len(rays_list), 6):
            if len(color) == 0:
                color = ["yellow", "orange", "blue", "black", "red", "cyan", "magenta", "green"]
            cur_color = color.pop()
            for ray_num in range(6):
                this_ray = rays_list[ray_num+idx]
                this_id = self.create_line(self._get_draw_line_coords(this_ray), fill=cur_color, width=3)
                self.container.drawing_to_internal_data_mapping[this_id] = this_ray

    def _draw_image(self):
        pass


class FileManagementButtonFrame(tk.LabelFrame):
    """
    Handles the follow widgets:
        Open
        Save As...
        Import Image
    """
    def __init__(self, container):
        super().__init__(container, text="File Management")
        self.container = container
        self._create_widgits()

    def _create_widgits(self):
        btn_open = tk.Button(self, text = 'Open...')
        btn_save_as = tk.Button(self, text = 'Save As...')
        btn_import_image = tk.Button(self, text = 'Import Image...')

        btn_open.grid(row=0, column=0, sticky='ew')
        btn_save_as.grid(row=1, column=0, sticky='ew')
        btn_import_image.grid(row=2, column=0, sticky='ew')

class DrawingElementsButtonsFrame(tk.LabelFrame):
    """
    Handles the follow widgets:
        Draw Source
        Draw Reflector
        Draw Receiver
        Select
        Delete Active Item
        Clear Canvas
    """
    def __init__(self, container):
        super().__init__(container, text="Draw Tools")
        self.container = container
        self._create_widgits()

    def _create_widgits(self):
        btn_draw_source = tk.Button(self, text = 'Draw Source')
        btn_draw_reflector = tk.Button(self, text = 'Draw Reflector')
        btn_draw_receiver = tk.Button(self, text = 'Draw Receiver')
        btn_select = tk.Button(self, text = 'Select Element')
        btn_delete_active_element = tk.Button(self, text = 'Delete Active Element')
        btn_clear_drawing_area = tk.Button(self, text = 'Clear Drawing Area')

        btn_draw_source.grid(row=0, column=0)
        btn_draw_reflector.grid(row=1, column=0)
        btn_draw_receiver.grid(row=2, column=0)
        btn_select.grid(row=3, column=0)
        btn_delete_active_element.grid(row=4, column=0)
        btn_clear_drawing_area.grid(row=5, column=0)

        # give all buttons the sticky='EW'
        for child in self.winfo_children():
            if child.winfo_class() in ('Button'):
                child.grid_configure(sticky='EW')

class DisplacingElementsButtonsFrame(tk.LabelFrame):
    """
    Handles the follow widgets:
        Organizes the buttons:
        Move Up
        Move Left
        Move Right
        Move Down
    """
    def __init__(self, container):
        super().__init__(container, text='Move Tools')
        self.container = container
        self._create_widgits()

    def _create_widgits(self):
        btn_move_up = tk.Button(self, text='Move Up')
        btn_move_left = tk.Button(self, text='Move Left')
        btn_move_right = tk.Button(self, text='Move Right')
        btn_move_down = tk.Button(self, text='Move Down')
        
        btn_move_up.grid(row=0, columnspan=2)
        btn_move_left.grid(row=1, column=0)
        btn_move_right.grid(row=1, column=1)
        btn_move_down.grid(row=2, columnspan=2)

        # give all buttons the sticky='EW'
        for child in self.winfo_children():
            if child.winfo_class() in ('Button'):
                child.grid_configure(sticky='EW')

class RotatingElementsButtonsFrame(tk.LabelFrame):
    """
    Handles the follow widgets:
        L
        C
        R
        Rotate Clockwise
        Rotate Counterclockwise
    """
    def __init__(self, container):
        super().__init__(container, text='Rotate Tools')
        self.container = container
        self._create_widgits()

    def _create_widgits(self):
        btn_L = tk.Button(self, text='L')
        btn_C = tk.Button(self, text='C')
        btn_R = tk.Button(self, text='R')
        btn_rotate_clockwise = tk.Button(self, text='Rotate Clockwise')
        btn_rotate_counterclockwise = tk.Button(self, text='Rotate Counterclockwise')

        btn_L.grid(row=0, column=0)
        btn_C.grid(row=0, column=1)
        btn_R.grid(row=0, column=2)
        btn_rotate_clockwise.grid(row=1, columnspan=3)
        btn_rotate_counterclockwise.grid(row=2, columnspan=3)

        # give all buttons the sticky='EW'
        for child in self.winfo_children():
            if child.winfo_class() in ('Button'):
                child.grid_configure(sticky='EW')


class UpdateStepMoveRotateButtonsFrame(tk.LabelFrame):
    """
    Handles the follow widgets:
        Update Move Step (ft)
        Update Angle Step (deg)
        input_box for value
        label for dispalaying value
    """
    def __init__(self, container):
        super().__init__(container, text='Parameters')
        self.container = container
        self._create_widgits()

    def _create_widgits(self):
        btn_update_move_step = tk.Button(self, text='Update Move Step (ft)')
        btn_update_angle_step = tk.Button(self, text='Update Angle Step (ft)')
        entry_angle_move_step = tk.Entry(self)
        label_for_angle_move_step = tk.Label(self, text=f'GET CUR STEPS')

        btn_update_move_step.grid(row=0)
        btn_update_angle_step.grid(row=1)
        entry_angle_move_step.grid(row=2)
        label_for_angle_move_step.grid(row=3)

        # give all widgets the sticky='EW'
        for child in self.winfo_children():
            if child.winfo_class() in ('Button', 'Entry', 'Label'):
                child.grid_configure(sticky='EW')

        entry_angle_move_step.insert(0, "input num val & click update")
        entry_angle_move_step.focus()

class ButtonsFrameArea(tk.Frame):
    """
    Combines all separate button frames into one frame
    """
    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self._create_widgets()
    
    def _create_widgets(self):
        file_management_button_frame = FileManagementButtonFrame(self)
        drawing_elements_buttons_frame = DrawingElementsButtonsFrame(self)
        displacing_elements_buttons_frame = DisplacingElementsButtonsFrame(self)
        rotating_elements_buttons_frame = RotatingElementsButtonsFrame(self)
        update_step_move_rotate_buttons_frame = UpdateStepMoveRotateButtonsFrame(self)

        file_management_button_frame.grid(column=0, row=0)
        drawing_elements_buttons_frame.grid(column=0, row=1)
        displacing_elements_buttons_frame.grid(column=0, row=2)
        rotating_elements_buttons_frame.grid(column=0, row=3)
        update_step_move_rotate_buttons_frame.grid(column=0, row=4)

        # give all Label Frames the sticky='EW' and pady= update
        for child in self.winfo_children():
            if child.winfo_class() == 'Labelframe':
                child.grid_configure(sticky='EW', pady=10)

class App(tk.Tk):
    # the main window. 
    def __init__(self):
        super().__init__()

        self.title("Angle Reflection Analysis")

        # position center
        app_width = self.winfo_screenwidth()//2
        app_height = self.winfo_screenheight()//2
        app_width_pad = f'{self.winfo_screenwidth()//2 - app_width//2}'  # for center
        app_height_pad = f'{self.winfo_screenheight()//2 - app_height//2}'  # for center
        screen_geometry_str = f'{app_width}x{app_height}+{app_width_pad}+{app_height_pad}'
        self.geometry(screen_geometry_str)
        
        # set columns / row sizes
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=3)

        self.drawing_to_internal_data_mapping = dict()
        self.pixel_per_foot_scale = 16  # pixel per foot 
        self._load_default_room()
        self._create_widgits()

    def _create_widgits(self):
        """ initializes the buttons and drawings area widgets """
        # add frames
        drawing_area = DrawingArea(self)
        buttons_area = ButtonsFrameArea(self)

        # place frames on grid
        drawing_area.grid(column=1, row=0, sticky="NSEW", padx=5, pady=5)  # TODO is rowspan the right way to do this? 
        buttons_area.grid(column=0, row=0, sticky="ew", padx=5, pady=5)  # TODO is rowspan the right way to do this? 
    
    def _load_default_room(self):
        """ initializes a default room """
        self.room = Room(100, 30)
        self.room.add_source((5, 25))
        self.room.add_reflector((45, 5), (55, 8))
        self.room.add_receiver((95, 25))
        
        self.test_var = "hellohellohello"
        # self.canvas = tk.Canvas(width=self.room.get_length(), height=self.room.get_height(), cursor="cross")



if __name__ == '__main__':
    app = App()
    app.mainloop()