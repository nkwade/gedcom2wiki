import argparse

from .gedcom.parse import parse_gedcom  # type: ignore
from .gedcom.tree import FamilyTree  # type: ignore

from .graph.tree_builder import generate_hierarchical_tree  # type: ignore

from .wiki.build import generate_wiki_pages  # type: ignore
import sys

import time


def main(
    ged_path: str = "C:\\Users\\beake\\Documents\\dev\\gedcom2wiki\\wade.ged",
    output_path: str = "out/",
    graph: bool = False,
    verbose: bool = True,
) -> None:

    start = time.time()

    # Parse GEDCOM file
    with open(ged_path, encoding="utf-8", errors="ignore") as f:
        gedcom_text = f.read()
    ft: FamilyTree = parse_gedcom(gedcom_text)

    if graph:
        generate_hierarchical_tree(ft, "out/graph/")

    if verbose:
        with open("out/verbose.txt", "w", encoding="utf-8", errors="ignore") as f:
            for person_id, person in ft.persons.items():
                f.write(person.__repr__() + "\n")

    # Generate wiki pages for family tree
    generate_wiki_pages(ft, output_path)

    print(f"Total Time: {time.time() - start:.2f} Seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GEDCOM to CSV")
    parser.add_argument("--ged_path", type=str, help="Path to GEDCOM file")
    parser.add_argument("--output_path", type=str, help="Path to output CSV file")
    parser.add_argument(
        "--graph",
        action="store_true",
        help="Generate a graph of the family tree",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print verbose output",
    )

    args = parser.parse_args()
    main_kwargs = {}
    if args.ged_path:
        main_kwargs["ged_path"] = args.ged_path
    if args.output_path:
        main_kwargs["output_path"] = args.output_path
    if args.graph:
        main_kwargs["graph"] = args.graph
    if args.verbose:
        main_kwargs["verbose"] = args.verbose

    main(**main_kwargs)
