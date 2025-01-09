# gedcom2wiki
Convert GEDCOM to a Wiki style family tree along with some data validation on the tree.

Most examples I've seen online either require you to post information to a public website or are old outdates programs. 

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/nkwade/gedcom2wiki.git
    cd gedcom2wiki
    ```

2. Create a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Covert GEDCOM to Wiki

To convert a GEDCOM file to a Wiki style family tree, run the following command:

```bash
python main.py --ged_path <path_to_gedcom_file> --output_path <output_directory> [options]
```

### Options

- `--ged_path`: Path to the GEDCOM file
- `--output_path`: Path to the output directory (default: `out/`)
- `--graph`: Generate a graph of the family tree (currently not working)
- `--verbose`: Print verbose output
- `--use_cache`: Use cache if available
- `--write_cache`: Write cache after processing (if one does not exists, use --force to overwrite cache)
- `--validate`: Validate the GEDCOM data and create a data validation report (at bottom of index file)
- `--force`: Forces overwriting current cache (if it exists)

### Example

```bash
python main.py --ged_path my_family.ged --output_path output/ --graph --verbose
```

## Support

I (nkwade) should be paying attention to any Github pull requests, but reach out to gedcom@wade.dev to get in contact with me personally. 
