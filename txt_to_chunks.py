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
    "-rh",
    "--remove-hyphenation",
    dest="remove_hyphenation",
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
md_files = []

for root, dirs, files in os.walk(args.input_directory):
    for file in files:
        if file.endswith("_md.txt"):
            md_files.append(os.path.join(root, file))

# Now md_files contains all the file paths ending with _md.txt
if args.verbose:
    print(len(md_files))
    # print(md_files)

# Remove items containing the substring "1_Meta" from the list
md_files = [file for file in md_files if "1_Meta" not in file]

#  Prepare files for splitting
# ==============================================================================

# Put footnotes back into their context




#     * optionally strip html tags from markdown
#     * remove hyphenation
#     * Create one document per family
#         * remove repeating headers and footers
#         * remove repeating numbering
# * Split familiy documents into separate person chunks
#     * write each person chunk to a new file
#     * keep the file name of the original text files for reference