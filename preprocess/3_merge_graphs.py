from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import OWL
import shutil, os

# from rdflib import Graph, Namespace, URIRef
# from rdflib.namespace import OWL, RDF, RDFS

def merge_elementkg_chebi(
    elementkg_owl_path, 
    chebi_func_owl_path, 
    output_owl_path, 
    chebi_funcgroup_txt_path, 
    output_funcgroup_txt_path,
    elementkg_funcgroup_txt_path=None):
    """
    Merges ElementKG graph with Chebi Functional Group graph and handles funcgroup.txt integration.

    :param elementkg_owl_path: Path to the ElementKG OWL file.
    :param chebi_func_owl_path: Path to the Chebi Functional Group OWL file.
    :param output_owl_path: Path where the combined OWL graph will be saved.
    :param chebi_funcgroup_txt_path: Path to the funcgroup.txt file for the Chebi functional groups.
    :param output_funcgroup_txt_path: Path where the final funcgroup.txt will be saved.
    :param elementkg_funcgroup_txt_path: Path to the funcgroup.txt file for ElementKG (if modifying ElementKG).
    """
    # Load the ElementKG graph
    elementkg_graph = Graph()
    elementkg_graph.parse(elementkg_owl_path, format="xml")

    # Load the Chebi Functional Group graph
    chebi_func_graph = Graph()
    chebi_func_graph.parse(chebi_func_owl_path, format="xml")

    # Merge the two graphs
    combined_graph = elementkg_graph + chebi_func_graph

    # Namespace for ElementKG
    ELEMENTKG = Namespace("http://www.semanticweb.org/ElementKG#")

    # Add disjointWith relationship for #element
    element_class = ELEMENTKG.element
    chebi_24433_class = ELEMENTKG.CHEBI_24433
    combined_graph.add((element_class, OWL.disjointWith, chebi_24433_class))

    # Load and integrate funcgroup.txt files
    integrate_funcgroup_txt(combined_graph, chebi_funcgroup_txt_path, ELEMENTKG)

    # If modifying ElementKG, integrate its funcgroup.txt as well
    if elementkg_funcgroup_txt_path:
        # Concatenate funcgroup.txt files
        with open(output_funcgroup_txt_path, 'wb') as wfd:
            for f in [elementkg_funcgroup_txt_path, chebi_funcgroup_txt_path]:
                with open(f, 'rb') as fd:
                    shutil.copyfileobj(fd, wfd)
    else:
        shutil.copy(chebi_funcgroup_txt_path, output_funcgroup_txt_path)

    # Serialize and save the combined graph
    combined_graph.serialize(destination=output_owl_path, format="xml")
    print("The ElementKG and Chebi functional groups have been successfully combined.")

def integrate_funcgroup_txt(graph, chebi_funcgroup_txt_path, ELEMENTKG):
    """
    Integrates funcgroup.txt into the provided graph.

    :param graph: The RDFLib Graph instance to integrate funcgroup.txt into.
    :param chebi_funcgroup_txt_path: Path to the funcgroup.txt file.
    :param ELEMENTKG: Namespace object for ElementKG.
    """
    with open(chebi_funcgroup_txt_path, "r") as file:
        for line in file:
            chebi_id, smiles = line.strip().split(' ', 1)
            # Simplified extraction of unique atom types from the SMILES string
            atom_types = set(filter(str.isalpha, smiles))
            for atom_type in atom_types:
                atom_uri = URIRef(ELEMENTKG[atom_type])
                # Construct the isPartOf relationship
                graph.add((atom_uri, URIRef(ELEMENTKG.isPartOf), URIRef(ELEMENTKG[chebi_id])))


output_dir = "outputs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Replace operation
merge_elementkg_chebi(
    elementkg_owl_path="temp/elementkg_modified.owl",
    chebi_func_owl_path="temp/chebi_func.owl",
    output_owl_path=f"{output_dir}/elementkg_chebi_replace.owl",
    chebi_funcgroup_txt_path="temp/funcgroup.txt",
    output_funcgroup_txt_path=f"{output_dir}/funcgroup_replace.txt"
)

# Integrate operation
merge_elementkg_chebi(
    elementkg_owl_path="./../KGembedding/elementkg.owl",
    chebi_func_owl_path="temp/chebi_func.owl",
    output_owl_path=f"{output_dir}/elementkg_chebi_integrate.owl",
    chebi_funcgroup_txt_path="temp/funcgroup.txt",
    elementkg_funcgroup_txt_path="./../chemprop/data/elementkg/funcgroup.txt",
    output_funcgroup_txt_path=f"{output_dir}/funcgroup_integrate.txt"
)
