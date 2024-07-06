import os
from goatools.base import download_go_basic_obo
from goatools.cli.gosubdag_plot import PlotCli

#Lee el archivo .obo y retorna una lista de términos.
def read_field(file_path):
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist. We proceed to download it.")
        download_go_term_field()
    
    with open(file_path, 'r') as file:
        contenido = file.read()
        
    terminos = contenido.split("\n\n")
    terminos_dict = []

    for termino in terminos:
        if termino.startswith("[Term]"):
            term_dict = {}
            lineas = termino.split("\n")
            for linea in lineas:
                if linea:
                    clave_valor = linea.split(": ", 1)
                    if len(clave_valor) == 2:
                        clave, valor = clave_valor
                        term_dict[clave] = valor
            terminos_dict.append(term_dict)
    
    return terminos_dict

def get_name_namespace_by_id(terminos,result,go_id):
    for termino in terminos:
        if termino.get('id') == go_id:
            result.append({
                'id': go_id,
                'name': termino.get('name'),
                'namespace': termino.get('namespace')
            })
            break

# Obtiene los valores de name y namespace a partir de una lista de ids de go-terms dado en el archivo .obo.
def get_name_namespace_from_field(terminos,go_ids):
    resultado = []
    
    for go_id in go_ids:
        get_name_namespace_by_id(terminos,resultado,go_id)
    
    return resultado


# Función para descargar el archivo necesario para el enriquecimiento
def download_go_term_field():
    # Ruta completa del archivo de destino
    destino = os.path.join("downloads", "go-basic.obo")

    # Verificar si el archivo existe y borrarlo si es así
    if os.path.exists(destino):
        os.remove(destino)
        print(f"Existing file {destino} deleted.")

    # Descargar el archivo
    download_go_basic_obo(obo=destino)

    print(f"File downloaded and saved in {destino}")


def show_go_terms(go_terms):

    if(not go_terms):
        print("There are no values")
    else:
        for go_term in go_terms:
            print(f"ID: {go_term['id']}\nName: {go_term['name']}\nNamespace: {go_term['namespace']}\n")
    print("-------------------- ***** * ***** --------------------")

# Función para comparar términos GO mediante codigos de uniprot
def compare_go_terms(uniprot_id1,uniprot_id2,go_terms1, go_terms2):
    terminos = read_field("downloads/go-basic.obo")

    set1 = set(go_terms1)
    set2 = set(go_terms2)
    common = set1.intersection(set2)
    unique1 = set1 - set2
    unique2 = set2 - set1

     
    go_common_enrichment = get_name_namespace_from_field(terminos,common)
    print("Common GO terms: \n")
    show_go_terms(go_common_enrichment)

    go_terms1_enrichment = get_name_namespace_from_field(terminos,unique1)
    print(f"Unique GO terms for {uniprot_id1}: \n")
    show_go_terms(go_terms1_enrichment)

    go_terms2_enrichment = get_name_namespace_from_field(terminos,unique2)
    print(f"Unique GO terms for{uniprot_id2}: \n")
    show_go_terms(go_terms2_enrichment)


def plotGOTComparison(goTermA,goTermB):
    obj={'GO': [goTermA,goTermB], 'obo': 'downloads/go-basic.obo', 'outfile': 'downloads/comparison.png', 'rankdir': 'TB'}
    PlotCli().cli(obj)
    
def get_go_terms_detail(go_terms_uniprots_list):
    terminos = read_field("downloads/go-basic.obo")

    result = []
    for res in go_terms_uniprots_list:
        uniProt_id =  res['UniProtId']
        go_terms_ids = res['GoTerms']
        go_term_fields = []
        for go_term_id in go_terms_ids:
            get_name_namespace_by_id(terminos,go_term_fields,go_term_id)
            
        result.append({
            'UniProtId':uniProt_id,
            'GoTerms': go_term_fields
        })
    return result

        






