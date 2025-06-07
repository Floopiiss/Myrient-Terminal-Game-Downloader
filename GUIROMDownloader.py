import tkinter
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os

import sv_ttk

URLS = {
    "Gamecube": "https://myrient.erista.me/files/Redump/Nintendo%20-%20GameCube%20-%20NKit%20RVZ%20%5Bzstd-19-128k%5D/",
    "Nintendo Wii": "https://myrient.erista.me/files/Redump/Nintendo%20-%20Wii%20-%20NKit%20RVZ%20[zstd-19-128k]/?C=N&O=A",
    "Nintendo Wii U": "https://myrient.erista.me/files/Redump/Nintendo%20-%20Wii%20U%20-%20WUX/",
    "Playstation 1": "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/",
    "Playstation 2": "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%202/",
    "Playstation 3": "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%203/",
    "Xbox 360": "https://myrient.erista.me/files/Redump/Microsoft%20-%20Xbox%20360/",
    "Original Xbox": "https://myrient.erista.me/files/Redump/Microsoft%20-%20Xbox/"
}

root = tkinter.Tk()

root.minsize(800, 900)    

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
all_matches = []

platform_var = tkinter.StringVar(root, value="Select an Option")
console_var = tkinter.StringVar(root, value="Select an Option")
search_var = tkinter.StringVar(root)

platform_menu = ttk.OptionMenu(root, platform_var,"Select an Option", *platforms_list)
platform_menu.config(width=20)
platform_menu.pack(side="left", anchor="n", padx=15, pady=15)

nin_menu = ttk.OptionMenu(root, console_var,"Select an Option", *NIN_LIST)
nin_menu.config(width=20)

sony_menu = ttk.OptionMenu(root, console_var,"Select an Option", *SONY_LIST)
sony_menu.config(width=20)

xbox_menu = ttk.OptionMenu(root, console_var,"Select an Option", *XBOX_LIST)
xbox_menu.config(width=20)


search_entry = ttk.Entry(root, textvariable=search_var)
add_placeholder(search_entry, "Search Game...")

game_list = tkinter.Listbox(root, height=50, width=50, bg="#1c1c1c",activestyle="dotbox",fg="white")

def get_correct_url(*args):
    console = console_var.get()
    
    if console in URLS:
        URL = URLS[console]
        return URL
    else:
        return None

def check_ready_for_search():
    platform = platform_var.get()
    console = console_var.get()

    show_search = False

    if platform == "Nintendo" and console in NIN_LIST:
        show_search = True
    elif platform == "Playstation" and console in SONY_LIST:
        show_search = True
    elif platform == "Xbox" and console in XBOX_LIST:
        show_search = True

    if show_search:
        search_entry.pack(side="top", anchor="n", pady=15)
    else:
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

def on_platform_change(*args):
    console_var.set("Select an Option")
    

def fetch_links_for_console(console):
    url = get_correct_url() 
    if url is None:
        return

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    all_matches.clear()
    
    for a in soup.find_all("a"):
        href = a.get("href") # type: ignore
        text = a.get_text(strip=True)
        if href and href not in ("../", "./", "/", ""):
            if href.lower().endswith((".iso", ".nkit", ".rvz", ".zip", ".7z", ".rar")): # type: ignore
                all_matches.append((text, href))
            
    update_listbox_with_matches()
            
def on_console_selected(*args):
    fetch_links_for_console(console_var.get())

def update_listbox_with_matches():
    game_list.delete(0, tkinter.END)

    for text, href in all_matches:
        game_list.insert(tkinter.END, text) 

def check_ready_to_show_listbox(*args):
    platform = platform_var.get()
    console = console_var.get()
    
    if platform != "Select an Option" and console != "Select an Option":
        game_list.pack(side="bottom", fill="both", expand=True, padx=0, pady=0)
    else:
        game_list.pack_forget()

def update_search_results(*args):
    query = search_var.get().strip().lower()

    if query == "" or query == "search game...":
        game_list.delete(0, tkinter.END)
        for game in all_matches:
            game_list.insert(tkinter.END, game[0])
    else:
        filtered = [game for game in all_matches if query in game[0].lower()]
        game_list.delete(0, tkinter.END)
        for game in filtered:
            game_list.insert(tkinter.END, game[0])

if __name__ == "__main__":
    platform_var.trace_add("write", update_console_menu)
    console_var.trace_add("write", lambda *args: check_ready_for_search())
    platform_var.trace_add("write", update_console_menu)
    platform_var.trace_add("write", on_platform_change)
    console_var.trace_add("write", lambda *args: print(get_correct_url()))
    console_var.trace_add("write", on_console_selected)    
    platform_var.trace_add("write", check_ready_to_show_listbox)
    console_var.trace_add("write", check_ready_to_show_listbox)
    search_var.trace_add("write", update_search_results)
    
    sv_ttk.set_theme("dark")
    root.mainloop()

    


