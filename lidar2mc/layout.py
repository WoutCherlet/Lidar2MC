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
        self.selected_index_x = None
        self.selected_index_z = None

        self.calc_visible_regions()

    def read_data(self, chunk_data):
        self.data = chunk_data
        self.update_occupancy()
        return

    def render(self):
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                frame = tk.Frame(master=self.parent, borderwidth=1)
                frame.grid(row=i, column=j, padx=0,pady=0) # row is z, column is x
                button = tk.Button(frame, image=self.pixel, width=15, height=15, bd=0, command=partial(self.btn_callback,j,i))
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

        collision_id = self.check_chunk_collisions(x,z)
        if collision_id:
            self.infolabel.config(text=f"Occupied space! (Collision with plot {collision_id}) \n", fg="red")
            return
        
        # if fits: clear previous selection and draw new selection
        z_range = range(z, min(z+self.new_plot.z_length, self.gridsize))
        x_range = range(x, min(x+self.new_plot.x_length, self.gridsize))
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                if self.occupancy[i][j]:
                    continue
                elif i in z_range and j in x_range:
                    self.buttons[i][j].config(bg="green")
                else:
                    self.buttons[i][j].config(bg="white")
        self.selected_index_x = x
        self.selected_index_z = z

    def check_chunk_collisions(self, x, z):
        act_z = z + self.cur_z
        act_x = x + self.cur_x

        new_plot_x_range = range(act_x, act_x + self.new_plot.x_length)
        new_plot_y_range = range(act_z, act_z + self.new_plot.z_length)

        for plot in self.data:
            data = self.data[plot]
            left_x = data["x"]
            top_z = data["z"]
            x_l = data["x_length"]
            z_l = data["z_length"]
            x_range = range(left_x, left_x + x_l)
            z_range = range(top_z, top_z + z_l)

            # get overlap between shown grid and occupied rectangle
            overlapx = range(max(new_plot_x_range.start,x_range.start), min(new_plot_x_range.stop,x_range.stop)) or None
            overlapz = range(max(new_plot_y_range.start,z_range.start), min(new_plot_y_range.stop,z_range.stop)) or None
            if overlapx is None or overlapz is None:
                continue
            else:
                return plot
        return False

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

        # get direction
        x_offset = 0
        z_offset = 0
        if direction == "N":
            z_offset = -steps
        elif direction == "S":
            z_offset = steps
        elif direction == "E":
            x_offset = steps
        elif direction == "W":
            x_offset = -steps

        # update parameters
        self.cur_x += x_offset
        self.cur_z += z_offset
        if self.selected_index_x and self.selected_index_z:
            self.selected_index_x -= x_offset
            self.selected_index_z -= z_offset

        # update occupancy
        self.update_occupancy()

        # redraw grid
        self.redraw()

    def update_occupancy(self):
        self.occupancy = [[0 for i in range(self.gridsize)] for j in range(self.gridsize)]
        x_range_gr = range(self.cur_x, self.cur_x+self.gridsize)
        z_range_gr = range(self.cur_z, self.cur_z+self.gridsize)
        for plot in self.data:
            data = self.data[plot]
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
    
    def redraw(self):
        if self.selected_index_x and self.selected_index_z:
            x_range = range(self.selected_index_x, self.selected_index_x+self.new_plot.x_length)
            z_range = range(self.selected_index_z, self.selected_index_z+self.new_plot.z_length)
        else:
            x_range = range(0)
            z_range = range(0)
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                if self.occupancy[i][j]:
                    self.buttons[i][j].config(bg="red")
                elif i in z_range and j in x_range:
                    self.buttons[i][j].config(bg="green")
                else:
                    self.buttons[i][j].config(bg="white")

    def calc_visible_regions(self):
        self.regions = []
        x_checks = range(self.cur_x, self.cur_x+self.gridsize, min(self.gridsize-1, 32))
        z_checks = range(self.cur_z, self.cur_z+self.gridsize, min(self.gridsize-1, 32))
        for x in x_checks:
            for z in z_checks:
                reg = get_region(x, z, chunk=True)
                if reg not in self.regions:
                    self.regions.append(reg)

    def clear_selection(self):
        self.selected_index_z = None
        self.selected_index_x = None
        self.redraw()
        return



def create_buttons(window, chunk_frame):
    button_frame_N = tk.Frame(master=window, borderwidth=0)
    button_frame_W = tk.Frame(master=window, borderwidth=0)
    button_frame_E = tk.Frame(master=window, borderwidth=0)
    button_frame_S = tk.Frame(master=window, borderwidth=0)
    button_frame_N.grid(column=1,row=0, sticky="sew")
    button_frame_W.grid(column=0,row=1, sticky="nsw")
    button_frame_E.grid(column=2,row=1, sticky="nse")
    button_frame_S.grid(column=1,row=2, sticky="new")
    
    # configure North buttons
    button_frame_cont = tk.Frame(master=button_frame_N, pady=5)
    btn_1 = tk.Button(master=button_frame_cont, text="^1", relief=tk.GROOVE, bg="white", command= lambda: chunk_frame.move_grid(direction="N", steps=1))
    btn_1.grid(row=0,column=0, padx=2)
    btn_5 = tk.Button(master=button_frame_cont, text="^5", relief=tk.GROOVE, bg="white", command= lambda: chunk_frame.move_grid(direction="N", steps=5))
    btn_5.grid(row=0,column=1, padx=2)
    btn_r = tk.Button(master=button_frame_cont, text="^R", relief=tk.GROOVE, bg="white", command= lambda: chunk_frame.move_grid(direction="N", steps=32))
    btn_r.grid(row=0,column=2, padx=2)
    button_frame_cont.pack(anchor="center")

    # configure South buttons
    button_frame_cont = tk.Frame(master=button_frame_S, pady=5)
    btn_1 = tk.Button(master=button_frame_cont, text="v1", relief=tk.GROOVE, bg="white", command= lambda: chunk_frame.move_grid(direction="S", steps=1))
    btn_1.grid(row=0,column=0, padx=2)
    btn_5 = tk.Button(master=button_frame_cont, text="v5", relief=tk.GROOVE, bg="white", command= lambda: chunk_frame.move_grid(direction="S", steps=5))
    btn_5.grid(row=0,column=1, padx=2)
    btn_r = tk.Button(master=button_frame_cont, text="vR", relief=tk.GROOVE, bg="white", command= lambda: chunk_frame.move_grid(direction="S", steps=32))
    btn_r.grid(row=0,column=2, padx=2)
    button_frame_cont.pack(anchor="center")

    # configure West buttons
    button_frame_cont = tk.Frame(master=button_frame_W, padx=5)
    btn_1 = tk.Button(master=button_frame_cont, text="<1", relief=tk.GROOVE, bg="white", command= lambda: chunk_frame.move_grid(direction="W", steps=1))
    btn_1.grid(row=0,column=0, pady=2)
    btn_5 = tk.Button(master=button_frame_cont, text="<5", relief=tk.GROOVE, bg="white", command= lambda: chunk_frame.move_grid(direction="W", steps=5))
    btn_5.grid(row=1,column=0, pady=2)
    btn_r = tk.Button(master=button_frame_cont, text="<R", relief=tk.GROOVE, bg="white", command= lambda: chunk_frame.move_grid(direction="W", steps=32))
    btn_r.grid(row=2,column=0, pady=2)
    button_frame_cont.pack(anchor="center", expand=True)

    # configure East buttons
    button_frame_cont = tk.Frame(master=button_frame_E, padx=5)
    btn_1 = tk.Button(master=button_frame_cont, text=">1", relief=tk.GROOVE, bg="white", command= lambda: chunk_frame.move_grid(direction="E", steps=1))
    btn_1.grid(row=0,column=0, pady=2)
    btn_5 = tk.Button(master=button_frame_cont, text=">5", relief=tk.GROOVE, bg="white", command= lambda: chunk_frame.move_grid(direction="E", steps=5))
    btn_5.grid(row=1,column=0, pady=2)
    btn_r = tk.Button(master=button_frame_cont, text=">R", relief=tk.GROOVE, bg="white", command= lambda: chunk_frame.move_grid(direction="E", steps=32))
    btn_r.grid(row=2,column=0, pady=2)
    button_frame_cont.pack(anchor="center", expand=True)

def quit_with_selection_check(window, chunk_frame, infolabel):
    if not (chunk_frame.selected_index_x and chunk_frame.selected_index_z):
        infolabel.config(text="Please make a selection first. \n", fg="red")
        return
    else:
        window.quit()

def selector_window(new_plot : PlotInfo, occu_file : str):
    window = tk.Tk()
    window.title("Select location for new plot")

    main_selector_container = tk.Frame(master=window)

    label = tk.Label(master=window,text = " \n ")
    chunk_frame_container = tk.Frame(master=main_selector_container, relief=tk.GROOVE, borderwidth=3)
    chunk_frame_container.grid(column=1, row=1)
    chunk_frame = ChunkFrame(chunk_frame_container, new_plot=new_plot, infolabel=label)
    with open(occu_file) as f:
        occupancy = json.load(f) 
    chunk_frame.read_data(occupancy)
    chunk_frame.render()

    create_buttons(main_selector_container, chunk_frame)

    main_selector_container.pack()
    label.pack()
    close_btn = tk.Button(master=window, text="Confirm", command = lambda w=window, cf=chunk_frame, l=label : quit_with_selection_check(w, cf, l))
    close_btn.pack()

    window.mainloop()

    return chunk_frame.cur_x + chunk_frame.selected_index_x, chunk_frame.cur_z + chunk_frame.selected_index_z


if __name__ == "__main__":
    new_plot = PlotInfo(name="newplottest", x=None, z=None, x_length=5, z_length=8,description="test of new plot", type="type of new plot")
    selector_window(new_plot, "occupancy.json")
    # occu = PlotInfo("testplot", 2, 2, 10, 15, "this is a test plot to test the software. ", "test type")
    # occu2 = PlotInfo("testplot2", 15, 20, 10, 5, "a second test plot, non overlapping with the first one", "another test type")
    # dict = {0: occu.__dict__, 1: occu2.__dict__}
    # with open( "occupancy.json" , "w" ) as f:
    #     json.dump(dict, f)