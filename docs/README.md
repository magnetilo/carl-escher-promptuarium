# GLAMhack24 - Keller-Escher's Promptuarium

Challenge...

```json
“relations”: [
        {
            “person_number_1”: 1, 
            “person_number_2”: 2, 
            “relation_type”: “HUSBAND_WIFE”
        },
        {
            “person_number_1”: 1,
            “person_number_2”: 3,
            “relation_type”: “FATHER_CHILD”
        },
        {
            “person_number_1”: 2,
            “person_number_2”: 3,
            “relation_type”: “MOTHER_CHILD”
        },
        {
            “person_number_1”: 1,
            “person_number_2”: 4,
            “relation_type”: “FATHER_CHILD”
        }
```
![test-img](/img/logo.png)

Content:
- [Preprocessing: Building Chunks](#preprocessing:-building-chunks)
- [Prompt Engineering: Chunks to JSON](#prompt-engineering:-chunks-to-json)
- [Construct Graph](#construct-graph)
- [Visualization](#visualization)


## Preprocessing: Building Chunks
### Summary

[`txt_to_chunks.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Frued%2Fcarl-escher-promptuarium%2Ftxt_to_chunks.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22caa600a5-c058-4497-98ed-d7a3aee56710%22%5D "/home/rued/carl-escher-promptuarium/txt_to_chunks.py") is a CLI application designed to process and split text files containing genealogical data about Zurich families. The script performs the following main steps:

1. **Directory Traversal**: It traverses a specified directory to locate text files ending with `_md.txt`.
2. **File Preparation**:
   - Reintegrates footnotes into their context.
   - Optionally strips HTML tags from markdown.
   - Removes hyphenation.
   - Creates one document per family by removing repeating headers, footers, and numbering.
3. **Text Splitting**: Splits family documents into separate chunks for each person and writes these chunks to new files, retaining the original file names for reference.

### Dependencies
- Python 3.11
- argparse
- colorama
- alive_progress

### Usage
The script requires an input directory containing the text files and an output directory for the chunked text files. It also includes options to remove hyphenation and enable verbose logging.

### Example Command
```bash
python txt_to_chunks.py -i /path/to/input-directory -o /path/to/output-directory -rh -v
```

## Prompt Engineering: Chunks to JSON


## Construct Graph


## Visualization


