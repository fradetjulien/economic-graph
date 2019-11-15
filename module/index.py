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
    try:
        with open(file, newline='') as csvfile:
            csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            return True
    except:
        print("Insert a correct CSV file please.")
        return False

def set_equilibrium(data, quantity_demanded, quantity_supply, price):
    '''
    Check if the row correspond to the Equilibrium Price and Quantity
    '''
    if (quantity_demanded.isdecimal() and quantity_supply.isdecimal() and
            price.isdecimal() and (int(quantity_demanded) == int(quantity_supply))):
        data["equilibriumPrice"] = price
        data["equilibriumQuantity"] = quantity_demanded
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
    keys = {"price": 0, "quantity_demanded": 1, "quantity_supply": 2}
    for (key, value) in keys.items():
        data = set_data_by_row(row[value], key, data)
    if data["equilibriumPrice"] is None:
        data = set_equilibrium(data, row[1], row[2], row[0])
    del keys
    return data

def clean_row(row):
    '''
    Clean each row of any whitespace
    '''
    new_row = []
    for item in row:
        item = item.strip()
        new_row.append(item)
    del row
    return new_row

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
        "quantity_demanded": {
            "lowest": None,
            "highest": None,
            "all": []
        },
        "quantity_supply": {
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
          .format(data["quantity_demanded"]["lowest"], data["quantity_demanded"]["highest"]))
    print("The lowest quantity supply is equal to {} and the highest quantity supply is equal to {}."
          .format(data["quantity_supply"]["lowest"], data["quantity_supply"]["highest"]))

def builder(file):
    '''
    Build the final graph and display the results
    '''
    data = get_data(file)
    plt.plot(data["quantity_demanded"]["all"], data["price"]["all"])
    plt.plot(data["quantity_supply"]["all"], data["price"]["all"])
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
@click.argument('file', type=click.Path(exists=True))
def build_graphic(file):
    '''
    Build Supply and Demand curve into a graph
    '''
    if is_csv(file):
        builder(file)

if __name__ == '__main__':
    cli()
