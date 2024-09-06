""" 
Copyright 2024 Oliver Waddell

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 """

""" 
Aim: This CLI app creates chunks of text to feed into chunk_to_graph.py

Dependencies:
* Python 3.11
* argparse

Mains steps:

* Travers a directory containing data regarding Zurich families in a number of formats
    * source https://www.e-manuscripta.ch/zuzcmi/content/titleinfo/3530958
    * transcription https://opendata.swiss/de/dataset/promptuarium-genealogicum-des-carl-keller-escher
    * transcription rules https://www.zb.uzh.ch/storage/app/media/ueber-uns/Citizen-Science/Familiengeschichte/Stylesheet_Transkriptionen_Familiengeschichte.pdf
* Choose relevant text files
* Prepare files for splitting
    * Put footnotes back into their context
    * optionally strip html tags from markdown
    * remove hyphenation
    * Create one document per family
        * remove repeating headers and footers
        * remove repeating numbering
* Split familiy documents into separate person chunks
    * write each person chunk to a new file
    * keep the file name of the original text files for reference

"""

import os
import re
import argparse
import pathlib
from datetime import date
import sys
import logging
from colorama import just_fix_windows_console, Fore
from alive_progress import alive_bar

parser = argparse.ArgumentParser()

parser.add_argument(
    "-i",
    "--input-directory",
    dest="input_directory",
    required=True,
    help="Directory containing the text files",
)

parser.add_argument(
    "-o",
    "--output-directory",
    dest="output_directory",
    required=True,
    help="Directory to output the chunked text files to",
)

parser.add_argument(
    "-fns",
    "--fn-delimiter-start",
    dest="footnote_delimiter_start",
    required=False,
    default="FNS",
    help="string to mark beginning of footnote",
)

parser.add_argument(
    "-fne",
    "--fn-delimiter-end",
    dest="footnote_delimiter_end",
    required=False,
    default="FNE",
    help="string to mark end of footnote",
)

parser.add_argument(
    "-rh",
    "--remove-hyphenation",
    dest="remove_hyphenation",
    required=False,
    default=True,
    action="store_true",
)

parser.add_argument(
    "--remove-html",
    dest="remove_html",
    required=False,
    default=True,
    action="store_true",
)


parser.add_argument("-v", "--verbose", dest="verbose", action="store_true")

parser.add_argument(
    "--version",
    action="store_true",
)

args = parser.parse_args()


# get ANSI escapes to work on Windows
just_fix_windows_console()

# output version string and exit
# see https://en.wikipedia.org/wiki/List_of_mythological_places for version codenames
version_string: str = "txt_to_chunks.py version 0.1.0 'Rarohenga'"
if args.version is True:
    print(version_string)
    sys.exit(0)

# configure logging
# set logging level
if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
# use colorama to colorize logging output
logging.addLevelName(
    logging.DEBUG, Fore.BLUE + logging.getLevelName(logging.DEBUG) + Fore.RESET
)
logging.addLevelName(
    logging.INFO, Fore.GREEN + logging.getLevelName(logging.INFO) + Fore.RESET
)
logging.addLevelName(
    logging.WARNING, Fore.YELLOW + logging.getLevelName(logging.WARNING) + Fore.RESET
)
logging.addLevelName(
    logging.ERROR, Fore.RED + logging.getLevelName(logging.ERROR) + Fore.RESET
)
logging.addLevelName(
    logging.CRITICAL, Fore.RED + logging.getLevelName(logging.CRITICAL) + Fore.RESET
)

# check if input directory exists, is readable and contains files

try:
    if not os.path.exists(args.input_directory):
        logging.critical(f"The given directory {args.input_directory} doesn't exist.")
        sys.exit(1)
    if not os.access(args.input_directory, os.R_OK):
        logging.critical(f"The given directory {args.input_directory} cannot be read.")
        sys.exit(1)
    if not any(os.scandir(args.input_directory)):
        logging.critical(f"The given directory {args.input_directory} is empty.")
        sys.exit(1)
except Exception as e:
    logging.critical(f"An error occurred: {e}")
    sys.exit(1)


# traverse the given directory and add all files ending with _md.txt to a list of strings
md_files: list[str] = []

for root, dirs, files in os.walk(args.input_directory):
    for file in files:
        if file.endswith("_md.txt"):
            md_files.append(os.path.join(root, file))

# Now md_files contains all the file paths ending with _md.txt
if args.verbose:
    print(len(md_files))
    # print(md_files)

# Remove items containing the substring "1_Meta" from the list
md_files: list[str] = [file for file in md_files if "1_Meta" not in file]

#  Prepare files for splitting
# ==============================================================================

# write text files to list of strings
texts: list[str] = []
for file in md_files:
    with open(file, "r", encoding="utf-8") as f:
        texts.append(f.read())

# Put footnotes back into their context

# iterate over the list of strings and in each string replace the first occurrence
# of [^fn##] with the text behind the second occurence of [^fn##] in brackets

# regex pattern to match the footnote number
fn_pattern: re.Pattern[str] = re.compile(r"\[\^fn\d+\]")

# regex pattern to match the footnote text delimited by [^fn##]: and following label [^fn##] using a lookahead and allowing for newlines

fn_text_pattern: re.Pattern[str] = re.compile(
    r"^(\[\^fn\d+\]:\s*(.*?))(?=\[\^fn\d+\])", re.DOTALL
)

# iterate over the footnotes and check if a footnote text is found and whether it is preceded by a footnote anchor with the corresponding number earlier in the string
for text in texts:
    fn_matches: list[re.Match[str]] = fn_pattern.finditer(text)
    for match in fn_matches:
        fn_text_match: re.Match[str] = fn_text_pattern.search(text, match.end())
        if fn_text_match:

            # check if the corresponding footnote anchor is missing before trying to replace it by the footnote text
            if not fn_text_match.group(1):
                logging.warning(
                    f"Footnote text {fn_text_match.group(2)} has no corresponding anchor in text {text}"
                )
                continue
            else:
                # replace the footnote anchor with the footnote text
                text: str = text.replace(
                    match.group(), fn_text_match.group(2), 1
                )
                # remove the footnote text from the text
                text: str = re.sub(fn_text_pattern, "", text, 1)
                texts[texts.index(text)] = text


# #     * optionally strip html tags from markdown (dirty solution)

# if args.remove_html:
#     html_pattern: re.Pattern[str] = re.compile(r"<.*?>")
#     for text in texts:
#         text = html_pattern.sub("", text)
#         texts[texts.index(text)] = text

# #     * remove hyphenation if line ends with hyphen and next line starts with lowercase letters
# if args.remove_hyphenation:
#     hyphenation_pattern = re.compile(r"(\w+)-\n(\w+)")
#     for text in texts:
#         text: str = hyphenation_pattern.sub(r"\1\2", text)
#         texts[texts.index(text)] = text

# output the first 5 entries of the texts list
if args.verbose:
    print(texts[:5])


#     * Create one document per family
#         * remove repeating headers and footers
#         * remove repeating numbering
# * Split familiy documents into separate person chunks
#     * write each person chunk to a new file
#     * keep the file name of the original text files for reference
