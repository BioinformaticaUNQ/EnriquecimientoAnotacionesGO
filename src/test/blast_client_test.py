import unittest
from context import blast_client, uniprot_client
import os, glob
import shutil

BlastClient = blast_client.BlastClient
UniprotClient = uniprot_client.UniprotClient

pathDatabase = os.path.abspath(os.path.join(os.path.dirname(__file__), "CytochromeC.fasta"))
pathDBs = os.path.abspath(os.path.join(os.path.dirname(__file__), "../integraciones/blast/database"))

class TestBlastClient(unittest.TestCase):

    def setUp(self):
        blastClient = BlastClient()

        shutil.copyfile(pathDatabase, pathDBs + "/CytochromeC.fasta")
        blastClient.add_database("CytochromeC.fasta", "CytochromeC", ())
        

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

        filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "NewSpecies.fasta"))

        shutil.copyfile(filePath, pathDBs + "/NewSpecies.fasta")

        blastClient.add_database("NewSpecies.fasta", "NewSpecies", ())

        DBFiles = glob.glob(os.path.abspath(os.path.join(os.path.dirname(__file__), "../integraciones/blast/database/NewSpecies*")))

        self.assertEqual(len(DBFiles), 9)

    def test_download_swissprot_db(self):
        blastClient = BlastClient()

        blastClient.download_database("swissprot")

        DBFiles = glob.glob(os.path.abspath(os.path.join(os.path.dirname(__file__), "../integraciones/blast/database/swissprot*")))

        self.assertEqual(len(DBFiles), 10)        

    def test_run_query(self):
        uniprotClient = UniprotClient()

        blastClient = BlastClient()

        uniprotClient.getSequenceFromProtein("P00401")

        args = ["-out", "test.json"]

        blastClient.run_query("P00401", "CytochromeC", args)

        pathProtein = os.path.abspath(os.path.join(os.path.dirname(__file__), "../integraciones/blast/results/test.json"))


        self.assertTrue(os.path.isfile(pathProtein))

        os.remove(pathProtein)



    def tearDown(self):
        for filename in glob.glob(os.path.abspath(os.path.join(os.path.dirname(__file__), "../integraciones/blast/database/CytochromeC*"))):
             os.remove(filename) 

        for filename in glob.glob(os.path.abspath(os.path.join(os.path.dirname(__file__), "../integraciones/blast/database/NewSpecies*"))):
             os.remove(filename) 

        for filename in glob.glob(os.path.abspath(os.path.join(os.path.dirname(__file__), "../integraciones/blast/database/swissprot*"))):
             os.remove(filename) 

     

if __name__ == '__main__':
    unittest.main()