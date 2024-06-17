from integraciones.uniprot_client import *

def main():
    uniprotClient=UniprotClient()
    response = uniprotClient.getProtein()
    print (response.content)


if __name__ == '__main__':
    main()