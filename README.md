# IMDB Analyser

## Techstack: Python

## Description:
### This program enables users to make specific queries against an IMDB file of film titles. A query is, for example, listing the most frequent words used for a film title within a given year or how many films were released in a year.

### This python program downloads an imdb zipped and tarred csv file from the IMDB website containing titles of fims from before the 1900s all the way to the present.
### The program then untars and unzips the file and reads the csv contents into a Panda dataframe from where the data can be queried.
### As the IMDB file is large it will only be downloaded once. To replace the file simply delete the existing downloaded file and the corresponding unzipped file and rerun the program.
###
## Acknowledgements
### Thanks to IMDB for making their data publicly available