import requests
import json

class InvalidRequestException(Exception):
    "Ocurrió un error en la consulta. Verifique el código Uniprot"
    pass

    def printMe():
        print ("Ocurrió un error en la consulta. Verifique el código Uniprot")

class UniprotClient:
    def __init__(self):
        self.headers={"Accept":"application/json"}       
        self.url="https://rest.uniprot.org/uniprotkb/"   
        

    def getProteinDetail(self,uniprotId):
        #Dada una uniprot ID retorna una proteina en detalle 
        response=  requests.get(self.url+uniprotId,headers=self.headers)
        if response.status_code!=200:
                raise InvalidRequestException
        return json.loads(response.content)
    
        
    def getSequenceFromProtein(self, uniprotId):
        #Dada una Uniprot ID retorna una secuencia 
        
        response=  self.getProteinDetail(uniprotId)
        return response['sequence']['value']
        
    
    def getProteinDetailByKey(self,uniprotId,key):
        #Dada una uniprot id y una clave retorna solo el valor de la clave
        return self.getProteinDetail(uniprotId)[key]
    
    def getCrossReferences(self,uniprotId):
        goNotations =[]
        references=self.getProteinDetailByKey(uniprotId,'uniProtKBCrossReferences')
        for x in references:
            if x['database']=="GO":
                goTerm=""
                goEvidence=""
                for y in x['properties']:
                    if y.key=="GoTerm":
                        goTerm=y.value
                    if y.key=="GoEvidenceType":
                        goEvidence=y.value
                    
                goNotations.append([x['id'],goTe])

        return (goNotations)
    


    