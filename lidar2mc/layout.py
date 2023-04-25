import tkinter as tk
from functools import partial
import json

class OccupiedSpace:
    def __init__(self, name, x, z, x_length, z_length, description, type):
        self.name = name
        self.x = x
        self.z = z
        self.x_length = x_length
        self.z_length = z_length
        self.description = description
        self.type = type


class ChunkFrame():
    def __init__(self, parent, infolabel, gridsize=32, x=0, z=0) -> None:
        self.parent = parent
        self.infolabel = infolabel
        self.gridsize = gridsize
        self.pixel = tk.PhotoImage(width=10, height=10)
        self.data = {}
        self.occupancy = [[0 for i in range(gridsize)] for j in range(gridsize)]
        # cur_x and cur_z keep track of current top left chunk coordinates
        self.cur_x = x
        self.cur_z = z

    def read_data(self, chunk_data):
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
                for i in overlapx:
                    for j in overlapz:
                        self.occupancy[i-self.cur_x][j-self.cur_z] = 1
        return
        

    def render(self):
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                frame = tk.Frame(master=self.parent, borderwidth=1)
                frame.grid(row=i, column=j, padx=0,pady=0)
                button = tk.Button(frame, image=self.pixel, width=15, height=15, bd=1, command=partial(self.btn_callback,i,j))
                if self.occupancy[i][j]:
                    button.config(bg="red")
                button.bind("<Enter>", lambda event, arg=f"{i},{j}": self.change_label_txt(event, arg))
                button.bind("<Leave>", lambda event, arg=f"": self.change_label_txt(event, arg))
                button.pack(fill="both")

    def btn_callback(self, i, j):
        # TODO: render chunk here
        print(f"Button on row {i} and column {j}")

    def change_label_txt(self, e, txt):
        # TODO: show info about plot in label here:
        self.infolabel.config(text=txt)
    
    def move_grid(self, direction, steps):
        """
        Move the grid in direction for n steps.
        """

        # TODO: implement move grid

        ## Hard part: keep track of which regions are visible, and read new ones if necessary
        # Update occupancy grid
        # Update button colors
        # Have to also keep track of which exact chunks are where somehow

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

def run_selector():
    window = tk.Tk()
    window.title("Select location for new plot")

    main_selector_container = tk.Frame(master=window)

    label = tk.Label(master=window,text = "")

    chunk_frame_container = tk.Frame(master=main_selector_container, relief=tk.RAISED, borderwidth=1)
    chunk_frame_container.grid(column=1, row=1)
    chunk_frame = ChunkFrame(chunk_frame_container, infolabel=label)
    with open("occupancy.json") as f:
        occupancy = json.load(f) 
    chunk_frame.read_data(occupancy)
    chunk_frame.render()

    create_buttons(main_selector_container)

    main_selector_container.pack()
    label.pack()

    window.mainloop()


if __name__ == "__main__":
    run_selector()
    # occu = OccupiedSpace("testplot", 2, 2, 10, 15, "this is a test plot to test the software. ", "test type")
    # occu2 = OccupiedSpace("testplot2", 15, 20, 10, 5, "a second test plot, non overlapping with the first one", "another test type")
    # dict = {0: occu.__dict__, 1: occu2.__dict__}
    # with open( "occupancy.json" , "w" ) as f:
    #     json.dump(dict, f)