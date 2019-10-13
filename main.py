import tkinter as tk
from tkinter import ttk
import json, glob, datetime
import extractor, generator


superscripts = {
        1: u"\u00B9",
        2: u"\u00B2",
        3: u"\u00B3",
        4: u"\u2074",
        5: u"\u2075",
        6: u"\u2076",
        7: u"\u2077",
        8: u"\u2078",
        9: u"\u2079",
    }

window = tk.Tk()
window.title("Puzzitive")
    
# Title
tk.Label(window, text="PUZZITIVE", font=("Helvetica", 30), fg="Blue").grid(row=0, column=0, columnspan="4", padx=(20,0), pady=(0,10))
    
# Combo box
filenames = glob.glob(r"C:\Users\shkha\OneDrive\Desktop\Courses\Spring 18-19\CS 461\Project\Final\code\data\*.json")
filenames = [w[-15:-5] for w in filenames]
combo = ttk.Combobox(window, values=filenames)
combo.grid(row=16, column=10, columnspan="2")
combo.current(1)
button = tk.Button(window, text="Extract today's puzzle", fg="black")                                                    
button.grid(row=16, column=7, columnspan="2")



def extract_puzzle(event):
    extractor.get_puzzle()
    combo.set(datetime.date.today().strftime("%Y-%m-%d"))
    draw(None)
    
def draw(event):
    name = combo.get()
    file = r"C:\Users\shkha\OneDrive\Desktop\Courses\Spring 18-19\CS 461\Project\Final\code\data\\" + name + ".json"
    with open(file) as json_file:
        data = json.load(json_file)
        
    cells = data["cells"]
    clues = data["clues"]
    across = clues["across"]
    down = clues["down"]
    
    # Drawing crossword matrix
    z = 0
    for x in range(1, 6):
        for y in range(1, 6):
            if cells[z]["letter"] is None:
                tk.Label(window, bg="Black", font=("Helvetica", 24),
                              borderwidth="3", relief="groove", width="4", height="2").grid(row=x, column=y)
            elif cells[z]["key"] != None:
                tk.Label(window, text=superscripts[cells[z]["key"]] + "  " + (cells[z]["letter"]),
                              font=("Helvetica", 24), foreground="Black", borderwidth="3", relief="groove",
                              width="4", height="2").grid(row=x, column=y)
            else:
                tk.Label(window, text=(cells[z]["letter"]), font=("Helvetica", 24),
                              foreground="Black", borderwidth="3", relief="groove", width="4", height="2").grid(row=x, column=y)
            z = z + 1   
    tk.Label(window, text="Date: " + name).grid(row=len(down) + 1, column=len(across) - 1, padx=(30, 0),pady=(10, 0), columnspan="2")
    
    
    #These labels are to display across and down on the window
    tk.Label(window, width="55", text="Across").grid(row=0, column=7)
    tk.Label(window, width="55", text="Down").grid(row=0, column=10)
    # Drawing the clues
    for i in range(1, len(across) + 1):
        tk.Label(window, text=across[i - 1]["key"], borderwidth="3", bg="White").grid(row=i, column=6, padx=(50, 0))
        tk.Label(window, text=across[i - 1]["hint"], borderwidth="3", bg="White", height=2, width=55, wraplength=400).grid(row=i, column=7,
                                                                                                        padx=(10, 0), pady=(5, 5))
        tk.Label(window, text=down[i - 1]["key"], borderwidth="3", bg="White").grid(row=i, column=9, padx=(50, 0))
        tk.Label(window, text=down[i - 1]["hint"], borderwidth="3", bg="White", height=2, width=55, wraplength=400).grid(row=i, column=10,
                                                                                                            padx=(10, 0), pady=(5, 5))
        #tk.Label(window, text=across[i - 1]["key"], borderwidth="3", bg="White").grid(row=len(down) + 1 + i, column=6, padx=(50, 0), pady =(5,5))
        
    # Drawing new clues
    tk.Label(window, text="New Across Clues").grid(row=6, column=7)
    tk.Label(window, text="New Down Clues").grid(row=6, column=10)
    down_sol, across_sol = generator.extract_solutions(cells)
    new_down_clues, new_across_clues = generator.generate_clues(down_sol, across_sol)
    for i in range(len(new_down_clues)):
        clue = new_across_clues[i][1]
        key = new_across_clues[i][0]
        tk.Label(window, text=key, borderwidth="3", bg="White").grid(row=i+7, column=6, padx=(50, 0))
        tk.Label(window, text=clue, borderwidth="3", bg="White", height=2, width=55, wraplength=400).grid(row=i+7, column=7,
                                                                                                        padx=(10, 0), pady=(5, 5))
        
        clue = new_down_clues[i][1]
        key = new_down_clues[i][0]
        tk.Label(window, text=key, borderwidth="3", bg="White").grid(row=i+7, column=9, padx=(50, 0))
        tk.Label(window, text=clue, borderwidth="3", bg="White", height=2, width=55, wraplength=400).grid(row=i+7, column=10,
                                                                                                        padx=(10, 0), pady=(5, 5))
    
    
    
draw(None)   
combo.bind("<<ComboboxSelected>>", draw)
button.bind("<Button-1>", extract_puzzle)
window.mainloop()

