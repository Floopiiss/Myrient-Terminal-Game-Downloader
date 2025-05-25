import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os

GC_URL = "https://myrient.erista.me/files/Redump/Nintendo%20-%20GameCube%20-%20NKit%20RVZ%20%5Bzstd-19-128k%5D/"
WII_URL = "https://myrient.erista.me/files/Redump/Nintendo%20-%20Wii%20-%20NKit%20RVZ%20[zstd-19-128k]/?C=N&O=A"
WII_U_URL = "https://myrient.erista.me/files/Redump/Nintendo%20-%20Wii%20U%20-%20WUX/"
PS1_URL = "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/"
PS2_URL = "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%202/"
PS3_URL = "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%203/"
XBOX360_URL = "https://myrient.erista.me/files/Redump/Microsoft%20-%20Xbox%20360/"
XBOX_URL = "https://myrient.erista.me/files/Redump/Microsoft%20-%20Xbox/"


def get_correct_url():
    """
    The function `get_correct_url` allows the user to select a gaming platform and then a specific
    console from that platform to return the corresponding URL.
    :return: The code is returning different URLs based on the user's input for the gaming platform and
    the specific console within that platform. The URLs are returned based on the choices made by the
    user for Nintendo, Sony, and Xbox platforms, and the specific consoles within those platforms.
    """
    while True:
        print("#######################")
        print("###### Platforms ######")
        print("#######################")
        print("1. Nintendo")
        print("2. Sony")
        print("3. Xbox")

        try:
            choice = int(input("Number => "))
        except ValueError:
            print("Enter a Number from the List, Numbnut.")
            continue

        if choice == 1:
            print("######################")
            print("###### Nintendo ######")
            print("######################")
            print("1. Gamecube")
            print("2. Nintendo Wii")
            print("3. Nintendo Wii U")
            try:
                nin_choice = int(input("Number => "))
            except ValueError:
                print("Enter a Number from the List, Numbnut.")
                continue
            
            if nin_choice == 1:
                return GC_URL
            elif nin_choice == 2:
                return WII_URL
            elif nin_choice == 3:
                return WII_U_URL
            else:
                print("Enter a Number from the List, Numbnut.")
                continue

        elif choice == 2:
            print("################")
            print("###### Sony ######")
            print("################")
            print("1. PlayStation 1")
            print("2. PlayStation 2")
            print("3. PlayStation 3")
            try:
                sony_choice = int(input("Number => "))
            except ValueError:
                print("Enter a Number from the List, Numbnut.")
                continue
            
            if sony_choice == 1:
                return PS1_URL
            elif sony_choice == 2:
                return PS2_URL
            elif sony_choice == 3:
                return PS3_URL
            else:
                print("Enter a Number from the List, Numbnut.")
                continue

        elif choice == 3:
            print("################")
            print("###### Xbox ######")
            print("################")
            print("1. Xbox Original")
            print("2. Xbox 360")
            try:
                xbox_choice = int(input("Number => "))
            except ValueError:
                print("Enter a Number from the List, Numbnut.")
                continue
            
            if xbox_choice == 1:
                return XBOX_URL
            elif xbox_choice == 2:
                return XBOX360_URL
            else:
                print("Enter a Number from the List, Numbnut.")
                continue

        else:
            print("Enter a Number from the List, Numbnut.")
            continue

URL = get_correct_url()

r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')

links = [a.get('href') for a in soup.find_all('a') if a.get('href')] # type: ignore - For some reason, it thinks there is an error here for no reason

matches = []


print("#################################################")
print("###### Scrapes Data From Myrient.erista.me ######")
print("#################################################")

def get_sort_value():
    """
    This function prompts the user to enter a game name and returns the input as the sort value.
    :return: The function `get_sort_value()` is returning the value entered by the user when prompted to
    enter a game name.
    """
    print("Sometimes the Game Names are kind of finnicky, just play around with how its spelt")
    sort = input("Enter Game Name: ")
    
    return sort

def sort_request(sort):
    """
    The function `sort_request` searches for matches in href attributes of anchor tags and allows the
    user to select and retrieve a download URL and game name.
    
    :param sort: The `sort_request` function takes a parameter `sort` which is used to filter and sort
    the results based on the provided input. The function searches for all anchor tags (`<a>`) in the
    HTML content (assuming `soup` is a BeautifulSoup object) and extracts the `href` attribute
    :return: The function `sort_request` returns a tuple containing the download URL and the name of the
    game. If there are matches found based on the `sort` parameter provided, it will print a numbered
    list of game names, prompt the user to enter a number corresponding to their choice, and then return
    the download URL and game name based on the user's selection. If no matches are found, it will exit
    the function with None Values, which will then come into play later on the program.
    """
    for a in soup.find_all("a"):
        href = a.get("href")  # type: ignore - For some reason, it thinks there is an error here for no reason
        text = a.get_text(strip=True)

        if href and sort.lower() in href.lower():  # type: ignore - For some reason, it thinks there is an error here for no reason
            matches.append((text, href))

    if matches:
        list_amount = len(matches)
        for number, name in enumerate(matches, start = 1):
            print(f"{number}. {name[0]}")
        while True:
            try:
                choice = int(input("Enter Number: "))
            except ValueError:
                print("Why did you enter something other than a number, are u stupid?")
                continue
            if choice > list_amount or choice < 1:
                print("Why did you enter a number thats not on the menu, are u stupid?")
                continue
            else:
                index = choice - 1
                game = matches[index]
                game_name = game[0]
                download_url = f"{URL.split('?')[0]}{game[1]}"
                return download_url, game_name
    else:
        download_url = None
        game_name = None
        return download_url, game_name

def download_file(url, output_path=None):
    """
    The `download_file` function downloads a file from a given URL with progress tracking and error
    handling.
    
    :param url: The `url` parameter in the `download_file` function is the URL from which you want to
    download a file
    :param output_path: The `output_path` parameter in the `download_file` function is used to specify
    the location where the downloaded file should be saved on the local system. If the `output_path` is
    not provided when calling the function, it defaults to the last segment of the URL (extracted using
    `url
    """
    if output_path is None:
        output_path = url.split("/")[-1]

    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024 

        with open(output_path, 'wb') as file, tqdm(
            desc=output_path,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(block_size):
                file.write(data)
                bar.update(len(data))
        
        print(f"\n✅ Download completed: {output_path}")
    except KeyboardInterrupt:
        print("\n❌ Download cancelled by user.")
        if os.path.exists(output_path):
            os.remove(output_path)
            print(f"🧹 Partial file deleted: {output_path}")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


sort = get_sort_value()

download_tuple = sort_request(sort)
game_name = download_tuple[1]
download_url = download_tuple[0]
if game_name is None or download_url is None:
    print("No Game Matches Found")
    print("Exiting Program...")
else:
    download_file(download_url, game_name)
