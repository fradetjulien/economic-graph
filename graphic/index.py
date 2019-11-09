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

# Check if the row correspond to the Equilibrium Price and Quantity
def setEquilibrium(ranges, quantityDemanded, quantitySupply, price):
    if (quantityDemanded.isdecimal() and quantitySupply.isdecimal() and price.isdecimal() and
        (int(quantityDemanded) == int(quantitySupply))):
        ranges["equilibriumPrice"] = price
        ranges["equilibriumQuantity"] = quantityDemanded
        return ranges
    return ranges

# Set the highest and lowest value for the price, quantity demanded and quantity supply
def setMinAndMaxValues(key, data):
    try:
        if (data[key]["all"]):
            data[key]["lowest"] = min(data[key]["all"])
            data[key]["highest"] = max(data[key]["all"])
    except:
        return data
    return data

# Set data for each row
def setDataByRow(item, value, data):
    if item.isdecimal():
        data[value]["all"].append(int(item))
    return data

# Fill and sort data inside the dictionnary
def fillData(row, data):
    keys = { "price": 0, "quantityDemanded": 1, "quantitySupply": 2 }
    for (key, value) in keys.items():
        data = setDataByRow(row[value], key, data)
    if data["equilibriumPrice"] == None:
        data = setEquilibrium(data, row[1], row[2], row[0])
    return data

# Clean each row of any whitespace
def cleanRow(row):
    newRow = []
    for item in row:
        item = item.strip()
        newRow.append(item)
    del row
    return (newRow)

# Initialization of the dictionary which will contain all the results
def initData():
    data = {
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
        },
        "equilibriumPrice": None,
        "equilibriumQuantity": None
    }
    return (data)

# Open and read the data inside the CSV file
def getData(file):
    data = initData()
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            row = cleanRow(row)
            data = fillData(row, data)
    for key in data.keys():
        data = setMinAndMaxValues(key, data)
    return data

# Display the founded results in the console
def displayResults(data):
    print("The equilibrium price is equal to {} and the equilibrium quantity is equal to {}.".format(data["equilibriumPrice"], data["equilibriumQuantity"]))
    print("The minimum price is {}$ and the maximum price is {}$.".format(data["price"]["lowest"], data["price"]["highest"]))
    print("The lowest quantity demanded is equal to {} and the highest quantity demanded is equal to {}.".format(data["quantityDemanded"]["lowest"], data["quantityDemanded"]["highest"]))
    print("The lowest quantity supply is equal to {} and the highest quantity supply is equal to {}.".format(data["quantitySupply"]["lowest"], data["quantitySupply"]["highest"]))

# Build the final graph and display the results
def builder(file):
    data = getData(file)
    plt.plot(data["quantityDemanded"]["all"],data["price"]["all"])
    plt.plot(data["quantitySupply"]["all"], data["price"]["all"])
    plt.legend(["Demand","Supply"])
    plt.ylabel("Price")
    plt.xlabel("Supply and Demand Quantity")
    plt.suptitle("Demand and Supply schedule")
    displayResults(data)
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
