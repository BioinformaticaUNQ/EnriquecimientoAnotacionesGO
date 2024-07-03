import subprocess
import os
import urllib.request
import gzip
import shutil
import json
from pathlib import Path

class BlastClient():

    def __init__(self): 
        self.path = Path(os.path.abspath(__file__))
        self.blast_path = os.path.join(self.path.parent, "ncbi-blast-2.15.0+/bin")
    

    def print_output(self, subprocess):
        while True:
            line = subprocess.stdout.readline().decode('UTF-8')
            if not line:
                break
            print (line.rstrip())


    def db_exists(self, database):
        command_path = os.path.join(self.blast_path , "blastdbcmd")
        db_path = os.path.join(self.path.parent, "db", database)

        args = (command_path, "-db", db_path, "-info")
        popen = subprocess.Popen(args, stdout=subprocess.DEVNULL )
        popen.wait()
        popen.kill()
        # output = popen.stdout.read()
        #src/integraciones/ncbi-blast-2.15.0+/bin/blastdbcmd
        return not popen.returncode == 2



    def add_database(self, filename, database):
        print(self.blast_path)

        command_path = os.path.join(self.blast_path, "makeblastdb")
        db_path = os.path.join(self.path.parent, "db", database)

        args = (command_path, "-in", filename, "-parse_seqids",
                "-dbtype", "prot", "-out", db_path)
        
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()
        self.print_output(popen)
        popen.kill()



    def run_query(self, protein, database, blast_args):
        command_path = os.path.join(self.blast_path, "blastp")
        
        if ("-remote" in blast_args):
            db_path = database
        else:
            db_path = os.path.join(self.path.parent, "db", database)
        protein_path = os.path.join(self.path.parent, "proteins", protein + ".fasta")

        args = (command_path, "-db", db_path,
                "-query", protein_path, "-outfmt", "15")
        
        for arg in blast_args:
            args = args + (arg,)

        popen = subprocess.Popen(args, stdout=subprocess.PIPE )
        popen.wait()
        self.print_output(popen)
        popen.kill()


    def show_help(self ):
        command_path = os.path.join(self.blast_path, "blastp")

        args = (command_path, "-help")
        popen = subprocess.Popen(args, stdout=subprocess.PIPE, cwd="./")
        popen.wait()
        self.print_output(popen)
        popen.kill()


    def download_database(self, database):

        if (database == "swissprot"):
            urllib.request.urlretrieve("https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz", database + ".gz")

        else:
            urllib.request.urlretrieve("https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.fasta.gz", database + ".gz")

        with gzip.open(database + '.gz', 'rb') as f_in:
            with open (database + ".fasta", "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        f_in.close()
        f_out.close()
        self.add_database(database + ".fasta", database)
        os.remove(database + ".gz")
        os.remove(database + ".fasta")


    def save_ids(self, file_path):

        with open(file_path) as file:
            prots = json.load(file)

        file.close()
        matchs = prots['BlastOutput2'][0]["report"]["results"]["search"]["hits"]

        # for match in matchs:
        #      print(match["description"][0]["accession"])#["description"]["accession"])

        ids = [match["description"][0]["accession"] for match in matchs]
        print(ids)
        return (ids)



    # command_path, "-db", "src/integraciones/db/" + database,
    #             "-query", "src/integraciones/proteins/" + protein + ".fasta", "-out", "results.out")

blastClient = BlastClient()
blastClient.save_ids("/home/luqui/EnriquecimientoAnotacionesGO/src/resul.json")