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
        self.db_path= os.path.join(self.path.parent, "blast/database")
        self.proteins_path= os.path.join(self.path.parent, "blast/proteins")
        self.results_path= os.path.join(self.path.parent, "blast/results")
        # self.blast_path = os.path.join(self.path.parent, "ncbi-blast-2.15.0+/bin")
    

    def print_output(self, subprocess):
        while True:
            line = subprocess.stdout.readline().decode('UTF-8')
            if not line:
                break
            print (line.rstrip())


    def db_exists(self, database):
        # command_path = os.path.join(self.blast_path , "blastdbcmd")
        # db_path = os.path.join(self.path.parent, "db", database)

        # args = (command_path, "-db", db_path, "-info")
        # popen = subprocess.Popen(args, stdout=subprocess.DEVNULL )
        # popen.wait()
        # popen.kill()
        # # output = popen.stdout.read()
        # return not popen.returncode == 2

        command = f'docker run --rm \
                -v {self.db_path}:/blast/blastdb_custom:rw \
                -w /blast/blastdb_custom \
                ncbi/blast \
                blastdbcmd -db /blast/blastdb_custom/{database} -info'

        try:

            proc = subprocess.run(command, shell=True, check=True, capture_output=True)
        
        except subprocess.CalledProcessError:

            return False
        
        return True



    def add_database(self, filename, database, blast_args):

        # command_path = os.path.join(self.blast_path, "makeblastdb")
        # db_path = os.path.join(self.path.parent, "db", database)

        # args = (command_path, "-in", filename, "-parse_seqids",
        #         "-dbtype", "prot", "-out", db_path)
        
        # popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        # popen.wait()
        # self.print_output(popen)
        # popen.kill()

        

        command = f'docker run --rm \
                -v {self.db_path}:/blast/blastdb_custom:rw \
                -w /blast/blastdb_custom \
                ncbi/blast \
                makeblastdb -in /blast/blastdb_custom/{filename} -dbtype prot \
                -out {database}'
        
        for arg in blast_args: 
            command += " " + arg

        subprocess.run(command, shell=True, check=True)



    def run_query(self, protein, database, blast_args):
        # command_path = os.path.join(self.blast_path, "blastp")
        
        # if ("-remote" in blast_args):
        #     db_path = database
        # else:
        #     db_path = os.path.join(self.path.parent, "db", database)

        # protein_path = os.path.join(self.path.parent, "proteins", protein + ".fasta")

        # args = (command_path, "-db", db_path,
        #         "-query", protein_path, "-outfmt", "15")

        # if not os.path.isdir( self.results_path):
        #     os.mkdir(self.results_path)

 
        # if "-out" in blast_args:
        #     index = blast_args.index("-out")
        #     blast_args[index + 1] =  os.path.join (self.results_path, blast_args[index + 1] )

        # for arg in blast_args:
        #     args = args + (arg,)

        # print(args)

        # popen = subprocess.Popen(args, stdout=subprocess.PIPE )
        # popen.wait()
        # self.print_output(popen)
        # popen.kill()

        if not os.path.isdir( self.results_path): 
            os.mkdir(self.results_path)

        # if ("-remote" in blast_args):
        #     db = database
        # else:
        #     db = f"blast/blastdb_custom/{database}"

        if "-out" in blast_args:
            index = blast_args.index("-out")
            blast_args[index + 1] =  os.path.join ('/blast/results', blast_args[index + 1] )

        command = f'docker run --rm \
                -v {self.db_path}:/blast/blastdb_custom:rw \
                -v {self.proteins_path}:/blast/queries:rw \
                -v {self.results_path}:/blast/results:rw \
                ncbi/blast \
                blastp -query /blast/queries/{protein}.fasta \
                -db {database} -outfmt 15'
        
        for arg in blast_args:
            command += f" {arg}"

        subprocess.run(command, shell=True, check=True)
                 


    def show_help(self ):
        # command_path = os.path.join(self.blast_path, "blastp")

        # args = (command_path, "-help")
        # popen = subprocess.Popen(args, stdout=subprocess.PIPE, cwd="./")
        # popen.wait()
        # self.print_output(popen)
        # popen.kill()

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


blastClient = BlastClient()
