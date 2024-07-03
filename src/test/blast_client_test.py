import unittest
from context import blast_client
import os, glob

BlastClient = blast_client.BlastClient

pathDabase = os.path.abspath(os.path.join(os.path.dirname(__file__), "CytochromeC.fasta"))

class TestBlastClient(unittest.TestCase):

    def setUp(self):
        blastClient = BlastClient()

        blastClient.add_database(pathDabase, "CytochromeC")
        


    def test_database_does_not_exists(self):
        blastClient = BlastClient()

        result = blastClient.db_exists("database")

        self.assertFalse(result)


    def test_database_does_exists(self):
        blastClient = BlastClient()

        result = blastClient.db_exists("CytochromeC")

        self.assertTrue(result)


    def test_create_database(self):
        blastClient = BlastClient()

        newDB = os.path.abspath(os.path.join(os.path.dirname(__file__), "NewSpecies.fasta"))

        blastClient.add_database(newDB, "NewSpecies")

        DBFiles = glob.glob(os.path.abspath(os.path.join(os.path.dirname(__file__), "../integraciones/db/NewSpecies*")))

        self.assertEqual(len(DBFiles), 10)

    def tearDown(self):
        for filename in glob.glob(os.path.abspath(os.path.join(os.path.dirname(__file__), "../integraciones/db/CytochromeC*"))):
             os.remove(filename) 

        for filename in glob.glob(os.path.abspath(os.path.join(os.path.dirname(__file__), "../integraciones/db/NewSpecies*"))):
             os.remove(filename) 
     

if __name__ == '__main__':
    unittest.main()