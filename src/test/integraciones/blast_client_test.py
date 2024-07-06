import sys

from ...integraciones.uniprot_client import UniprotClient

uniprotClient=UniprotClient()

print(uniprotClient.getSequenceFromProtein("P00533"))