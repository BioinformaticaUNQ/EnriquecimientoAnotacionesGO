from integraciones.uniprot_client import *
import click

@click.group()
def main():
    pass

@main.command()
@click.argument('protein', required=True)
def query_protein(protein):
    uniprotClient=UniprotClient()
    #default test protein

    response = uniprotClient.getSequenceFromProtein(protein)
    
    print (response)
    

if __name__ == '__main__':
    main()