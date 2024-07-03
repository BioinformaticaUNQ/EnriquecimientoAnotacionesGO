import requests
import json
import shutil

class InvalidRequestQuickGoException(Exception):
    "An error has ocurred on the request. Please check Quick Go Id"
    pass

    def printMe():
        print ("An error has ocurred on the request. Please check Quick Go Id")

class QuickGoClient:
    def __init__(self):
        self.headers={"Accept":"application/json"}       
        self.url="https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/"   


    def getChartById(self,goTermId):

        response = requests.get(self.url+goTermId+"/chart",stream=True)
        if response.status_code!=200:
                raise InvalidRequestQuickGoException
        if response.status_code==200:
            fileName=goTermId.replace(":","") +'.png'
            with open(fileName, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
        return (fileName + " chart downloaded!")
          
     

    