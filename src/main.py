import argparse


def main(ged_path: str, output_path: str) -> None:
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GEDCOM to CSV")
    parser.add_argument("ged_path", type=str, help="Path to GEDCOM file")
    parser.add_argument("output_path", type=str, help="Path to output CSV file")

    main(**vars(parser.parse_args()))
