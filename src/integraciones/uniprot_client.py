import requests
import json
from pathlib import Path
import os
from concurrent.futures import ThreadPoolExecutor, as_completed


class InvalidRequestException(Exception):
    def __init__(self, message="An error occurred in the query. Please check the Uniprot ID"):
        super().__init__(message)
        self.message = message
    

    def printMe(self):
        print(f"Error: {self.message}")
    
    
class UniprotClient:
    def __init__(self):
        self.headers={"Accept":"application/json"}       
        self.url="https://rest.uniprot.org/uniprotkb/"
        self.path = Path(os.path.abspath(__file__))

    def saveProteinFasta(self, filename, protein):

        newpath = os.path.join( self.path.parent, "blast/proteins" )
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        with open(newpath + "/" + filename + ".fasta", "w") as file:
            file.write("> " + filename + "\n" + protein)
        


    # Dividimos una lista segun un n en particular
    def chunk_list(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    # Dada una lista de codigos uniprots, hacemos la peticion para todos esos codigos.
    def getManyProteinDetail(self,listUniproId):
        uniprot_ids_str = ""
        total = len(listUniproId)
        count = 0
        for uniprotId in listUniproId:
            count+= 1
            query = None
            if(count == total):
                query = f"accession:{uniprotId}"
            else:
                query = f"accession:{uniprotId}+OR+"
            uniprot_ids_str = uniprot_ids_str + query

        url = f"https://rest.uniprot.org/uniprotkb/search?query={uniprot_ids_str}&format=json"
        response=  requests.get(url,headers=self.headers)

        if response.status_code!=200:
            raise InvalidRequestException
        return  json.loads(response.content)
    
    def getProteinDetail(self,uniprotId):
        #Dada una uniprot ID retorna una proteina en detalle 
        response=  requests.get(self.url+uniprotId,headers=self.headers)
        if response.status_code!=200:
                raise InvalidRequestException()
        return json.loads(response.content)
    
        
    def getSequenceFromProtein(self, uniprotId):
        #Dada una Uniprot ID retorna una secuencia 
        response=  self.getProteinDetail(uniprotId)
        self.saveProteinFasta(uniprotId, response['sequence']['value'])
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
    
    # Devuelvo los terminos GO para una lista de codigos Uniprots
    def getManyGoTerms(self, uniprotIds):
        result = []

        try:
            proteinsDetails = self.getManyProteinDetail(uniprotIds)['results']
        except InvalidRequestException as ex:
            raise
        for protein in proteinsDetails:
            references = protein['uniProtKBCrossReferences']
            resProt = {
                "UniProtId": protein['primaryAccession'],
                "GoTerms": self.getGoTermsResultMap(references,False)

            }
            result.append(resProt)
        return result

    


    