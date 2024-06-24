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
        references=self.getProteinDetailByKey(uniprotId,'uniProtKBCrossReferences')
        return self.getGoTermsResultMap(references,True)
    
    ## Devuelvo los GoTerms en una lista, si fullValue es true termino retornando el value y su GoEvidence
    def getGoTermsResultMap(self,references,fullValue):
        result = []
        for x in references:
            if x['database']=="GO":
                if(fullValue):
                    goTerm=""
                    goEvidence=""
                    for y in x['properties']:
                        print('properties:', y)
                        if y['key']=="GoTerm":
                            goTerm=y['value']
                        if y['key']=="GoEvidenceType":
                            goEvidence=y['value']

                    result.append([x['id'],goTerm])##TODO: falta agregar el goEvidence, como deberiamos manejarlo?
                else:
                    result.append(x['id'])
        return result

    ## devuelvo solo los ids de los GOTerms en una lista.                
    def getGoTerms(self,uniprotId):
        references=self.getProteinDetailByKey(uniprotId,'uniProtKBCrossReferences')
        return self.getGoTermsResultMap(references,False)
    


    