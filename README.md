# Gerstein Lab Project

These are a set of programs that I used to parse data files and to generate Bash and Julia scripts based on that data. This program is designed to make Bash and Julia scripts in conjunction with Marc Williams' SubClonalSelection Julia package, found here: https://github.com/marcjwilliams1/SubClonalSelection.jl

## Prerequisites

These files have been tested with Python 3.7+ but should work with different versions of Python, such as versions 2.7+, as well. The SubClonalSelection module requires Julia 0.7.0+. Bash files are designed to be run on Slurm.

## separate_samples.py

This file takes as command-line input a path to a text file that contains sample numbers and VAF values separated by tabs. It outputs a file for each sample that contains every corresponding VAF value.

## list_samples.py

This files takes as command line input a path to a text file that contains sample numbers, and outputs two a files: a list of samples, and an enumerated list of samples, with an id for each sample separated by the sample number by a tab.

## cohort_final.py

This file takes as command-line input a path to a text file with a list of samples and a number, with an optional argument "-g". It creates Bash and Julia scripts based on the samples present in a samples folder. These Bash and Julia scripts are designed to be run in a cluster; each Bash script runs a Julia script that runs multiple samples dependent on the number inputted. If "-g" is included, the Julia script includes graphs.

## make_time_scripts.py

This file takes as command-line input a file of listed VAF values with optional argument "-g", and returns text files that randomly select a predetermined portion of the text file, Bash files, and Julia files that correspond to running SubClonalSelection on those segments of the original file, in addition to running the module with different numbers of iterations. If "-g" is included, the Julia script includes graphs. 

## make_test_script.py

This file runs a test based on the "oneclone.txt" file implemented in the module's native test, and assumes you have the sample file in your current directory. This test includes graphing and calculating capabilities.

## make_results.py

This file parses the ".out" or results files from a given directory and graphs some characteristics of the results, as well as cleaning up results files and outputting them as a new text file.