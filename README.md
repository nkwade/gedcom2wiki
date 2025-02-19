# gedcom2wiki
Convert GEDCOM to a Wiki style family tree along with some data validation on the tree. This program will go through a GEDCOM file and generate a Wikipedia-style page for the whole family tree, a page for each family, a page for each person, and a data validation report. 

Most examples I've seen online either require you to post information to a public website or are old outdated programs, so I decided to make my own.
I built this because 1) sharing family trees from standard websites like Ancestry.com or MyHeritage.com sucks and 2) they are great to edit and research family trees, but suck for just viewing people/families. Being able to easily just search a person or family and then reading all their facts and click through to other people is much more intuitive for those that haven't used the standard websites.

Hope this helps your family tree!

### Disclaimer
I've been told by people that I should add a disclaimer that this program DOES NOT privatize any information at all. I don't plan on writing a module for this on the Python code, but if I make this a Gramps add-on I will use their module to help detect living people and privatize that information. Keeping information private is up to you, password/permission protect any Wiki files you want to upload to the internet if you choose to do so. I am not responsible for anything related to data or AI if you choose to use LLM generation. If you clone and generate the Wiki files locally no data will leave your computer unless you choose to share it. LLM generation is done locally using Ollama and data does not leave the computer, please refer to Ollama & Meta LLama for more information. 

## Link to example Royal Family Tree Wiki
https://wade.dev/royaltreewiki/index.html

## Requirements
- Python 3+ (personally used 3.10): https://www.python.org/downloads/
- Git: https://git-scm.com/downloads

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

## LLM Biography Generation
If you want to use LLM biography generation run the command below. This will install ollama, pull llama3.1:8b, and run it in the background. Feel free to change the model as needed. Another disclaimer: I am not responsible for any data given to the model, output from any AI models, ensuring compatability, costs incurred with running a GPU intensive task like this, or anything related to LLM biography generation. This is purely a tool that you can choose to incorporate or not. 

```bash
./llama.sh
```

Then once this is complete you can add the option to generate bio's for everyone in your tree. 
```bash
--use_llm
```

## Covert GEDCOM to Wiki

To convert a GEDCOM file to a Wiki style family tree, run the following command:

```bash
python src/main.py --ged_path <path_to_gedcom_file> --output_path <output_directory> [options]
```

### Options

- `--ged_path`: Path to the GEDCOM file (default: `royal92.ged`)
- `--output_path`: Path to the output directory (default: `out/`)
- `--verbose`: Writes verbose output to `out/verbose.txt` (default: False)
- `--use_cache`: Use cache if available (default: False)
- `--write_cache`: Write cache after processing if one does not exists, use `--force` to overwrite cache (default: True)
- `--validate`: Validate the GEDCOM data and create a data validation report at bottom of index file (default: True)
- `--force`: Forces overwriting current cache if cache already exists (default: False)
- `--use_llm`: This will check to ensure Ollama is running and then generate LLM bio's for everyone in your tree. 

Not Working: `--graph`: Generate a graph of the family tree

### Example Using The Royal Family Tree

```bash
python src/main.py --ged_path royal92.ged --output_path output/ --verbose
```

## View Wiki

After running the program you will see a line giving you the direct link that should open the index.html file in your browser. If not you can either copy that file:///<path_to_index.html> and paste that in your web browser or find the `index.html` file in your specified output folder (default: `out/`).
Example line: `Open the wiki at: file:///D:/dev/gedcom2wiki/out/index.html`

## Example Images Of Wiki
![image](https://github.com/user-attachments/assets/510412cd-6bce-4088-8dc9-aed0028373e5)
![image](https://github.com/user-attachments/assets/6634ab1e-23e0-4393-9696-9f190f48a79a)
![image](https://github.com/user-attachments/assets/020c437d-c922-4a3c-9096-ea56d9bb65cf)
![image](https://github.com/user-attachments/assets/27c836c5-30f4-4072-96e8-f655b1abe8eb)




## Support

I (nkwade) should be paying attention to any Github pull requests, but reach out to gedcom@wade.dev to get in contact with me personally about this project. 
