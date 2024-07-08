# Final practical work: GO annotation enrichment
CLI that allows comparison and enrichment of homologous proteins

## Members:

* Enrique Alonso.
* Lucas Alvarez.
* Gaston Da Silva.

## Facility

### Prerequisites


### Step 1. Install Docker
In a production system, Docker has to be installed as an application.  

```
## Run these commands to install Docker and add non-root users to run Docker
sudo snap install docker
sudo apt update
sudo apt install -y docker.io
sudo usermod -aG docker $USER
exit
# exit and SSH back in for changes to take effect
```
To confirm the correct installation of Docker, run the command `docker run hello-world`. If correctly installed, you should see "Hello from Docker!..."(https://docs.docker.com/samples/library/hello-world/)  

See docker [install](https://docs.docker.com/engine/install/) for another system options.
  


### Step 2. Set virtual enviroment
Make sure you have Python 3 installed on your system. You can check the installed Python version with the following command:

```sh
python3 --version
```
### Steps to follow

1. Clone the repository (or download the source code):
```bash
git clone https://github.com/BioinformaticaUNQ/EnriquecimientoAnotacionesGO.git
cd EnriquecimientoAnotacionesGO
```

2. Create a virtual environment:
   
```bash
python3 -m venv venv  
```

3. Activate the virtual environment:
```bash
source venv/bin/activate
```

4. Installs the dependencies configured in the requirements.txt file within the virtual environment.

```bash
pip install -r requeriments.txt
```


# Use

You can execute it with the following commands:

Returns an amino acid sequence for the requested protein.
```bash
query-protein [codigoUniprot]
```


## run-blast

Executes a blast query run and returns the results of that run. The results will shown in a .json file of the given name.
(-outfmt and -out blastp parameters had been set)
```bash
run-blast [protein] [dataBase] [outfile name] {blastp args}
```

If the database was not found, user will be ask to insert the name of a fasta file to create the database.
This file has to be inside the blast/database folder

```bash
Database not found, insert database file inside blast/database directory: Database.fasta
```

The parameter -remote can be added to perform the query in ncbi remote blast servers. In case of using this functionality swissprot is recommend to continue with the Go enrichment features.
```bash
run-blast P04439 swissprot result -remote -max_target_seqs 20
```

## download-query
Download the swissprot or trembl databases and add them to the working locally databases.
```bash
get-database -swissprot -trembl
```
If -swissprot is set the swissprot database will be downloaded. If-trembl is set the trembl database will be downloaded\
 
> :warning: **WARNING: The trembl database size is 52 GB**
## Get Go Terms

Returns the go terms for a protein.
```bash
get-goterms[uniprotCode]
```



## compare-goterms
Gets and compares the GoTerms given by parameter.
```bash
compare-goterms [uniprotCode1] [uniprotCode2]
```

### Example:
To compare the GO terms of UniProt codes P12345 and Q67890:
```bash
compare-goterms P12345 Q67890
```

## score-go
Generate a csv file with all the details of the Go-terms for each uniprot code.
The command requests to be sent the name of the file where the uniprots code information is located.
```bash
score-go [field_name]
```

### Ejemplo:
If you have a file called uniprot_codes.json with the UniProt codes, you can generate the CSV with the details of the GO terms using:
```bash
score-go uniprot_codes.json

### Example:
To compare the GO terms of UniProt codes P12345 and Q67890:
```bash
compare-goterms P12345 Q67890
```

## score-go
Generate a csv file with all the details of the Go-terms for each uniprot code.
The command requests to be sent the name of the file where the uniprots code information is located.
```bash
score-go [field_name]
```

### Ejemplo:
If you have a file called uniprot_codes.json with the UniProt codes, you can generate the CSV with the details of the GO terms using:
```bash

## Get Go Terms

Returns the go terms for a protein.
```bash
get-goterms[uniprotCode]
```



## Get an aminoacid sequence
Get an aminoacid sequence for a given protein.
```bash
query-protein [uniprotCode] [options]
```

Where options are:
* -v\tAllow to view response sequence in command line
* -f\tForce protein request even if have already downloaded

### Example:
To get protein related to uniprot id O95905:
```bash
query-protein O95905
```

## Read batch aminoacid's sequences from a file
You can read a massive quantity of Uniprot ID from a file and get each aminoacids sequence.
Use a plain text file with one Uniprot ID by row.
```bash
read-file [filename]
```

### Example:
To read each uniprot ID in file 
```bash
read-file /home/user/100proteins.txt