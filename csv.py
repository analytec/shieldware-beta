import csv

# Takes CSV filename as input and returns list
def csv_to_list(filename):
    results = []
    with open(filename) as csvfile:
        filereader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
        for row in filereader: # each row is a list
            results.append(row)
    return results

print(csv_to_list('csv/accounts.csv'))
