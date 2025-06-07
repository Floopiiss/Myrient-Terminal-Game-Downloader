import tkinter
from tkinter import ttk

import sv_ttk

root = tkinter.Tk()

root.minsize(500, 500)

title_text = ttk.Label(root, text="ROM Downloader",
                       font=("Helvetica", 24)).pack(side = "top", pady = 10)

def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.config(foreground='grey')

    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tkinter.END)
            entry.config(foreground='white')

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(foreground='grey')

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

platforms_list = ["Nintendo", "Playstation", "Xbox"]
NIN_LIST = ["Gamecube", "Nintendo Wii", "Nintendo Wii U"]
SONY_LIST = ["Playstation 1", "Playstation 2", "Playstation 3"]
XBOX_LIST = ["Original Xbox", "Xbox 360"]

platform_var = tkinter.StringVar(root, value="Select an Option")
nin_var = tkinter.StringVar(root, value="Select an Option")
xbox_var = tkinter.StringVar(root, value="Select an Option")
sony_var = tkinter.StringVar(root, value="Select an Option")
search_var = tkinter.StringVar(root)


platform_menu = ttk.OptionMenu(root, platform_var,"Select an Option", *platforms_list).pack(side="left", anchor="n", padx=15, pady=15)
nin_menu = ttk.OptionMenu(root, nin_var,"Select an Option", *NIN_LIST) 
sony_menu = ttk.OptionMenu(root, xbox_var,"Select an Option", *SONY_LIST) 
xbox_menu = ttk.OptionMenu(root, sony_var,"Select an Option", *XBOX_LIST) 

search_label = ttk.Label(root, text="Search Game:")
search_entry = ttk.Entry(root, textvariable=search_var)
add_placeholder(search_entry, "Search Game...")

game_list = tkinter.Listbox(root, height=50, width=25, bg="black",activestyle="dotbox",fg="white")

def check_ready_for_search():
    platform = platform_var.get()
    nin = nin_var.get()
    sony = sony_var.get()
    xbox = xbox_var.get()

    show_search = False

    if platform == "Nintendo" and nin in NIN_LIST:
        show_search = True
    elif platform == "Playstation" and sony in SONY_LIST:
        show_search = True
    elif platform == "Xbox" and xbox in XBOX_LIST:
        show_search = True

    if show_search:
#        search_label.pack(side="top", anchor="n")
        search_entry.pack(side="top", anchor="n", pady=15)
    else:
        search_label.pack_forget()
        search_entry.pack_forget()

def update_console_menu(*args):
    
    nin_menu.pack_forget()
    sony_menu.pack_forget()
    xbox_menu.pack_forget()

    selected = platform_var.get()
    if selected == "Nintendo":
        nin_menu.pack(side="right", anchor="n", padx=15, pady=15)
    elif selected == "Playstation":
        sony_menu.pack(side="right", anchor="n", padx=15, pady=15)
    elif selected == "Xbox":
        xbox_menu.pack(side="right", anchor="n", padx=15, pady=15)
        
    check_ready_for_search()

def update_search_results(*args):
    query = search_var.get().lower()

if __name__ == "__main__":
    platform_var.trace_add("write", update_console_menu)
    nin_var.trace_add("write", lambda *args: check_ready_for_search())
    sony_var.trace_add("write", lambda *args: check_ready_for_search())
    xbox_var.trace_add("write", lambda *args: check_ready_for_search())
    platform_var.trace_add("write", update_console_menu)
    search_var.trace_add("write", update_search_results)
    sv_ttk.set_theme("dark")
    root.mainloop()

    


