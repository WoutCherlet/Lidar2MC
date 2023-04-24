import tkinter as tk
from functools import partial

class ChunkFrame():
    def __init__(self,parent,hoverlabel, gridsize=32) -> None:
        self.parent = parent
        self.hoverlabel = hoverlabel
        self.gridsize = gridsize
        self.pixel = tk.PhotoImage(width=10, height=10)

    def render(self):
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                frame = tk.Frame(master=self.parent, borderwidth=1)
                frame.grid(row=i, column=j, padx=0,pady=0)
                button = tk.Button(frame, image=self.pixel, width=15, height=15, bd=1, command=partial(self.btn_callback,i,j))
                button.bind("<Enter>", self.change_label_txt)
                # TODO: set text of bottom label on enter and leave
                button.pack(fill="both")

    def btn_callback(self, i, j):
        # TODO: render chunk here
        print(f"Button on row {i} and column {j}")

    def change_label_txt(self, e):
        print(e)
        self.hoverlabel.config(text="testbuttonenter")
    

def main():
    window = tk.Tk()
    # window.geometry("1200x800")  # set starting size of window
    # window.rowconfigure(2,weight=10, minsize=500)
    # window.columnconfigure(2,weight=10, minsize=500)

    label = tk.Label(master=window,text = "test")
    label.grid(row=4,sticky="w")

    chunk_frame_container = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
    chunk_frame_container.grid(column=2, row=2)
    chunk_frame = ChunkFrame(chunk_frame_container, hoverlabel=label)
    chunk_frame.render()

    button_frame_N = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
    button_frame_W = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
    button_frame_E = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
    button_frame_S = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
    
    button_frame_N.grid(column=2,row=1, sticky="sew")
    button_frame_W.grid(column=1,row=2, sticky="nsw")
    button_frame_E.grid(column=3,row=2, sticky="nse")
    button_frame_S.grid(column=2,row=3, sticky="new")

    label = tk.Label(master=button_frame_N, text=f"Upper buttons TODO")
    label.pack()
    label = tk.Label(master=button_frame_W, text=f"Left buttons TODO")
    label.pack()
    label = tk.Label(master=button_frame_E, text=f"Right buttons TODO")
    label.pack()
    label = tk.Label(master=button_frame_S, text=f"Bottom buttons TODO")
    label.pack()

    window.mainloop()


if __name__ == "__main__":
    main()