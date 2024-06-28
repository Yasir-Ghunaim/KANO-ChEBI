from rdflib import Graph, URIRef, RDF, RDFS, OWL, Namespace
import os 
import requests
from tqdm import tqdm 

CHEBI = Namespace("http://purl.obolibrary.org/obo/")
CHEBI_NS = Namespace("http://purl.obolibrary.org/obo/chebi/")
ELEMENTKG = Namespace("http://www.semanticweb.org/ElementKG#")

def download_file(url, path):
    """ Download a file from a given URL to a specified local path with a progress bar. """
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Get the total file size from headers
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte

    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    
    with open(path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")

def extract_chebi_subgraph(chebi_owl_path, parent_class_uri):
    """
    Extracts a subgraph from the CHEBI OWL file, including the parent node.
    """
    g = Graph()
    g.parse(chebi_owl_path, format="xml")
    subgraph = Graph()
    subgraph.bind("", CHEBI, override=True)
    
    def add_node_and_descendants(uri, subgraph, include_subclass=True):
        """
        Adds the node and its descendants to the subgraph.
        """


        # Add properties for the current node (parent node included)
        for p, o in g.predicate_objects(uri):
            if p == CHEBI_NS.smiles or (p == RDFS.subClassOf and include_subclass):
            # if p == RDFS.label or p == CHEBI_NS.smiles or (p == RDFS.subClassOf and include_subclass):
                subgraph.add((uri, p, o))
                
        # Recursively add descendants
        for child, _, _ in g.triples((None, RDFS.subClassOf, uri)):
            add_node_and_descendants(child, subgraph, include_subclass=True)
    
    parent_class = URIRef(parent_class_uri)
    add_node_and_descendants(parent_class, subgraph, include_subclass=False)
    return subgraph

def convert_to_elementkg_format(subgraph, chebi_functional_group_owl_path, smiles_file_path):
    """
    Converts the CHEBI subgraph into the ElementKG format.
    """
    new_g = Graph()
    new_g.bind("", ELEMENTKG, override=True)
    chebi_smiles = {}

    for s, p, o in subgraph:
        new_subject = ELEMENTKG[str(s).split('/')[-1]]

        new_g.add((new_subject, RDF.type, OWL.Class))

        # if p == RDFS.label:
        #     new_g.add((new_subject, p, o))
        if p == CHEBI_NS.smiles:
            chebi_smiles[str(s).split('/')[-1]] = o
            new_g.add((new_subject, RDF.type, OWL.NamedIndividual))
        elif p == RDFS.subClassOf:
            new_object = ELEMENTKG[str(o).split('/')[-1]]
            new_g.add((new_subject, p, new_object))
    
    # Serialize the new graph to an OWL file
    new_g.serialize(destination=chebi_functional_group_owl_path, format="xml")

    # Write CHEBI IDs and their SMILES to a text file
    with open(smiles_file_path, 'w') as f:
        for chebi_id, smiles in chebi_smiles.items():
            f.write(f"{chebi_id} {smiles}\n")

parent_class_uri = "http://purl.obolibrary.org/obo/CHEBI_24433"
chebi_owl_url = "https://ftp.ebi.ac.uk/pub/databases/chebi/ontology/chebi_core.owl"
chebi_owl_path = "KG/chebi_core2.owl"

output_dir = "temp"
chebi_functional_group_owl_path = f"{output_dir}/chebi_func.owl"
smiles_file_path = f"{output_dir}/funcgroup.txt"

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Ensure ChEBI OWL file exists, download if not
if not os.path.exists(chebi_owl_path):
    print("ChEBI core OWL file not found. Downloading...")
    if not os.path.exists('KG'):
        os.makedirs('KG')
    download_file(chebi_owl_url, chebi_owl_path)
    print("Download completed.")

# Extract the subgraph
subgraph = extract_chebi_subgraph(chebi_owl_path, parent_class_uri)

# Convert and format the subgraph for ElementKG
convert_to_elementkg_format(subgraph, chebi_functional_group_owl_path, smiles_file_path)

print("Process completed. ChEBI subgraph converted to ElementKG format.")
