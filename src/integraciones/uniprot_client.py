import requests
import json
class UniprotClient:
    def __init__(self):
        #Set all types of headers for uniprot
        self.headers={"Accept":"application/json"}
        
        
        self.url="https://rest.uniprot.org/uniprotkb/"

        
        
        
    def getSequenceFromProtein(self, protein):

        response=  requests.get(self.url+protein,headers=self.headers)
        data = json.loads(response.content)

        return data['sequence']['value']
