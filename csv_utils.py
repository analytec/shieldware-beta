import csv

# Takes CSV filename as input and returns list
def csv_to_list(filename):
    results = []
    with open(filename) as csvfile:
        filereader = csv.reader(csvfile) # change contents to floats
        for row in filereader: # each row is a list
            results.append(row)
    return [element[0] for element in results] # return first column (usernames) only
