# Myrient TUI (AND GUI) Game Downloader 🎮📥
A simple terminal tool to scrape and download game files from [myrient.erista.me](https://myrient.erista.me).
---
## ❗Reminder❗

- No Piracy, Piracy is really bad and we don't want to do anything super bad
- This tool scrapes and downloads files from [myrient.erista.me](https://myrient.erista.me)
- I Developed this to make Downloading quicker and easier, but if this program goes against website TOS, just send me a message and ill take it down.
- It says "This means not limiting users from being able to play their favorite video game or simply having an archive for themselves", which i took as free reign to develop this tool.
---
## Features

- Scrapes the latest game list automatically 🔍  
- Search games by name (case-insensitive, but the search is kind of terrible, just enter one word from the title and search through the list)  
- Interactive selection of matching games  
- Downloads with progress bar ⏳  
- Handles download interruptions gracefully ❌  
- Downloads the ZIP Content to the same Directory
- Good Enough Validation ¯\_(ツ)_/¯ , don't purposefully break it
- Features Nintendo, Sony, and Xbox Games

---

## Shortcomings/Issues

- If you search for Europe or USA or something, then it may only display some of the results
![Code_3FgeebcGVz](https://github.com/user-attachments/assets/2b8d3337-9d60-4cac-a6d3-7d1f7b741499)
-  There is probably something that can crash, i couldnt be arsed to check all of it tho.
-  Eventually (someday), i will add a sort to only check depending on the Region you select
-  I also want to add a GUI, but that looks annoying so dont expect it anytime soon

---

## Requirements

altgraph==0.17.4  
beautifulsoup4==4.13.4  
bs4==0.0.2  
certifi==2025.4.26  
charset-normalizer==3.4.2  
colorama==0.4.6  
idna==3.10  
packaging==25.0  
pefile==2024.8.26  
pyasn1==0.6.1  
pyinstaller==6.13.0  
pyinstaller-hooks-contrib==2025.4  
pywin32-ctypes==0.2.3  
requests==2.32.3  
rsa==4.9.1  
setuptools==80.8.0  
soupsieve==2.7  
sv-ttk==2.6.0  
thread==2.0.5  
tqdm==4.67.1  
typing_extensions==4.13.2  
urllib3==2.4.0 

---

## Usage (TUI)

Run the script:

   ```bash
   python TUIROMDownloader.py
   ```

# OR

Run the Executable from dist folder or from releases:

## Usage (GUI)
1. Run the script:

   ```bash
   python GUIROMDownloader.py
   ```
   
# OR

Run the Executable from dist folder or from releases
