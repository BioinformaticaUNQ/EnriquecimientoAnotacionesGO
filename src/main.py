from integraciones.uniprot_client import UniprotClient, InvalidRequestException

import click
from integraciones.run_blast import *
import os
import sys

## pathlib

def saveProteinFasta(filename, protein):

    newpath = "./integraciones/proteins"
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    with open(newpath + "/" + filename + ".fasta", "w") as file:
        file.write("> " + filename + "\n" + protein)

@click.group()
def main():
    pass

@main.command(short_help='Retorna los terminos go para una proteina.')
@click.argument('protein', required=True)
def get_GoTerms(protein):
    uniprotClient=UniprotClient()

    response = uniprotClient.getCrossReferences(protein)
    
    print (response)


@main.command(short_help='Retorna una secuencia de aminoacidos para la proteina solicitada.')
@click.argument('protein', required=True)
def query_protein(protein):


    uniprotClient=UniprotClient()

    try:
        response = uniprotClient.getSequenceFromProtein(protein)
        saveProteinFasta(protein, response)
        print (response)
    except InvalidRequestException:
        InvalidRequestException.printMe()
    except Exception:
        print ("OCURRIÓ UN ERROR INESPERADO")
    
    
    



class HelpfulCmd(click.Command):
    def format_help(self, ctx, formatter):
        click.echo("Usage: main.py run-blast PROTEIN DATABASE [OPTIONS]")
        click.echo(show_help())


@main.command(short_help="Ejecuta una corrida blast y retorna los resultados de tal corrida.", 
              cls=HelpfulCmd,
              context_settings=dict(
                ignore_unknown_options=True,
                allow_extra_args=True,
))
@click.argument('protein', required= True)
@click.argument('database',required= True)
def run_blast(protein, database):

    
    result = check_db(database)

    if result == 2:
        dbfile = input("Database not found, insert database file: ")
        add_database(dbfile, database)

    run_query(protein, database, sys.argv[4:])


if __name__ == '__main__':
    main()
