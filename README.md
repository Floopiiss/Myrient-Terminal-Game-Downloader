# Wii NKit RVZ Downloader 🎮📥
A simple terminal tool to scrape and download Nintendo Wii NKit RVZ files from [myrient.erista.me](https://myrient.erista.me).
---
## ❗Reminder❗
No Piracy, Piracy is super bad for our Glorious Nintendo.
---
## Features

- Scrapes the latest game list automatically 🔍  
- Search games by name (case-insensitive, fuzzy)  
- Interactive selection of matching games  
- Downloads with progress bar ⏳  
- Handles download interruptions gracefully ❌  
- Downloads the ZIP Content to the same Directory
- Good Enough Validation ¯\_(ツ)_/¯ , don't purposefully break it

---

## Shortcomings/Issues

- If you search for Europe or USA or something, then it may only display some of the results
![Code_3FgeebcGVz](https://github.com/user-attachments/assets/2b8d3337-9d60-4cac-a6d3-7d1f7b741499)
-  There is probably something that can crash, i couldnt be arsed to check all of it tho.
-  Eventually (someday), i will add a sort to only check depending on the Region you select
-  I also want to add a GUI, but that looks annoying so dont expect it anytime soon

---

## Requirements

- beautifulsoup4 >= 4.13.4
- bs4 >= 0.0.2
- certifi >= 2025.4.26
- charset-normalizer >= 3.4.2
- colorama >= 0.4.6
- idna >= 3.10
- requests >= 2.32.3
- soupsieve >= 2.7
- tqdm >= 4.67.1
- typing_extensions >= 4.13.2
- urllib3 >= 2.4.0

---

## Usage

1. Run the script:

   ```bash
   python downloader.py
