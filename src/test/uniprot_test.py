import unittest
import sys;
#sys.path.append(r'C:\\temp\\desa\\EnriquecimientoAnotacionesGO\\src')
from integraciones.uniprot_client import UniprotClient,InvalidRequestException
#sys.path.insert(0 , 'C:\\Users\\name\\desktop\\folder\\mod2')
# then import module
#import script2 as lib

class TestStringMethods(unittest.TestCase):

    def test_getProteinDetailAndObteinIt(self):
        #Dada una uniprot ID retorna una proteina en detalle 
        uniprotClient = UniprotClient()
        detail=uniprotClient.getProteinDetail("Q13651")
        sequence="MLPCLVVLLAALLSLRLGSDAHGTELPSPPSVWFEAEFFHHILHWTPIPNQSESTCYEVALLRYGIESWNSISNCSQTLSYDLTAVTLDLYHSNGYRARVRAVDGSRHSNWTVTNTRFSVDEVTLTVGSVNLEIHNGFILGKIQLPRPKMAPANDTYESIFSHFREYEIAIRKVPGNFTFTHKKVKHENFSLLTSGEVGEFCVQVKPSVASRSNKGMWSKEECISLTRQYFTVTNVIIFFAFVLLLSGALAYCLALQLYVRRRKKLPSVLLFKKPSPFIFISQRPSPETQDTIHPLDEEAFLKVSPELKNLDLHGSTDSGFGSTKPSLQTEEPQFLLPDPHPQADRTLGNREPPVLGDSCSSGSSNSTDSGICLQEPSLSPSTGPTWEQQVGSNSRGQDDSGIDLVQNSEGRAGDTQGGSALGHHSPPEPEVPGEEDPAAVAFQGYLRQTRCAEEKATKTGCLEEESPLTDGLGPKFGRCLVDEAGLHPPALAKGYLKQDPLEMTLASSGAPTGQWNQPTEEWSLLALSSCSDLGISDWSFAHDLAPLGCVAAPGGLLGSFNSDLVTLPLISSLQSSE"
        self.assertEqual(detail['sequence']['value'],sequence)

        
    def test_getProteinDetailAndItDoesNotExists(self):
        #Dada una uniprot ID erronea arrojo mensaje de error
        uniprotClient = UniprotClient()
        try:
            detail=uniprotClient.getProteinDetail("ALGO QUE NO EXISTE")
        except InvalidRequestException:
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)
        

    def test_getSequenceFromProteinIdAndIGetIt(self):
        #Dada una Uniprot ID retorna una secuencia 
        uniprotClient = UniprotClient()
        detail=uniprotClient.getSequenceFromProtein("Q13651")
        sequence="MLPCLVVLLAALLSLRLGSDAHGTELPSPPSVWFEAEFFHHILHWTPIPNQSESTCYEVALLRYGIESWNSISNCSQTLSYDLTAVTLDLYHSNGYRARVRAVDGSRHSNWTVTNTRFSVDEVTLTVGSVNLEIHNGFILGKIQLPRPKMAPANDTYESIFSHFREYEIAIRKVPGNFTFTHKKVKHENFSLLTSGEVGEFCVQVKPSVASRSNKGMWSKEECISLTRQYFTVTNVIIFFAFVLLLSGALAYCLALQLYVRRRKKLPSVLLFKKPSPFIFISQRPSPETQDTIHPLDEEAFLKVSPELKNLDLHGSTDSGFGSTKPSLQTEEPQFLLPDPHPQADRTLGNREPPVLGDSCSSGSSNSTDSGICLQEPSLSPSTGPTWEQQVGSNSRGQDDSGIDLVQNSEGRAGDTQGGSALGHHSPPEPEVPGEEDPAAVAFQGYLRQTRCAEEKATKTGCLEEESPLTDGLGPKFGRCLVDEAGLHPPALAKGYLKQDPLEMTLASSGAPTGQWNQPTEEWSLLALSSCSDLGISDWSFAHDLAPLGCVAAPGGLLGSFNSDLVTLPLISSLQSSE"
        self.assertEqual(detail,sequence)
        
    
    def test_getProteinDetailByKeyAndIGet(self):
        #Dada una uniprot id y una clave retorna solo el valor de la clave
        uniprotClient = UniprotClient()
        returnedValue=uniprotClient.getProteinDetailByKey("Q13651","uniProtkbId")
        expectedValue="I10R1_HUMAN"
        self.assertEqual(returnedValue,expectedValue)
        
    
    def test_getProteinGoRefsAndIGetIt(self):
        uniprotClient = UniprotClient()
        returnedValue=uniprotClient.getGoTerms("Q13651")
        expectedValue=['GO:0016324', 'GO:0005829', 'GO:0005886', 'GO:0019969', 'GO:0004920', 'GO:0038023', 'GO:0019221', 'GO:0060729', 'GO:0010507', 'GO:0050728', 'GO:0046427', 'GO:0050807', 'GO:0032496', 'GO:0070086']
        self.assertEqual(returnedValue,expectedValue)
        


    
    
if __name__ == '__main__':
    unittest.main()