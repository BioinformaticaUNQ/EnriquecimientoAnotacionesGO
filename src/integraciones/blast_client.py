import subprocess
import os
import urllib.request
import gzip
import shutil
import json
from pathlib import Path


class FileNotFoundException(Exception):
    pass

class BlastQueryException(Exception):
    pass

class BlastClient():

    def __init__(self): 
        self.path = Path(os.path.abspath(__file__))
        self.db_path= os.path.join(self.path.parent, "blast","database")
        self.proteins_path= os.path.join(self.path.parent, "blast","proteins")
        self.results_path= os.path.join(self.path.parent, "blast","results")
    

    def print_output(self, subprocess):
        while True:
            line = subprocess.stdout.readline().decode('UTF-8')
            if not line:
                break
            print (line.rstrip())


    def db_exists(self, database):

        command = f'docker run --rm \
                -v {self.db_path}:/blast/blastdb_custom:rw \
                -w /blast/blastdb_custom \
                ncbi/blast \
                blastdbcmd -db /blast/blastdb_custom/{database} -info'


        
        try:
            proc = subprocess.run(command, shell=True, check=True, capture_output=True)
        
        except subprocess.CalledProcessError:

            return False
        else:
            return True



    def add_database(self, filename, database, blast_args):

        if not os.path.isfile(os.path.join(self.db_path, filename)):
            raise FileNotFoundException("Database file not found")
        

        command = f'docker run --rm \
                -v {self.db_path}:/blast/blastdb_custom:rw \
                -w /blast/blastdb_custom \
                ncbi/blast \
                makeblastdb -in /blast/blastdb_custom/{filename} -dbtype prot \
                -out {database}'
        
        for arg in blast_args: 
            command += " " + arg

        subprocess.run(command, shell=True, check=True)



    def run_query(self, protein, database, outfile, blast_args):
        
        if not os.path.isfile(os.path.join(self.proteins_path, protein + ".fasta")):
            raise FileNotFoundException("Protein not found in files. Run query-protein")

        if not os.path.isdir( self.results_path): 
            os.mkdir(self.results_path)

        result = os.path.join (self.results_path, outfile + ".json")
        outfile = os.path.join ('/blast/results/' +  outfile + ".json" )

        command = f'docker run --rm \
                -v {self.db_path}:/blast/blastdb_custom:rw \
                -v {self.proteins_path}:/blast/queries:rw \
                -v {self.results_path}:/blast/results:rw \
                ncbi/blast \
                blastp -query /blast/queries/{protein}.fasta \
                -db {database} -outfmt 15 -out {outfile}'
        
        for arg in blast_args:
            command += f" {arg}"

        try:
            subprocess.run(command, shell=True, check=True)
        except Exception:
            raise BlastQueryException("BLAST blastp error in query run")
        else:
           self.produce_log(result)
           print(f"See results in {result}")
                 


    def show_help(self ):
        command = f'docker run --rm ncbi/blast blastp -help'

        subprocess.run(command, shell=True, check=True)


    def download_database(self, database):
        
        path = os.path.join(self.db_path, database)
        if (database == "swissprot"):
            urllib.request.urlretrieve("https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz",path + ".gz")

        else:
            urllib.request.urlretrieve("https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.fasta.gz",path + ".gz")

        with gzip.open(path + ".gz", 'rb') as f_in:
            with open (path + ".fasta", "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        f_in.close()
        f_out.close()
        self.add_database(database + ".fasta", database, ["-parse_seqids"])
        os.remove(path + ".gz")
        os.remove(path + ".fasta")
        print("Database succesfully downloaded")


    def save_ids(self, file_path):

        file_path = os.path.join(self.results_path, file_path)

        if not os.path.exists(file_path):
            raise FileNotFoundException(f"The file {file_path} does not exist in integraciones/blast/results.\nPlease check that the file exists, it also has to be in json format.\nIf it does not exist, please run the run_blast command and follow the steps indicated in the help.")
         
        else:

            with open(file_path) as file:
                prots = json.load(file)

            file.close()
            matchs = prots['BlastOutput2'][0]["report"]["results"]["search"]["hits"]

            ids = [match["description"][0]["accession"] for match in matchs]
            return (ids)


    def produce_log(self, results):
        
        with open(results) as file:
            blast = json.load(file)
        
        report = blast['BlastOutput2'][0]['report']

        file = open(os.path.join(self.path.parent, "blast", "blast.log"), "a+")
        
        file.write("====================================================================\n")
        file.write("Query: " + report["results"]["search"]["query_title"]+ "\n")
        file.write("Database: " + report['search_target']['db']+ "\n")
        file.write("Matrix: " + report["params"]["matrix"] + "\n")
        file.write("E-Value: " + str(report["params"]["expect"]) + "\n")
        file.write("Cost to open a gap: " + str(report["params"]["gap_open"]) + "\n")
        file.write("Cost to extend a gap: " + str(report["params"]["gap_extend"]) + "\n")
        file.write("Query length: " + str(report["results"]["search"]["query_len"])+ "\n")
        file.write("Matches: ")
        
        matchs = blast['BlastOutput2'][0]["report"]["results"]["search"]["hits"]

        for match in matchs:
            file.write("    Id: " + match["description"][0]['id'] + "\n")
            file.write("    Title: " + match["description"][0]['title'] + "\n")
            file.write("    Score: " + str(match["hsps"][0]['score']) + "\n")
            file.write("    Evalue: " + str(match["hsps"][0]['evalue'])+ "\n")
            identity = (match["hsps"][0]["identity"] / match["hsps"][0]["query_to"]) * 100
            file.write("    Identity: " + str(identity)+ "% \n")
            file.write("    Alignment:\n")
            file.write("        " + match["hsps"][0]['qseq'] + "\n")
            file.write("        " + match["hsps"][0]['midline'] + "\n")
            file.write("        " + match["hsps"][0]['hseq'] + "\n \n")


        total = report["results"]["search"]["stat"]["db_num"]
        file.write("Missed sequences: "+str({ total - len( matchs)}) + "\n")

