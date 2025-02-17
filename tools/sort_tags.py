import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# Import the GedcomTag class
from gedcom.fact import GedcomTag

# from src.gedcom.fact import GedcomTag

with open("tags.txt", "w") as file:
    for tag in sorted(GedcomTag.__members__.items(), key=lambda item: item[0]):
        file.write(f'{tag[1].name} = "{tag[1].value}"\n')
