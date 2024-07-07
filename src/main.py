
from integraciones.uniprot_client import *
import click
from integraciones.blast_client import *
import os
import sys
from integraciones.go_terms import *
import cv2
from screeninfo import get_monitors
from PIL import Image

## pathlib

uniprotClient=UniprotClient()
blastClient = BlastClient()


@click.group()
def main():
    """This tool provides support for Enrichment of Go Notations."""
    pass

@main.command(short_help='Returns all protein\'s GO Terms')
@click.argument('protein', required=True)
def get_GoTerms(protein):
    """Returns all protein\'s GO Terms.
    
    [PROTEIN] is a Uniprot ID of a protein from which we want to obtain the GO Terms."""
    uniprotClient=UniprotClient()

    response = uniprotClient.getCrossReferences(protein)
    
    print (response)


@main.command(short_help='Download the file needed for GO enrichment.')
def download_go_basic_obo():
    """Run this command to download de go-basic definitions from obolibrary.org
    
    This commands only need an Internet Connection"""
    download_go_term_field() 
    print ("Go-basic.obo file has been downloaded successfully.")



@main.command(short_help='Compares the Go Terms of 2 proteins and returns a result.')
@click.argument('proteinone', required=True)
@click.argument('proteintwo', required=True)
def compare_goterms(proteinone, proteintwo):
    """Compares the GO Terms of 2 proteins and returns a result.
    
        [PROTEINONE] is a Uniprot ID of a protein.

        [PROTEINTWO] is a Uniprot ID of an another protein."""

    go_terms1 = uniprotClient.getGoTerms(proteinone)
    go_terms2 = uniprotClient.getGoTerms(proteintwo)

    if go_terms1 is None or go_terms2 is None:
        print("Could not get GO Terms for one or both IDs")
        return
  
    compare_go_terms(proteinone,proteintwo,go_terms1,go_terms2)


@main.command(short_help='Obtains Go Terms and their details from a Uniprot ID code or a list of them.')
@click.argument('namefield', required=True)
def score_go(namefield):
    uniprot_ids_list = get_uniprotIds_from_field(namefield)    
    if(uniprot_ids_list == None):
        return

    try:
        go_terms = uniprotClient.getManyGoTerms(uniprot_ids_list)
        if go_terms is None:
            print("Could not get GO Terms for one or both IDs")
            return

        go_terms_enrichemt = get_go_terms_detail(go_terms)
        
        write_score_go(go_terms_enrichemt)
    except InvalidRequestException as e:
        e.printMe()
        return
    except Exception as e:
        print(f"Error: An error occurred while processing the file {namefield}: {e}")
        return 
    

def get_uniprotIds_from_field(name_field):

    blastClient = BlastClient()
    try:
        uniprot_ids_list = blastClient.save_ids(name_field)
    except Exception as e:
        print(e)
        print(f"An error occurred while processing the file {name_field}: {e}")
        return None
    else:
        return uniprot_ids_list


    
def getProteinFromUniprot(uniprotId,verbose):
    uniprotClient=UniprotClient()

    try:
        response = uniprotClient.getSequenceFromProtein(uniprotId)
        if verbose:
            print (response)
    except InvalidRequestException as e:
        e.printMe()
    except Exception:
        print ("OCURRIÓ UN ERROR INESPERADO")

@main.command(short_help='Returns an aminoacid sequence for a given protein.')
@click.argument('protein', required=True)
@click.option('-v', is_flag=True, default= False,help='Allow to view response sequence in command line.' )
def query_protein(protein,v):
    """Returns an aminoacid sequence for a given protein.
    
    [PROTEIN] is a Uniprot ID of a protein."""

    getProteinFromUniprot(protein,v)
    

class HelpfulCmd(click.Command):
    def format_help(self, ctx, formatter):
        click.echo("USAGE: main.py run-blast PROTEIN DATABASE OUTFILENAME [OPTIONS]")
        click.echo(blastClient.show_help())
        click.echo("-outfmt has been set to a json format")


@main.command(short_help="Run a blast protein query.", 
              cls=HelpfulCmd,
              context_settings=dict(
                ignore_unknown_options=True,
                allow_extra_args=True,
))
@click.argument('protein', required= True)
@click.argument('database',required= True)
@click.argument('outfile',required= True)
def run_blast(protein, database, outfile):

    args = sys.argv[5:]

    if ("-outfmt" in args):

        outIndex = args.index("-outfmt")
        args.pop(outIndex)
        args.pop(outIndex)

    if ("-out" in args):

        outIndex = args.index("-out")
        args.pop(outIndex)
        args.pop(outIndex) 

    if not "-remote" in args and not blastClient.db_exists(database):
        dbfile = input("Database not found, insert database file inside blast/database directory:")
        db_args = list(dbfile.split(" "))

        try:
            blastClient.add_database(db_args[0], database, db_args[1:])
        except Exception as e:
            print(e)
            return

    try:
        blastClient.run_query(protein, database, outfile, args)
    except Exception as e:
        print(e)
    


@main.command(short_help='Download Uniprot/Swissprot or Uniprot/Trembl databases.')
@click.option('--swissprot', is_flag=True, default= False )
@click.option('--trembl', is_flag=True, default= False )
def get_database(swissprot, trembl):
    """Add swissprot or trembl databases to locally working databases.
    """


    if (swissprot and not blastClient.db_exists('swissprot')):
        blastClient.download_database('swissprot')

    if (trembl and not blastClient.db_exists('trembl')):
        blastClient.download_database('trembl')

def readFile(filename):
    try:
        file = open(filename, "r") 
        lines= file.read().splitlines()
        file.close() 
        return lines
    except FileNotFoundError:
        print ("The file {0} can not be reached. Check filename and path.".format(filename))

@main.command(short_help='Reads all Uniprot ID from a given file and get its aminoacids sequence.')
@click.argument('filename', required=True)
def read_file(filename):
    """Reads all Uniprot ID from a given file and get its aminoacids sequence.
    
    [FILENAME] is a simple flat text file with any extension you like.
    Just put each Uniprot ID per row and it will be readed.
    """

    uniprotCodes =readFile(filename)
    if uniprotCodes!=None:

        for eachUniprotCode in uniprotCodes:
            try:
                getProteinFromUniprot(eachUniprotCode)
            except InvalidRequestException as e:
                e.printMe()
            

    
@main.command(short_help='Shows a hierarchy graph comparing of 2 GO Terms')
@click.argument('goTermA', required=True)
@click.argument('goTermB', required=True)
@click.option('--children', is_flag=True, default= False,help="Show all children relationships" )
@click.option('--relationships', is_flag=True, default= False, help="Show all ancestors relationships (part_of, regulates, positively regulates, negatively regulates)")
def plotGoTerms(goterma,gotermb,children,relationships):
    """Shows a hierarchy graph comparing of 2 GO Terms.
    
    [GOTERMA] is a first GO Term to be compared.

    [GOTERMB] is a second GO Term to be compared."""
    plotGOTComparison(goterma,gotermb,children,relationships)
    im = Image.open("downloads/comparison.png")
    im.show()
    

if __name__ == '__main__':
    main()