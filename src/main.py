import argparse
import time
import os

from gedcom.tree import FamilyTree
from graph.tree_builder import generate_hierarchical_tree
from gedcom.parse import parse
from wiki.build import generate_wiki_pages
import pickle


def write_to_cache(ft: FamilyTree, output_folder: str):
    cache_file = os.path.join(output_folder, "cache.pkl")
    with open(cache_file, "wb") as f:
        pickle.dump(ft, f)


def load_from_cache(output_folder: str) -> FamilyTree | None:
    cache_file = os.path.join(output_folder, "cache.pkl")
    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            return pickle.load(f)
    return None


def main(
    ged_path: str = "royal92.ged",
    output_path: str = "out/",
    graph: bool = False,
    verbose: bool = False,
    use_cache: bool = False,
    write_cache: bool = True,
    validate: bool = True,
    force: bool = False,
    use_llm: bool = False,
) -> None:

    start = last = time.time()

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Parse GEDCOM file
    ft: FamilyTree | None = None
    if not use_cache or force:
        ft = parse(ged_path)
        print(f"Time to parse Gedcom: {time.time() - last:.2f}")
        last = time.time()
    if use_cache and not ft:
        ft = load_from_cache(output_path)
        print(f"Time to load from cache: {time.time() - last:.2f}")
        last = time.time()

    if not ft:
        print("No Family Tree Detected Or Critical Error Occured")
        return

    if graph:
        generate_hierarchical_tree(ft, "out/graph/")
        print(f"Time to generate graph tree: {time.time() - last:.2f}")
        last = time.time()

    if verbose:
        with open("out/verbose.txt", "w", encoding="utf-8", errors="ignore") as f:
            for person_id, person in ft.persons.items():
                f.write(person.__repr__() + "\n")
        print(f"Time to write log file: {time.time() - last:.2f}")
        last = time.time()

    if write_cache:
        write_to_cache(ft, output_path)
        print(f"Time to write to cache: {time.time() - last:.2f}")
        last = time.time()

    # Generate wiki pages for family tree
    generate_wiki_pages(ft, output_path, validate, use_llm)
    print(f"Time to generate wiki pages: {time.time() - last:.2f}")
    last = time.time()

    print(f"Total Time: {time.time() - start:.2f} Seconds")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    wiki_path = os.path.join(project_root, output_path, "index.html")
    wiki_path = wiki_path.replace("\\", "/")
    print(f"Open the wiki at: file:///{wiki_path}")


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
    parser.add_argument(
        "--use_cache",
        action="store_true",
        help="Use cache if available",
    )
    parser.add_argument(
        "--write_cache",
        action="store_true",
        help="Write cache after processing",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate the GEDCOM data",
    )
    parser.add_argument(
        "--force", action="store_true", help="Forces parsing of Gedcom file"
    )
    parser.add_argument(
        "--use_llm",
        action="store_true",
        help="Generate LLM biographies for persons",
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
    if args.use_cache:
        main_kwargs["use_cache"] = args.use_cache
    if args.write_cache:
        main_kwargs["write_cache"] = args.write_cache
    if args.validate:
        main_kwargs["validate"] = args.validate
    if args.force:
        main_kwargs["force"] = args.force
    if args.use_llm:
        main_kwargs["use_llm"] = args.use_llm

    main(**main_kwargs)
