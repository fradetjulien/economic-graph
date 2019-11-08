from matplotlib import pyplot as plt
import numpy as np
import click
import csv

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

def setExtremeQuantity(row, ranges):
    for item in row:
        if item.isdecimal():
            if ranges["quantity"]["lowest"] == None:
                ranges["quantity"]["lowest"] = int(item)
            if ranges["quantity"]["highest"] == None:
                ranges["quantity"]["highest"] = int(item)
            elif int(item) < ranges["quantity"]["lowest"]:
                ranges["quantity"]["lowest"] = int(item)
            elif int(item) > ranges["quantity"]["highest"]:
                ranges["quantity"]["highest"] = int(item)
    return ranges

def setExtremePrice(price, ranges):
    if price.isdecimal():
        if ranges["price"]["lowest"] == None:
            ranges["price"]["lowest"] = int(price)
        if ranges["price"]["highest"] == None:
            ranges["price"]["highest"] = int(price)
        elif int(price) < ranges["price"]["lowest"]:
            ranges["price"]["lowest"] = int(price)
        elif int(price) > ranges["price"]["lowest"]:
            ranges["price"]["highest"] = int(price)
    return ranges

def findExtreme(row, ranges):
    ranges = setExtremePrice(row[0], ranges)
    ranges = setExtremeQuantity(row[1:3], ranges)
    return ranges

def cleanRow(row):
    newRow = []
    for item in row:
        item = item.strip()
        newRow.append(item)
    del row
    return (newRow)

def getData(file):
    ranges = {
        "price": {
            "lowest": None,
            "highest": None
        },
        "quantity": {
            "lowest": None,
            "highest": None
        }
    }
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            row = cleanRow(row)
            ranges = findExtreme(row, ranges)
    return

def builder(file):
    getData(file)
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
