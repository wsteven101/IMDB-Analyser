import csv
import requests
import gzip
import numpy as np
import pandas as pd
import os.path
import binascii
import datetime


#######################################################################
# Display the main menu
#######################################################################
def main_menu():
    print("  ")
    print("Select a search:")
    print("  1) Number of Films Released For All Years")
    print("  2) Number of Films For a Specific Year")
    print("  3) The most frequent occuring word/s within film all titles for a range of years")
    print("  4) The most frequent occuring word/s within film all titles across all years")
    print("  5) The most frequent occuring word/s within film all titles displayed for each year")
    print("  9) Exit")
    option_selected = int(input())
    print("  ")
    return option_selected

#######################################################################
# Display the number of movies in a specific year selected by the user
#######################################################################
def how_many_films_in_a_year(film_frame):
	print("Enter a year to find how many films were released in that year.")
	print("Enter search year: ")
	search_year = int(input())
	year_frame = film_frame.loc[(film_frame['startYear'] == search_year)]
	no_of_films_in_year = year_frame.startYear.count()
	msg = "The number of films in the year {} is {} \n\n".format(search_year,no_of_films_in_year)
	print(msg)

#################################################################
# Display the number of movies released in each year since 1870
#################################################################
def display_no_of_movies_for_every_year(film_frame):

    years_frame = film_frame.groupby('startYear') 
    current_year = datetime.datetime.now().year

    for start_year, start_year_group in years_frame:
        if ((start_year > 1870) and (start_year <= current_year)):
            start_year_count = start_year_group['tconst'].count()
            print( start_year, start_year_count )

###############3Y##########################################
# Sort key helper function 
#########################################################
def is_excluded(w):

    if w.lower() in ["part","episode"]:
        return True
    if w.lower() in ["january","february","march","april","may","june","july","august","september","october","november","december"]:
        return True
    if w.isnumeric():
        return True
    return False

###############3Y##########################################
# Sort key helper function 
#########################################################
def wordCountSortKey(w):

        return w[1]
	
#########################################################
# Retrieves the most frequent word in in the film titles
#########################################################
def display_most_frequent_title_word(film_frame, start_year, end_year):

    if (start_year == 0):
        start_year = film_frame['startYear'].min()
        end_year = datetime.datetime.now().year

    year_frame = film_frame.loc[((film_frame['startYear'] >= start_year) & (film_frame['startYear'] <= end_year))]

    word_dict = dict()
    for index, film_row in year_frame.iterrows():

        words = list() 
        if film_row['primaryTitle']: 
            words = film_row['primaryTitle'].split()

        for word in words:
            if len(word) > 3 and word[0] != '#' and not is_excluded(word):
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1    

    word_count_list = list(word_dict.items())
    word_count_list.sort(reverse=True, key=wordCountSortKey)
    print ("The word or words, with more than 3 characters, that occured with the highest and same frequency within film titles are")
    print("{:<15s}    {:<15s}   {:<30s}".format("Position","Frequency","Word"))
    print("{:-<68s}".format(" "))
    for idx in range(1,30):
        print("{:<15d}    {:<15d}   {:<30s}".format(idx,word_count_list[idx][1],word_count_list[idx][0]))
    print("")

#########################################################
# Retrieves the most frequent word in in the film titles
# displaying the most frequent words for each year
# rather than across years
#########################################################
def display_most_frequent_title_word_summary(film_frame, start_year, end_year):

    if (start_year == 0):
        start_year = film_frame['startYear'].min()
        end_year = pd.datetime.now().year

    print ("The word or words, with more than 3 characters, that occured with the highest and same frequency within film titles are")
    for year in range(start_year,end_year):
        year_frame = film_frame.loc[(film_frame['startYear'] == year)]

        word_dict = dict()
        for index, film_row in year_frame.iterrows():

            words = list() 
            if film_row['primaryTitle']: 
                words = film_row['primaryTitle'].split()

            for word in words:
                if len(word) > 3 and word[0] != '#' and not is_excluded(word):
                    if word in word_dict:
                        word_dict[word] += 1
                    else:
                        word_dict[word] = 1    

        word_count_list = list(word_dict.items())
        word_count_list.sort(reverse=True, key=wordCountSortKey)

        display_word_limit = 40
        if len(word_count_list) < display_word_limit:
            display_word_limit = word_count_list.count

        display_line = str(year) + ": "
        for idx in range(0,display_word_limit):
            display_line += word_count_list[idx][0] 

            if (idx != display_word_limit):
                display_line += ", "

        print (display_line)
    
    print("")

#########################################################
# Retrieves the most frequent word in in the film titles
# displaying the most frequent words for each year
# rather than across years
#########################################################
def display_most_frequent_title_word_by_year_summary(film_frame):

    print("Enter a year to find the most frequent film titles for a range of years.")
    print("Enter start of year range: ")
    start_year = int(input())
    print("Enter end of year range: ")
    end_year = int(input())
    display_most_frequent_title_word_summary(film_frame, start_year, end_year)

#########################################################
# Retrieves the most frequent word in in the film titles
# within a year range
#########################################################
def display_most_frequent_title_word_by_year_range(film_frame):

    print("Enter a year to find the most frequent film titles for a range of years.")
    print("Enter start of year range: ")
    start_year = int(input())
    print("Enter end of year range: ")
    end_year = int(input())
    display_most_frequent_title_word(film_frame, start_year, end_year)

#########################################################
# main body starts here
#########################################################

gz_imdbfilename='imdb_film_titles.tsv.gz'
txt_imdbfilename='imdb_film_titles.txt'
imdburl = 'https://datasets.imdbws.com/title.basics.tsv.gz'
namefile = "imdb_film_titles.txt"

if not os.path.isfile(gz_imdbfilename): 

     # download file
    print('Downloading file from IMDB with url' + imdburl)
    res = requests.get(imdburl, allow_redirects=True)
    open(gz_imdbfilename,'wb').write(res.content)
    
if not os.path.isfile(txt_imdbfilename): 

    print('Unzipping and untarring downloaded file ' + gz_imdbfilename)
    gznamefile = gzip.open(gz_imdbfilename)
    namefile_content =  gznamefile.read()
     # convert binary contents to ascii whilst skipping incompatible characters
    namefile_content_str = str(namefile_content, encoding ='ascii',errors='ignore')
    namefile = open(txt_imdbfilename, "w") 
    namefile.write(namefile_content_str)
    namefile.close()

print("Reading data...")
film_frame = pd.read_csv(txt_imdbfilename,quoting=csv.QUOTE_NONE, na_values='\\N',  delimiter='\t',  dtype={'tconst': str, 'titleType': str, 'primaryTitle': str, 'originalTitle': str, 'isAdult': int, 'startYear': str, 'endYear': str, 'runtimeMinutes': str, 'genres': str})

# clean data, reformat strings to integers
print("Cleaning data...")
film_frame['primaryTitle'] = film_frame['primaryTitle'].fillna('')
film_frame['startYear'] = film_frame['startYear'].fillna(0)
film_frame['startYear'] = pd.to_numeric(film_frame['startYear']) 
film_frame['endYear'] = film_frame['endYear'].fillna(0)
film_frame['endYear'] = pd.to_numeric(film_frame['endYear']) 
film_frame['runtimeMinutes'] = film_frame['runtimeMinutes'].fillna(0)
film_frame['runtimeMinutes'] = pd.to_numeric(film_frame['runtimeMinutes']) 

option_selected = main_menu()
while (option_selected != 9):
    if (option_selected == 1):
        display_no_of_movies_for_every_year(film_frame)
    if (option_selected == 2):
        how_many_films_in_a_year(film_frame)
    if (option_selected == 3):
        display_most_frequent_title_word_by_year_range(film_frame)
    if (option_selected == 4):
        display_most_frequent_title_word(film_frame,0,9999)
    if (option_selected == 5):
        display_most_frequent_title_word_by_year_summary(film_frame)
    option_selected = main_menu()



