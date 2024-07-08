# Final practical work: GO annotation enrichment
CLI that allows comparison and enrichment of homologous proteins

## Members:

* Enrique Alonso.
* Lucas Alvarez.
* Gaston Da Silva.

## Facility

### Prerequisites

<<<<<<< HEAD
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
  
### Docker run command options
*This section is optional.*    
  
Below is a list of `docker run` command line [options](https://docs.docker.com/engine/reference/commandline/run/) used in this tutorial.

| Name, short-hand(if available) | Description |
| :----------------------------  | :---------- |
|`--rm`|Automatically remove the container when it exits|
|`--volume` , `-v`|Bind mount a volume|
|`--workdir` , `-w`| Working directory inside the container|


### Step 2. Set virtual enviroment

=======
>>>>>>> 9fdb3c5b7d38a04a7bf1c86d41dfce3c888732b1
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

<<<<<<< HEAD
## run-blast

Executes a blast query run and returns the results of that run.
```bash
run-blast [protein] [dataBase] [outfile name] {blastp args}
=======
Executes a blast run and returns the results of that run.
```bash
run-blast [protein] [dataBase] 
>>>>>>> 9fdb3c5b7d38a04a7bf1c86d41dfce3c888732b1
```

Returns the go terms for a protein.
```bash
get-goterms[uniprotCode]
```


## compare-goterms
Gets and compares the GoTerms given by parameter.
```bash
compare-goterms [uniprotCode1] [uniprotCode2]
<<<<<<< HEAD
=======
```

### Ejemplo:
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
>>>>>>> 9fdb3c5b7d38a04a7bf1c86d41dfce3c888732b1
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