#!/usr/bin/env bash

for file in ./data/bashinput/*.txt ; do
        python3 ./chunk_to_graph.py -i "$file" \
                -p promts/prompt_pilou02.txt \
                -o "${file%.txt}".json ;
        mv "${file%.txt}".json ./data/bashoutput/ ;
done
