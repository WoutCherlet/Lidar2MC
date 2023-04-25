import tkinter as tk
from functools import partial
import json
from utils import get_region

class PlotInfo:
    def __init__(self, name, x, z, x_length, z_length, description, type):
        self.name = name
        self.x = x
        self.z = z
        self.x_length = x_length
        self.z_length = z_length
        self.description = description
        self.type = type


class ChunkFrame:
    def __init__(self, parent, new_plot: PlotInfo, infolabel, gridsize=32, x=0, z=0) -> None:
        self.parent = parent
        self.new_plot = new_plot
        self.infolabel = infolabel
        self.gridsize = gridsize
        # holds data of other plots
        self.data = {}
        # first index is z, second is x
        self.occupancy = [[0 for i in range(gridsize)] for j in range(gridsize)]
        self.buttons = [[0 for i in range(gridsize)] for j in range(gridsize)]
        self.pixel = tk.PhotoImage(width=10, height=10)
        # cur_x and cur_z keep track of current top left chunk coordinates
        self.cur_x = x
        self.cur_z = z
        # selected_x and selected_z keep track of location selected for new plot
        self.selected_x = None
        self.selected_z = None

        self.calc_visible_regions()

    def read_data(self, chunk_data):
        self.data = chunk_data
        x_range_gr = range(self.cur_x, self.cur_x+self.gridsize)
        z_range_gr = range(self.cur_z, self.cur_z+self.gridsize)
        for plot in chunk_data:
            data = chunk_data[plot]
            left_x = data["x"]
            top_z = data["z"]
            x_l = data["x_length"]
            z_l = data["z_length"]
            x_range = range(left_x, left_x + x_l)
            z_range = range(top_z, top_z + z_l)

            # get overlap between shown grid and occupied rectangle
            overlapx = range(max(x_range_gr.start,x_range.start), min(x_range_gr.stop,x_range.stop)) or None
            overlapz = range(max(z_range_gr.start,z_range.start), min(z_range_gr.stop,z_range.stop)) or None
            if overlapx is None or overlapz is None:
                continue
            else:
                for i in overlapz:
                    for j in overlapx:
                        self.occupancy[i-self.cur_z][j-self.cur_x] = int(plot)+1
        return

    # TODO: render 
    def render(self):
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                frame = tk.Frame(master=self.parent, borderwidth=1)
                frame.grid(row=i, column=j, padx=0,pady=0) # row is z, column is x
                button = tk.Button(frame, image=self.pixel, width=15, height=15, bd=1, command=partial(self.btn_callback,j,i))
                if self.occupancy[i][j]:
                    button.config(bg="red")
                else:
                    button.config(bg="white")
                button.bind("<Enter>", lambda event, i=i, j=j: self.on_chunk_hover(event, i, j))
                # button.bind("<Leave>", lambda event: self.infolabel.config(text="", fg="black"))
                button.pack(fill="both")
                self.buttons[i][j] = button

    def btn_callback(self, x, z):
        # check if chunk fits in new location
        z_range = range(z, min(z+self.new_plot.z_length, self.cur_z+self.gridsize))
        x_range = range(x, min(x+self.new_plot.x_length, self.cur_x+self.gridsize))
        for i in z_range:
            for j in x_range:
                if self.occupancy[i][j]:
                    self.infolabel.config(text=f"Occupied space! (Collision at z= {i}, x={j}) \n", fg="red")
                    return
        
        # if fits: clear previous selection and draw new selection
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                if self.occupancy[i][j]:
                    continue
                elif i in z_range and j in x_range:
                    self.buttons[i][j].config(bg="green")
                else:
                    self.buttons[i][j].config(bg="white")
        self.selected_x = x
        self.selected_z = z

    def on_chunk_hover(self, e, i, j):
        if self.occupancy[i][j]:
            info = self.data[str(self.occupancy[i][j]-1)]
            reg_x, reg_z = get_region(j+self.cur_x,i+self.cur_z, chunk=True)
            info_txt = f"Reg {reg_x},{reg_z}, x={j+self.cur_x},z={i+self.cur_z}, plot located here: {info['name']}, of type {info['type']}.\n Description: {info['description']}"
            self.infolabel.config(text=info_txt, fg="black")
        else:
            reg_x, reg_z = get_region(j+self.cur_x,i+self.cur_z, chunk=True)
            self.infolabel.config(text=f"Reg {reg_x},{reg_z}, x={j+self.cur_x},z={i+self.cur_z} \n ", fg="black")
    
    def move_grid(self, direction, steps):
        """
        Move the grid in direction for n steps.
        """

        # TODO: implement move grid

        ## Hard part: keep track of which regions are visible, and read new ones if necessary
        # Update occupancy grid
        # Update button colors

        # second option: redraw everything by destroying everything then calling render. Will probably need to do this if we want region borders. Can also use seperators but is messy because takes place in grid

    def calc_visible_regions(self):
        self.regions = []
        x_checks = range(self.cur_x, self.cur_x+self.gridsize, min(self.gridsize-1, 32))
        z_checks = range(self.cur_z, self.cur_z+self.gridsize, min(self.gridsize-1, 32))
        for x in x_checks:
            for z in z_checks:
                reg = get_region(x, z, chunk=True)
                if reg not in self.regions:
                    self.regions.append(reg)


def create_buttons(window):
    button_frame_N = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
    button_frame_W = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
    button_frame_E = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
    button_frame_S = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
    button_frame_N.grid(column=1,row=0, sticky="sew")
    button_frame_W.grid(column=0,row=1, sticky="nsw")
    button_frame_E.grid(column=2,row=1, sticky="nse")
    button_frame_S.grid(column=1,row=2, sticky="new")
    
    # configure North buttons
    button_frame_cont = tk.Frame(master=button_frame_N)
    btn_1 = tk.Button(master=button_frame_cont, text="^1")
    btn_1.grid(row=0,column=0)
    btn_5 = tk.Button(master=button_frame_cont, text="^5")
    btn_5.grid(row=0,column=1)
    btn_r = tk.Button(master=button_frame_cont, text="^R")
    btn_r.grid(row=0,column=2)
    button_frame_cont.pack(anchor="center")

    # configure South buttons
    button_frame_cont = tk.Frame(master=button_frame_S)
    btn_1 = tk.Button(master=button_frame_cont, text="v1")
    btn_1.grid(row=0,column=0)
    btn_5 = tk.Button(master=button_frame_cont, text="v5")
    btn_5.grid(row=0,column=1)
    btn_r = tk.Button(master=button_frame_cont, text="vR")
    btn_r.grid(row=0,column=2)
    button_frame_cont.pack(anchor="center")

    # configure West buttons
    button_frame_cont = tk.Frame(master=button_frame_W)
    btn_1 = tk.Button(master=button_frame_cont, text="<1")
    btn_1.grid(row=0,column=0)
    btn_5 = tk.Button(master=button_frame_cont, text="<5")
    btn_5.grid(row=1,column=0)
    btn_r = tk.Button(master=button_frame_cont, text="<R")
    btn_r.grid(row=2,column=0)
    button_frame_cont.pack(anchor="center", expand=True)

    # configure East buttons
    button_frame_cont = tk.Frame(master=button_frame_E)
    btn_1 = tk.Button(master=button_frame_cont, text=">1")
    btn_1.grid(row=0,column=0)
    btn_5 = tk.Button(master=button_frame_cont, text=">5")
    btn_5.grid(row=1,column=0)
    btn_r = tk.Button(master=button_frame_cont, text=">R")
    btn_r.grid(row=2,column=0)
    button_frame_cont.pack(anchor="center", expand=True)

def selector_window(new_plot : PlotInfo, occu_file : str):
    window = tk.Tk()
    window.title("Select location for new plot")

    main_selector_container = tk.Frame(master=window)

    label = tk.Label(master=window,text = " \n ")

    chunk_frame_container = tk.Frame(master=main_selector_container, relief=tk.RAISED, borderwidth=1)
    chunk_frame_container.grid(column=1, row=1)
    chunk_frame = ChunkFrame(chunk_frame_container, new_plot=new_plot, infolabel=label)
    with open(occu_file) as f:
        occupancy = json.load(f) 
    chunk_frame.read_data(occupancy)
    chunk_frame.render()

    create_buttons(main_selector_container)

    main_selector_container.pack()
    label.pack()

    window.mainloop()


if __name__ == "__main__":
    new_plot = PlotInfo(name="newplottest", x=None, z=None, x_length=5, z_length=8,description="test of new plot", type="type of new plot")
    selector_window(new_plot, "occupancy.json")
    # occu = PlotInfo("testplot", 2, 2, 10, 15, "this is a test plot to test the software. ", "test type")
    # occu2 = PlotInfo("testplot2", 15, 20, 10, 5, "a second test plot, non overlapping with the first one", "another test type")
    # dict = {0: occu.__dict__, 1: occu2.__dict__}
    # with open( "occupancy.json" , "w" ) as f:
    #     json.dump(dict, f)