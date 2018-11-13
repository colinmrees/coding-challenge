#!/usr/bin/env bash

# Program Execution Script, with the input directory venmo_input and output the files in the directory venmo_output
python ./src/rolling_median.py -i ./venmo_input/venmo-trans.txt -o ./venmo_output/output.txt -b
