from matplotlib import pyplot as plt
import numpy as np
import click
import csv

# Check if the file received in parameter is a correct CSV file
def isCSV(file):
    if not file.endswith('.csv'):
        print("Insert a correct CSV file please.")
        return
    with open(file, newline='') as csvfile:
        try:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            return True
        except csv.Error as e:
            print("Insert a correct CSV file please.")
            return False
    return

# Define the lowest and highest value, store all value
def setRanges(item, value, ranges):
    if item.isdecimal():
        ranges[value]["all"].append(int(item))
        if ranges[value]["lowest"] == None:
            ranges[value]["lowest"] = int(item)
        if ranges[value]["highest"] == None:
            ranges[value]["highest"] = int(item)
        elif int(item) < ranges[value]["lowest"]:
            ranges[value]["lowest"] = int(item)
        elif int(item) > ranges[value]["lowest"]:
            ranges[value]["highest"] = int(item)
    return ranges

# Insert and sort data inside the dictionnary
def fillData(row, ranges):
    ranges = setRanges(row[0], "price", ranges)
    ranges = setRanges(row[1], "quantityDemanded", ranges)
    ranges = setRanges(row[2], "quantitySupply", ranges)
    return ranges

# Clean each row of any whitespace
def cleanRow(row):
    newRow = []
    for item in row:
        item = item.strip()
        newRow.append(item)
    del row
    return (newRow)

# Open and read the data inside the CSV file
def getData(file):
    ranges = {
        "price": {
            "lowest": None,
            "highest": None,
            "all": []
        },
        "quantityDemanded": {
            "lowest": None,
            "highest": None,
            "all": []
        },
        "quantitySupply": {
            "lowest": None,
            "highest": None,
            "all": []
        }
    }
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            row = cleanRow(row)
            ranges = fillData(row, ranges)
    return ranges

# Build the final graph
def builder(file):
    ranges = getData(file)
    plt.plot(ranges["quantityDemanded"]["all"],ranges["price"]["all"])
    plt.plot(ranges["quantitySupply"]["all"], ranges["price"]["all"])
    plt.legend(["Demand","Supply"])
    plt.ylabel("Price")
    plt.xlabel("Supply and Demand Quantity")
    plt.suptitle("Demand and Supply schedule")
    plt.show()
    return

@click.group()
def cli():
    '''Graphic Builder'''

@cli.command('build')
@click.argument('file')
def buildGraphic(file):
    """Build Supply and Demand curve into a graph"""
    if isCSV(file):
        builder(file)
    return

if __name__ == '__main__':
    cli()
