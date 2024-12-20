# Usually gedcom exports has links to photos that expire, so run this to get images under the assets/ folder
import sys

image_formats = ["jpg", "png"]


def main(file_path: str):
    links: list[str] = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        lines = file.readlines()

        for i in range(len(lines) - 1):
            parts = lines[i].strip().split(" ")

            if len(parts) >= 3 and parts[1] == "FORM" and parts[2] in image_formats:
                next_line_parts = lines[i + 1].split(" ")
                if len(next_line_parts) >= 3 and next_line_parts[1] == "FILE":
                    links.append(next_line_parts[2].strip())

    print(links)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_photos.py gedcom.ged")
    else:
        main(sys.argv[1])
