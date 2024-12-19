import sys


def extract_tags(gedcom_file):
    tags = set()
    with open(gedcom_file, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            line = line.strip()
            try:
                number = line.split()[0]
                if number == '0' or not number.isdigit():
                    continue
                words = line.split()
                if len(words) >= 2:
                    tags.add(words[1])
            except IndexError:
                continue
    return tags


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_tags.py filename.ged")
    else:
        tags = extract_tags(sys.argv[1])
        tags = sorted(tags)
        with open("tags.txt", "w") as file:
            for tag in tags:
                file.write(tag + "\n")
