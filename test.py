import csv

with open('test.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['test1', 'test2', 'test3'])
