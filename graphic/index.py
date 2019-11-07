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

def builder():
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
