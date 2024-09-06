#!/usr/bin/env python3
# coding: utf-8

"""
TODO: NEW description
"""

import sys
import argparse
from openai import OpenAI

# documentation: https://pypi.org/project/openai/
#                https://github.com/openai/openai-cookbook/

# Load the API key
try:
    with open('api_key.txt',  encoding="utf8") as file:
        client = OpenAI(api_key=file.read().strip())
except FileNotFoundError:
    print("Error: 'api_key.txt' not found. Please ensure it's in the \
    current directory.")
    sys.exit(1)

# Load the Prompt that is in a separate file for ease of use.
def promptread():
    try:
        with open('prompt.txt', encoding="utf8") as file:
            promptstring = file.read().strip()
    except FileNotFoundError:
        print("Error: 'prompt.txt' not found. Please ensure it's in the current directory.")
        sys.exit(1)
    return promptstring

prompt = promptread()

# Function to read the chunk from a specified file
def chunkread(input_file):
    try:
        with open(input_file, encoding="utf8") as file:
            chunkstring = file.read().strip()
    except FileNotFoundError:
        print(f"Error: '{input_file}' not found. Please ensure it's in the correct directory.")
        sys.exit(1)
    return chunkstring

def chunk2triple(chunk):
    """
    TODO
    """
    response = client.chat.completions.create(
            #model="gpt-3.5-turbo",
            model="gpt-4o",

    messages=[
        {"role": "system", "content":
        # Read the prompt. It is saved in a file and read in earlier.
        prompt 
        },
        {"role": "user", "content": chunk}
    ],
    temperature=0)
    triples = (response.choices[0].message.content
              .strip())
    # triples is the data in triple format (RDF).
    return triples

# Function to save the triples to a specified file
def save_triples(output_file, triples):
    try:
        with open(output_file, "w", encoding="utf8") as file:
            file.write(triples)
    except Exception as e:
        print(f"Error: Unable to write to '{output_file}'. {e}")
        sys.exit(1)


# Main function to handle CLI arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Turtle triples from a chunk of text using OpenAI API.')
    
    # Input and output file arguments
    parser.add_argument('--input', '-i', required=True, help='Input file containing the chunk.')
    parser.add_argument('--output', '-o', required=True, help='Output file to save the triples.')

    # Parse the arguments
    args = parser.parse_args()

    # Read the input chunk
    chunk = chunkread(args.input)

    # Read the input chunk
    #chunk = chunkread()

    # Generate triples using the chunk2triple function (assuming it's defined as in your script)
    triples = chunk2triple(chunk)

    # Save the triples to the output file
    save_triples(args.output, triples)

    print(f"Triples successfully saved to {args.output}")


