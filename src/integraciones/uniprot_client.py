import requests
class UniprotClient:
    def __init__(self):
        #first time example
        self.uniprotId="9606"
        self.url= "https://rest.uniprot.org/uniprotkb/search?query=reviewed:true+AND+"
        self.url= self.url + "organism_id:"+self.uniprotId
        self.url= self.url + "&format=fasta"
        
    def getProtein(self):
        return requests.get(self.url)
