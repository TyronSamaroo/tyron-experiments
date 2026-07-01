import pyfiglet
import random
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Your name
name = "TYRON SAMAROO"

# List of cool ASCII fonts
fonts = ["slant", "big", "block", "starwars", "graffiti", "isometric1", "doom", "larry3d", "rectangles", "speed"]

# Choose a random font
random_font = random.choice(fonts)

# Generate ASCII text
ascii_art = pyfiglet.figlet_format(name, font=random_font)

# List of cool colors
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
random_color = random.choice(colors)

# Print ASCII text with a random color
print(random_color + ascii_art)