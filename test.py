# -*- coding: utf-8 -*-
import pandas as pd
def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open('txtmetadata.txt', 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number,line.rstrip()))
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results

matched_lines = search_string_in_file('txtmetadata.txt', 'M103825623LC_pyr.tif')
#print('Total Matched lines : ', len(matched_lines))
for elem in matched_lines:
    print(elem[1])
    #print('Line Number = ', elem[0], ' :: Line = ', elem[1])

