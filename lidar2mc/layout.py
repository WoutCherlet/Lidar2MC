import tkinter as tk





def main():
    window = tk.Tk()

    # window.geometry("500x300")  # set starting size of window
    # window.maxsize(500, 300)  # width x height


    gridsize = 10

    for i in range(gridsize):
        for j in range(gridsize):
            frame = tk.Frame(
                master=window,
                relief=tk.RAISED,
                borderwidth=1
            )
            frame.grid(row=i, column=j)
            label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
            label.pack()


    window.mainloop()

if __name__ == "__main__":
    main()