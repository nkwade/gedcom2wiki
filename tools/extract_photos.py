# Usually gedcom exports has links to photos that expire, so run this to get images under the assets/ folder 
import sys

def main(file_path: str):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file.readlines():
            

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_photos.py gedcom.ged")
    
    main(sys.argv[1])