import subprocess


def check_db(database):
    args = ("integraciones/ncbi-blast-2.15.0+/bin/blastdbcmd", "-db", database, "-info")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE, cwd="./")
    popen.wait()
    # output = popen.stdout.read()
    return popen.returncode

def add_database(filename, database):
    args = ("src/integraciones/ncbi-blast-2.15.0+/bin/makeblastdb", "-in", filename,
            "-dbtype", "prot", "-out", "src/integraciones/db/" + database)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE, cwd="../")
    popen.wait()
    output = popen.stdout.read()
    print(output)

def run_query(protein, database):
    args = ("src/integraciones/ncbi-blast-2.15.0+/bin/blastp", "-db", "src/integraciones/db/" + database,
            "-query", "src/integraciones/proteins/" + protein + ".fasta", "-out", "results.out")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE, cwd="../")
    popen.wait()
    output = popen.stdout.read()
    print (output)

