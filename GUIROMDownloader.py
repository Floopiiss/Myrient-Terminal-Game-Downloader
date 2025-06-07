import tkinter
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import threading
import queue

import sv_ttk

URLS = {
    "Gamecube": "https://myrient.erista.me/files/Redump/Nintendo%20-%20GameCube%20-%20NKit%20RVZ%20%5Bzstd-19-128k%5D/",
    "Nintendo Wii": "https://myrient.erista.me/files/Redump/Nintendo%20-%20Wii%20-%20NKit%20RVZ%20[zstd-19-128k]/",
    "Nintendo Wii U": "https://myrient.erista.me/files/Redump/Nintendo%20-%20Wii%20U%20-%20WUX/",
    "Playstation 1": "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/",
    "Playstation 2": "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%202/",
    "Playstation 3": "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%203/",
    "Xbox 360": "https://myrient.erista.me/files/Redump/Microsoft%20-%20Xbox%20360/",
    "Original Xbox": "https://myrient.erista.me/files/Redump/Microsoft%20-%20Xbox/"
}

root = tkinter.Tk()

root.title("Myrient Frontend - Downloading Roms")

logo = tkinter.PhotoImage(file="src/logo.png")
root.iconphoto(False, logo)

top_frame = tkinter.Frame(root)
top_frame.pack(side="top", fill="x")

middle_frame = tkinter.Frame(root)
middle_frame.pack(side="top", fill="both", expand=True)

bottom_frame = tkinter.Frame(root)
bottom_frame.pack(side="top", fill="x")

root.minsize(800, 900)    

def on_focus_in(event, entry, placeholder_text):
    """
    The function `on_focus_in` checks if the entry widget contains placeholder text and clears it if it
    does.
    
    :param event: The `event` parameter typically represents the event that triggered the function
    `on_focus_in`. In this case, it could be an event like a mouse click or a keyboard focus event
    :param entry: The `entry` parameter in the `on_focus_in` function is typically a tkinter Entry
    widget. It is the input field where users can type in text or interact with the GUI
    :param placeholder_text: The `placeholder_text` parameter is a string that represents the text that
    is displayed in an entry widget as a placeholder or hint to the user. It is typically displayed in a
    lighter color or italicized font to indicate that it is not user input
    """
    if entry.get() == placeholder_text:
        entry.delete(0, tkinter.END)
        entry.config(foreground='white')

def on_focus_out(event, entry, placeholder_text):
    """
    The function `on_focus_out` inserts a placeholder text into an entry widget if it is empty when the
    widget loses focus.
    
    :param event: The `event` parameter typically represents the event that triggered the function, such
    as a mouse click or a keyboard event. In this case, it seems like the function `on_focus_out` is
    designed to handle a focus out event on a GUI entry widget
    :param entry: The `entry` parameter in the `on_focus_out` function is typically a Tkinter Entry
    widget. This widget allows users to input a single line of text
    :param placeholder_text: The `placeholder_text` parameter is a string that represents the text that
    will be displayed in the entry widget when it is empty and does not have focus
    """
    if not entry.get():
        entry.insert(0, placeholder_text)
        entry.config(foreground='grey')

def add_placeholder(entry, placeholder_text):
    """
    The `add_placeholder` function adds placeholder text to an entry widget in a GUI and changes its
    color to grey, with event bindings to handle focus in and out.
    
    :param entry: The `entry` parameter in the `add_placeholder` function is typically a tkinter Entry
    widget where you want to add a placeholder text
    :param placeholder_text: The `placeholder_text` parameter is the text that will be displayed as a
    placeholder in the entry widget before the user starts typing. It is typically a hint or example
    text to guide the user on what to input in the entry widget
    """
    entry.insert(0, placeholder_text)
    entry.config(foreground='grey')

    entry.bind("<FocusIn>", lambda event: on_focus_in(event, entry, placeholder_text))
    entry.bind("<FocusOut>", lambda event: on_focus_out(event, entry, placeholder_text))

def get_correct_url(*args):
    """
    The function `get_correct_url` retrieves a URL based on a console input from a dictionary, or
    returns None if the console is not found in the dictionary.
    :return: The function `get_correct_url` returns the URL associated with the console provided as an
    argument, if it exists in the `URLS` dictionary. If the console is not found in the dictionary, it
    returns `None`.
    """
    console = console_var.get()
    
    if console in URLS:
        URL = URLS[console]
        return URL
    else:
        return None

platforms_list = ["Nintendo", "Playstation", "Xbox"]
NIN_LIST = ["Gamecube", "Nintendo Wii", "Nintendo Wii U"]
SONY_LIST = ["Playstation 1", "Playstation 2", "Playstation 3"]
XBOX_LIST = ["Original Xbox", "Xbox 360"]
all_matches = []
right_click_target = {"name": None}

platform_var = tkinter.StringVar(root, value="Select an Option")
console_var = tkinter.StringVar(root, value="Select an Option")
search_var = tkinter.StringVar(root)

platform_menu = ttk.OptionMenu(root, platform_var,"Select an Option", *platforms_list)
platform_menu.config(width=20)
platform_menu.pack(in_=top_frame, side="left", anchor="n", padx=15, pady=15)

nin_menu = ttk.OptionMenu(root, console_var,"Select an Option", *NIN_LIST)
nin_menu.config(width=20)

sony_menu = ttk.OptionMenu(root, console_var,"Select an Option", *SONY_LIST)
sony_menu.config(width=20)

xbox_menu = ttk.OptionMenu(root, console_var,"Select an Option", *XBOX_LIST)
xbox_menu.config(width=20)

right_click_menu = tkinter.Menu(root, tearoff=0)
right_click_menu.add_command(label="Download", command=lambda: start_download())

search_entry = ttk.Entry(root, textvariable=search_var)
add_placeholder(search_entry, "Search Game...")

game_list = tkinter.Listbox(root, height=50, width=50, bg="#1c1c1c",activestyle="dotbox",fg="white")

download_bar = ttk.Progressbar(bottom_frame, orient='horizontal', length=600, mode='determinate')
progress_queue = queue.Queue()

def check_ready_for_search():
    """
    The function `check_ready_for_search` determines whether to display a search entry based on selected
    platform and console.
    """
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
        search_entry.pack(in_=top_frame, side="top", anchor="ne", pady=15, padx=15)
    else:
        search_entry.pack_forget()

def update_console_menu(*args):
    """
    The function `update_console_menu` updates the console menu based on the selected platform and then
    calls the `check_ready_for_search` function.
    """
    
    nin_menu.pack_forget()
    sony_menu.pack_forget()
    xbox_menu.pack_forget()

    selected = platform_var.get()
    if selected == "Nintendo":
        nin_menu.pack(in_=top_frame, side="left", anchor="n", padx=15, pady=15)
    elif selected == "Playstation":
        sony_menu.pack(in_=top_frame, side="left", anchor="n", padx=15, pady=15)
    elif selected == "Xbox":
        xbox_menu.pack(in_=top_frame, side="left", anchor="n", padx=15, pady=15)
        
    check_ready_for_search()

def on_platform_change(*args):
    """
    The function `on_platform_change` sets the value of a variable to "Select an Option".
    """
    console_var.set("Select an Option")
    

def fetch_links_for_console(*args):
    """
    The function fetches links from a webpage and filters out specific file types before updating a
    listbox with the matches.
    :return: The `fetch_links_for_console` function is returning the result of the function
    `update_listbox_with_matches()`.
    """
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
    """
    This function calls another function to fetch links based on the selected console.
    """
    fetch_links_for_console(console_var.get())

def update_listbox_with_matches():
    """
    The function `update_listbox_with_matches` clears the game listbox and inserts text from all matches
    into it.
    """
    game_list.delete(0, tkinter.END)

    for text, href in all_matches:
        game_list.insert(tkinter.END, text) 

def check_ready_to_show_listbox(*args):
    """
    This function checks if both a platform and a console have been selected before showing a listbox of
    games.
    """
    platform = platform_var.get()
    console = console_var.get()
    
    if platform != "Select an Option" and console != "Select an Option":
        game_list.pack(in_=middle_frame, fill="both", expand=True, padx=10, pady=10)
    else:
        game_list.pack_forget()

def update_search_results(*args):
    """
    The function `update_search_results` filters and updates search results based on a query input.
    """
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

def show_context_menu(event):
    """
    The function `show_context_menu` selects an item in a list based on the nearest position of a mouse
    event and displays a context menu at that position.
    
    :param event: The `event` parameter in the `show_context_menu` function is an event object that
    represents a user action, such as a mouse click or key press, that triggers the context menu to be
    displayed. It contains information about the event, such as the coordinates of the event (event.x
    and event
    """
    try:
        index = game_list.nearest(event.y)
        game_list.selection_clear(0, tkinter.END)
        game_list.selection_set(index)
        game_list.activate(index)

        right_click_menu.tk_popup(event.x_root, event.y_root)
    finally:
        right_click_menu.grab_release()

def on_right_click(event):
    """
    The function `on_right_click` handles right-click events on a list of games, selecting the clicked
    game and displaying a context menu.
    
    :param event: The `event` parameter in the `on_right_click` function is typically an event object
    that contains information about the event that triggered the function. In this case, it is likely a
    mouse right-click event that is being handled. The event object may contain attributes such as `x`
    and `y
    """
    try:
        index = game_list.nearest(event.y)
        game_list.selection_clear(0, tkinter.END)
        game_list.selection_set(index)
        selected_game = game_list.get(index)
        right_click_target["name"] = selected_game
        right_click_menu.tk_popup(event.x_root, event.y_root)
    finally:
        right_click_menu.grab_release()

game_list.bind("<Button-3>", on_right_click)

def download_game_with_progress(url, output_path=None):
    """
    The function `download_game_with_progress` downloads a file from a given URL with progress tracking
    using a progress queue.
    
    :param url: The `url` parameter is the URL from which the game will be downloaded
    :param output_path: The `output_path` parameter in the `download_game_with_progress` function is the
    path where the downloaded game file will be saved on the local system. If this parameter is not
    provided, the function will extract the filename from the URL and save the file in the current
    working directory with that filename
    """
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    if output_path is None:
        output_path = url.split("/")[-1]
    downloaded = 0
    
    progress_queue.put(('set_max', total_size))
    
    with open(output_path, 'wb') as f:
        for data in response.iter_content(block_size):
            if not data:
                break
            f.write(data)
            downloaded += len(data)
            progress_queue.put(('progress', downloaded))
    
    progress_queue.put(('done', None))

def process_queue():
    """
    The `process_queue` function continuously checks for messages in a queue and updates a download
    progress bar accordingly in a Python GUI application.
    """
    try:
        while True:
            message, value = progress_queue.get_nowait()
            if message == 'set_max':
                download_bar['maximum'] = value
                download_bar['value'] = 0
                download_bar.pack(side="bottom", anchor="s", pady=5)
            elif message == 'progress':
                download_bar['value'] = value
            elif message == 'done':
                download_bar['value'] = download_bar['maximum']                
    except queue.Empty:
        pass
    root.after(100, process_queue)  
            
def start_download():
    """
    The `start_download` function downloads a game with progress tracking based on the provided game
    name.
    """
    name = right_click_target["name"]
    game = next((g for g in all_matches if g[0] == name), None)
    if game:
        url = get_correct_url() + game[1]
        output_path = url.split("/")[-1]
        threading.Thread(target=download_game_with_progress, args=(url, output_path), daemon=True).start()
        
if __name__ == "__main__":
    platform_var.trace_add("write", update_console_menu)
    console_var.trace_add("write", lambda *args: check_ready_for_search())
    platform_var.trace_add("write", on_platform_change)
    console_var.trace_add("write", lambda *args: print(get_correct_url()))
    console_var.trace_add("write", on_console_selected)    
    platform_var.trace_add("write", check_ready_to_show_listbox)
    console_var.trace_add("write", check_ready_to_show_listbox)
    search_var.trace_add("write", update_search_results)
    process_queue()
    
    sv_ttk.set_theme("dark")
    root.mainloop()

    


