from goatools.base import download_go_basic_obo
from goatools.obo_parser import GODag
from goatools.goea.go_enrichment_ns import GOEnrichmentStudy
from goatools.anno.gaf_reader import GafReader

# Función para comparar términos GO mediante codigos de uniprot
def compare_go_terms(uniprot_id1,uniprot_id2,go_terms1, go_terms2):
    ##TODO: queda investigar y consultar sobre el enriquecimiento de los GOterms
    
    set1 = set(go_terms1)
    set2 = set(go_terms2)
    common = set1.intersection(set2)
    unique1 = set1 - set2
    unique2 = set2 - set1

    print(f"Términos GO comunes: {common}")
    print(f"Términos GO únicos para {uniprot_id1}: {unique1}")
    print(f"Términos GO únicos para {uniprot_id2}: {unique2}")
