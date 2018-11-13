#Insight Data Engineering Coding Challenge
Colin M. Rees

This project fulfills the following specifications:

- Use Venmo payments that stream in to build a  graph of users and their relationship with one another.

- Calculate the median degree of a vertex in a graph and update this each time a new Venmo payment appears. You will be calculating the median degree across a 60-second sliding window.

This repository contains the following files and directories:
	README.md
This readme
	run.sh
Shell script for running the solution using input files in the current directory
	src/rolling_median.py
Main code for the solution. Written in Python 3.6 syntax.
	venmo_input/venmo-trans.txt
Input file containing venmo transactions in the following json format: {"created_time": "2014-03-27T04:28:20Z", "target": "Jamie-Korn", "actor": "Jordan-Gruber"}
	venmo_output/output.txt
Output file containing median degree across verticies in the user transaction graph after each record is read from the input file.
	insight_testsuite/
Testing script and input files for unit testing.

##Usage

python ./src/rolling_median.py -i [input file] -o [output file] [-b]
The optional -b flag will output the runtime in seconds for benchmarking purposes

##Dependencies

The following non-standard python modules are utilized for this solution
	pandas
	networkx
in addition to the following standard modules.
	sys
	time
	datetime
	getopt