from integraciones.uniprot_client import *
import click
from integraciones.run_blast import *
import os

def saveProteinFasta(filename, protein):

    newpath = "./integraciones/proteins"
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    with open(newpath + "/" + filename + ".fasta", "a") as file:
        file.write("> " + filename + "\n" + protein)

@click.group()
def main():
    pass

@main.command()
@click.argument('protein', required=True)
def query_protein(protein):
    uniprotClient=UniprotClient()
    #default test protein

    response = uniprotClient.getSequenceFromProtein(protein)
    
    saveProteinFasta(protein, response)
    print (response)

@main.command()
@click.argument('protein', required=True)
@click.argument('database', required=True)
def run_blast(protein, database):

    result = check_db(database)

    if result == 2:
        dbfile = input("Database not found, insert database file: ")

    add_database(dbfile, database)

    run_query(protein, database)


if __name__ == '__main__':
    main()

