import csv
import click
from matplotlib import pyplot as plt

def is_csv(file):
    '''
    Check if the file received in parameter is a correct CSV file
    '''
    if not file.endswith('.csv'):
        print("Insert a correct CSV file please.")
        return False
    with open(file, newline='') as csvfile:
        try:
            csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            return True
        except csv.Error:
            print("Insert a correct CSV file please.")
            return False
    return

def set_equilibrium(data, quantityDemanded, quantitySupply, price):
    '''
    Check if the row correspond to the Equilibrium Price and Quantity
    '''
    if (quantityDemanded.isdecimal() and quantitySupply.isdecimal() and
            price.isdecimal() and (int(quantityDemanded) == int(quantitySupply))):
        data["equilibriumPrice"] = price
        data["equilibriumQuantity"] = quantityDemanded
        return data
    return data

def set_min_and_max_values(key, data):
    '''
    Set the highest and lowest value for the price, quantity demanded and quantity supply
    '''
    try:
        if data[key]["all"]:
            data[key]["lowest"] = min(data[key]["all"])
            data[key]["highest"] = max(data[key]["all"])
    except:
        return data
    return data

def set_data_by_row(item, value, data):
    '''
    Set data for each row
    '''
    if item.isdecimal():
        data[value]["all"].append(int(item))
    return data

def fill_data(row, data):
    '''
    Fill and sort data inside the dictionnary
    '''
    keys = {"price": 0, "quantityDemanded": 1, "quantitySupply": 2}
    for (key, value) in keys.items():
        data = set_data_by_row(row[value], key, data)
    if data["equilibriumPrice"] == None:
        data = set_equilibrium(data, row[1], row[2], row[0])
    del keys
    return data

def clean_row(row):
    '''
    Clean each row of any whitespace
    '''
    newRow = []
    for item in row:
        item = item.strip()
        newRow.append(item)
    del row
    return newRow

def init_data():
    '''
    Initialization of the dictionary which will contain all the results
    '''
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
    return data

def get_data(file):
    '''
    Open and read the data inside the CSV file
    '''
    data = init_data()
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            row = clean_row(row)
            data = fill_data(row, data)
    for key in data.keys():
        data = set_min_and_max_values(key, data)
    return data

def display_results(data):
    '''
    Display the founded results in the console
    '''
    print("The equilibrium price is equal to {} and the equilibrium quantity is equal to {}."
          .format(data["equilibriumPrice"], data["equilibriumQuantity"]))
    print("The minimum price is {}$ and the maximum price is {}$."
          .format(data["price"]["lowest"], data["price"]["highest"]))
    print("The lowest quantity demanded is equal to {} and the highest quantity demanded is equal to {}."
          .format(data["quantityDemanded"]["lowest"], data["quantityDemanded"]["highest"]))
    print("The lowest quantity supply is equal to {} and the highest quantity supply is equal to {}."
          .format(data["quantitySupply"]["lowest"], data["quantitySupply"]["highest"]))

def builder(file):
    '''
    Build the final graph and display the results
    '''
    data = get_data(file)
    plt.plot(data["quantityDemanded"]["all"], data["price"]["all"])
    plt.plot(data["quantitySupply"]["all"], data["price"]["all"])
    plt.legend(["Demand", "Supply"])
    plt.ylabel("Price")
    plt.xlabel("Supply and Demand Quantity")
    plt.suptitle("Demand and Supply schedule")
    display_results(data)
    plt.show()

@click.group()
def cli():
    '''
    Graphic Builder
    '''

@cli.command('build')
@click.argument('file')
def build_graphic(file):
    '''
    Build Supply and Demand curve into a graph
    '''
    if is_csv(file):
        builder(file)

if __name__ == '__main__':
    cli()
