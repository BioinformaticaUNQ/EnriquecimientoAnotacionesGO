
from integraciones.uniprot_client import *
import click
from integraciones.blast_client import *
import os
import sys
from integraciones.go_terms import *


## pathlib

uniprotClient=UniprotClient()
blastClient = BlastClient()

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


@main.command(short_help='Download the file needed for GO enrichment')
def download_go_basic_obo():
    download_go_term_field() 
    print ("Go-basic.obo file has been downloaded successfully.")

@main.command(short_help='Compares the GoTerms of 2 proteins and returns a result.')
@click.argument('proteinone', required=True)
@click.argument('proteintwo', required=True)
def compare_goterms(proteinone, proteintwo):
    go_terms1 = uniprotClient.getGoTerms(proteinone)
    go_terms2 = uniprotClient.getGoTerms(proteintwo)

    if go_terms1 is None or go_terms2 is None:
        print("Could not get GO terms for one or both IDs")
        return
  
    compare_go_terms(proteinone,proteintwo,go_terms1,go_terms2)


def getProteinFromUniprot(uniprotId):
    uniprotClient=UniprotClient()

    try:
        response = uniprotClient.getSequenceFromProtein(uniprotId)
        saveProteinFasta(uniprotId, response)
        print (response)
    except InvalidRequestException:
        InvalidRequestException.printMe()
    except Exception:
        print ("OCURRIÓ UN ERROR INESPERADO")

@main.command(short_help='Retorna una secuencia de aminoacidos para la proteina solicitada.')
@click.argument('protein', required=True)
def query_protein(protein):


    getProteinFromUniprot(protein)
    

class HelpfulCmd(click.Command):
    def format_help(self, ctx, formatter):
        click.echo("USAGE: main.py run-blast PROTEIN DATABASE [OPTIONS]")
        click.echo(blastClient.show_help())
        click.echo("-outfmt ha sido desabilitado")


@main.command(short_help="Run a blast protein query.", 
              cls=HelpfulCmd,
              context_settings=dict(
                ignore_unknown_options=True,
                allow_extra_args=True,
))
@click.argument('protein', required= True)
@click.argument('database',required= True)
def run_blast(protein, database):

    args = sys.argv[4:]

    if ("-outfmt" in args):

        outIndex = args.index("-outfmt")
        

        args.pop(outIndex)
        args.pop(outIndex)

    if not "-remote" in args and not blastClient.db_exists(database):
        dbfile = input("Database not found, insert database file: ")
        blastClient.add_database(dbfile, database)

    blastClient.run_query(protein, database, args)


@main.command(short_help='Download Uniprot/Swissprot or Uniprot/Trembl databases.')
@click.option('--swissprot', is_flag=True, default= False )
@click.option('--trembl', is_flag=True, default= False )
def get_database(swissprot, trembl):

    if (swissprot and not blastClient.db_exists('swissprot')):
        blastClient.download_database('swissprot')

    if (trembl and not blastClient.db_exists('trembl')):
        pass

def readFile(filename):
    try:
        file = open(filename, "r") 
        lines= file.read().splitlines()
        file.close() 
        return lines
    except FileNotFoundError:
        print ("El archivo indicado no existe")

@main.command(short_help='Lee desde archivo los diferentes codigos uniprot')
@click.argument('filename', required=True)
def read_file(filename):

    uniprotCodes =readFile(filename)
    if uniprotCodes!=None:

        for eachUniprotCode in uniprotCodes:
            try:
                getProteinFromUniprot(eachUniprotCode)
            except InvalidRequestException:
                InvalidRequestException.printMe()
            
    
@main.command(short_help='Show graph of comparison of 2 go terms')
@click.argument('goTermA', required=True)
@click.argument('goTermB', required=True)
def plotGoTerms(goterma,gotermb):
    plotGOTComparison(goterma,gotermb)

if __name__ == '__main__':
    main()