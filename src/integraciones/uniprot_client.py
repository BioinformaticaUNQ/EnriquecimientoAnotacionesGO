import requests
class UniprotClient:
    def __init__(self):
        #first time example
        self.url="https://rest.uniprot.org/uniprotkb/search?query=reviewed:true+AND+organism_id:9606&format=fasta"
        
    def get(self):
        return requests.get(self.url)
