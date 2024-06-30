import subprocess
import os
import urllib.request
import gzip
import shutil


current_path = os.getcwd()
blast_path = os.path.join(current_path, "integraciones/ncbi-blast-2.15.0+/bin")

def print_output(subprocess):
    while True:
        line = subprocess.stdout.readline().decode('UTF-8')
        if not line:
            break
        print (line.rstrip())


def check_db(database):
    command_path = os.path.join(blast_path, "blastdbcmd")
    db_path = os.path.join(current_path, "integraciones/db", database)

    args = (command_path, "-db", db_path, "-info")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE )
    popen.wait()
    # output = popen.stdout.read()
    return popen.returncode



def add_database(filename, database):
    command_path = os.path.join(blast_path, "makeblastdb")
    db_path = os.path.join(current_path, "integraciones/db", database)

    args = (command_path, "-in", filename,
            "-dbtype", "prot", "-out", db_path)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    print_output(popen)



def run_query(protein, database, blast_args):
    command_path = os.path.join(blast_path, "blastp")
    
    if ("-remote" in blast_args):
        db_path = database
    else:
        db_path = os.path.join(current_path, "integraciones/db", database)
    protein_path = os.path.join(current_path, "integraciones/proteins", protein + ".fasta")

    args = (command_path, "-db", db_path,
            "-query", protein_path, "-outfmt", "0")
    
    for arg in blast_args:
        args = args + (arg,)

    popen = subprocess.Popen(args, stdout=subprocess.PIPE )
    popen.wait()
    print_output(popen)


def show_help():
    command_path = os.path.join(blast_path, "blastp")

    args = (command_path, "-help")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE, cwd="./")
    popen.wait()
    print_output(popen)


def download_database(database):

    if (database == "swissprot"):
        urllib.request.urlretrieve("https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz", database + ".gz")

    else:
        urllib.request.urlretrieve("https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.fasta.gz", database + ".gz")

    with gzip.open(database + '.gz', 'rb') as f_in:
        with open (database + ".fasta", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    add_database(database + ".fasta", database)
    os.remove(database + ".gz")
    os.remove(database + ".fasta")


# command_path, "-db", "src/integraciones/db/" + database,
#             "-query", "src/integraciones/proteins/" + protein + ".fasta", "-out", "results.out")