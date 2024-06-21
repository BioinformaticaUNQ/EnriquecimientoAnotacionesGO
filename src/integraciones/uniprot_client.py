import requests
import json
class UniprotClient:
    def __init__(self):
        #Set all types of headers for uniprot
        self.headers={"Accept":"application/json"}
        
        
        self.url="https://rest.uniprot.org/uniprotkb/"

        
        
        
    def getSequenceFromProtein(self, uniprotId):

        response=  requests.get(self.url+uniprotId,headers=self.headers)
        data = json.loads(response.content)

        return data['sequence']['value']

    def getProteinDetail(self,uniprotId):
        response=  requests.get(self.url+uniprotId,headers=self.headers)
        return json.loads(response.content)
    
    def getProteinDetailByKey(self,uniprotId,key):
        return self.getProteinDetail(uniprotId)[key]
    
    def getCrossReferences(self,uniprotId):
        goNotations =[]
        references=self.getProteinDetailByKey(uniprotId,'uniProtKBCrossReferences')
        for x in references:
            if x['database']=="GO":
                goTerm=""
                goEvidence=""
                for y in x['properties']:
                    if y['key']=="GoTerm":
                        goTerm=y['value']
                    if y['key']=="GoEvidenceType":
                        goEvidence=y['value']
                    
                goNotations.append([x['id'],goTerm,goEvidence])

        return (goNotations)
    

    