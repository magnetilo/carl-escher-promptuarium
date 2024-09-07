# GLAMhack24 - Keller-Escher's Promptuarium

Challenge...

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

Turn 

Prompt:
````
In the following, I will give you input strings and you should parse it into a json as I will describe now. The input strings contain informations about historic families. The first person is always a male person (father) that is identified by a number within his family tree. Normally, the male is married to a female person (mother) introduced with the abbreviation ux. for uxor. Sometimes, the male person had a second wife or even more. The wives are sometimes further specified through noting their father, again possibly with his own identification number in their family tree. After the parents follow their children. Male children are sometimes described with a number, indicating their own identification number in the family tree. For some children, there is also their spouse listed, again possibly with its own identification number in their family tree.

The output should be in JSON, without the marks for the code block. So don't use the following sings, just straight JSON:

```json
```

The input should be parsed into the following json structure containing all the persons mentioned in the input string, as well as all the relations between the persons: 

{
    "persons": [
        {
            "person_number": 1,  # The number specifying each person in the input string. Should go from 1, 2, 3, …
            "family_name": "Billeter",  # The name of the family denoted at the top of the input string.
            "family_id": "<family_name><male identifier>",  # This identifier is important for being able to
                                                                                        # reconstruct the family relations. It is a string 
                                                                                        # combining the family_name and the male identifier
                                                                                        # with zero padding to four digits. The male identifier 
                                                                                        # is either denoted by the first number before 
                                                                                        # decimal dot preceding the father, or as an 
                                                                                        # identification number following the father of the 
                                                                                        # wive or the male children.
                                                                                        # Null for women.
            "father_family_id": "<family_name><male identifier of father>",  # All children are linked to their fathers with the family_id 
                                                                                                                 # of their father. This id is the family_id of the father.
                                                                                                                 # The father_family_id of the father is the digit after the decimal 
                                                                                                                 # point preceding the fathers name.
            "given_name": "Susanna",  # The given_name of each person.
            "birth_year": 1687,  # The birth year of each person, sometimes denoted after the person: <birth_year> - <death_year>. Can be null.
            "death_year": null,  # The year of death of each person, , sometimes denoted after the person: <birth_year> - <death_year>. Can be null.
            "profession": "Pfister",  # Sometimes the persons are further specified through their profession. Can be null.
            "husband_family_id": "Geiger0006" # The family_id of a woman's husband. Null for men.
        },
        {
            "person_number": 2,
            ...
        },
        ... 
    ],
    "relations": [
        {
            "person_number_1": 1,  # person_number of the first person
            "person_number_2": 2,  # person_number of the second person
            "relation_type": "<relation_type>"  # relation_type specifying the relation between person_number_1 
                                                                  # and person_number_2. One of ["HUSBAND_WIFE", "FATHER_DAUGHTER", "MOTHER_DAUGHTER"]
        },
        {
                "person_number_1": 1,
                "person_number_2": 3,
                "relation_type": "<relation_type>"
        },
        ...
    ]
}

-------------------------------------------
Example:

<input_string>
Billeter

1\. Heinrich Billeter der Pfister
von Mänedorf ward Burger & 
Zftr z. Weggen 1609
ux. Aa Maria Wirth
> Hs. Caspar 1613-      No 2

---
[Dazu auf S. 224:]
No 2 Pfr. zu Zumikon 1634 zu Wipkingen 1637
Alumnatsinspektor eod. Pfr. zu Albisrie-
den 1638

---

> Susanna 1615-1644
m. 1633 Christoph Geiger No 6
Pfr. zu Schwerzenbach 1636 +1665
Adrian 1617 -      No 3
</input_string>

<parsed_json>
{
    "persons": [
        {
            "person_number": 1,
            "family_id": "Billeter0001",
            "father_family_id": null,
            "family_name": "Billeter",
            "given_name": "Heinrich",
            "birth_year": null,
            "death_year": null,
            "profession": "Pfister",
            "origin": "Mänedorf"
        },
...
...
...
````

Parsed result:
```json
{
    “persons”: [
        {
            “person_number”: 1,
            "family_id": "Billeter0001",
            "father_family_id": null,
            "family_name": "Billeter",
            "surname": "Heinrich",
            "birth_year": 1613,
            "death_year": None,
            “profession”: “Pfister”,
            “origin”: “Mänedorf”
        },
        {
            "family_id": None,
            "father_family_id": None,
            "family_name": "Wirth",
            "surname": "Aa Maria",
            "birth_year": None,
            "death_year": None
        },
        {
            "family_id": "Billeter0002",
            "father_family_id": "Billeter0001",
            "family_name": "Billeter",
            "surname": "Hs. Caspar",
            "birth_year": 1613,
            "death_year": None
        },
        ...
    ],
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
        },
        ...
    ]
}
```

## Construct Graph


## Visualization

Visualization using [https://gephi.org/gephi-lite/](https://gephi.org/gephi-lite/).


![graph1](/img/graph1.png)


![graph](/img/graph.png)

