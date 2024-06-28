from rdflib import Graph, URIRef, RDF, RDFS

# Load the original ElementKG graph
elementkg_graph = Graph()
elementkg_graph.parse("./KGembedding/elementkg.owl", format="xml")


# Define the functionalGroup URI
functional_group_uri = URIRef("http://www.semanticweb.org/ElementKG#functionalGroup")
additional_relations_to_be_removed = [
    URIRef("http://www.semanticweb.org/ElementKG#Sulfonate"),
    URIRef("http://www.semanticweb.org/ElementKG#Sulfino"),
    URIRef("http://www.semanticweb.org/ElementKG#Nitroso"),
    URIRef("http://www.semanticweb.org/ElementKG#Phosphono"),
    URIRef("http://www.semanticweb.org/ElementKG#Cyanate"),
    URIRef("http://www.semanticweb.org/ElementKG#Hydroperoxy"),
    URIRef("http://www.semanticweb.org/ElementKG#Carbamate"),
    URIRef("http://www.semanticweb.org/ElementKG#Borono"),
    URIRef("http://www.semanticweb.org/ElementKG#Nitrosooxy"),
    URIRef("http://www.semanticweb.org/ElementKG#Thionoester"),
    URIRef("http://www.semanticweb.org/ElementKG#Nitro"),
    URIRef("http://www.semanticweb.org/ElementKG#Carboxamide"),
    URIRef("http://www.semanticweb.org/ElementKG#Borinate"),
    URIRef("http://www.semanticweb.org/ElementKG#Peroxy"),
    URIRef("http://www.semanticweb.org/ElementKG#Carbonyl"),
    URIRef("http://www.semanticweb.org/ElementKG#CarbothioicSAcid"),
    URIRef("http://www.semanticweb.org/ElementKG#CarbonateEster"),
    URIRef("http://www.semanticweb.org/ElementKG#Sulfonyl"),
    URIRef("http://www.semanticweb.org/ElementKG#Carboxyl"),
    URIRef("http://www.semanticweb.org/ElementKG#CarboxylicAnhydride"),
    URIRef("http://www.semanticweb.org/ElementKG#Carboalkoxy"),
    URIRef("http://www.semanticweb.org/ElementKG#CarbothioicOAcid"),
    URIRef("http://www.semanticweb.org/ElementKG#Thiolester"),
    URIRef("http://www.semanticweb.org/ElementKG#Isocyanate"),
    URIRef("http://www.semanticweb.org/ElementKG#Sulfo"),
    URIRef("http://www.semanticweb.org/ElementKG#Hydroxyl"),
    URIRef("http://www.semanticweb.org/ElementKG#Boronate"),
    URIRef("http://www.semanticweb.org/ElementKG#Borino"),
    URIRef("http://www.semanticweb.org/ElementKG#Haloformyl"),
    URIRef("http://www.semanticweb.org/ElementKG#Methylenedioxy"),
    URIRef("http://www.semanticweb.org/ElementKG#Sulfinyl"),
    URIRef("http://www.semanticweb.org/ElementKG#Carbodithio"),
    URIRef("http://www.semanticweb.org/ElementKG#Imine"),
    URIRef("http://www.semanticweb.org/ElementKG#Oxime"),
    URIRef("http://www.semanticweb.org/ElementKG#PrimaryAldimine"),
    URIRef("http://www.semanticweb.org/ElementKG#Sulfoate"),
    URIRef("http://www.semanticweb.org/ElementKG#Isothiocyanate"),
    URIRef("http://www.semanticweb.org/ElementKG#SecondaryAldimine"),
    URIRef("http://www.semanticweb.org/ElementKG#PrimaryKetimine"),
    URIRef("http://www.semanticweb.org/ElementKG#SecondaryKetimine"),
    URIRef("http://www.semanticweb.org/ElementKG#Alkenyl"),
    URIRef("http://www.semanticweb.org/ElementKG#CarbodithioicAcid"),
    URIRef("http://www.semanticweb.org/ElementKG#Azo"),
    URIRef("http://www.semanticweb.org/ElementKG#Alkynyl"),
    URIRef("http://www.semanticweb.org/ElementKG#Sulfhydryl"),
    URIRef("http://www.semanticweb.org/ElementKG#bromo"),
    URIRef("http://www.semanticweb.org/ElementKG#4ammoniumIon"),
    URIRef("http://www.semanticweb.org/ElementKG#Phenyl"),
    URIRef("http://www.semanticweb.org/ElementKG#iodo"),
    URIRef("http://www.semanticweb.org/ElementKG#halo"),
    URIRef("http://www.semanticweb.org/ElementKG#chloro"),
    URIRef("http://www.semanticweb.org/ElementKG#Alkyl"),
    URIRef("http://www.semanticweb.org/ElementKG#Pyridyl"),
    URIRef("http://www.semanticweb.org/ElementKG#Isonitrile"),
    URIRef("http://www.semanticweb.org/ElementKG#fluoro"),
    URIRef("http://www.semanticweb.org/ElementKG#PrimaryAmine"),
    URIRef("http://www.semanticweb.org/ElementKG#SecondaryAmine"),
    URIRef("http://www.semanticweb.org/ElementKG#TertiaryAmine"),
    URIRef("http://www.semanticweb.org/ElementKG#Phosphino"),

]

# Collect URIs of functionalGroup and all its subclasses to be removed
entities_to_remove = {functional_group_uri}

def collect_subclasses(uri):
    for subclass in elementkg_graph.subjects(RDFS.subClassOf, uri):
        entities_to_remove.add(subclass)
        collect_subclasses(subclass)

collect_subclasses(functional_group_uri)


for element in additional_relations_to_be_removed:
    entities_to_remove.add(element)


# Remove functionalGroup and its subclasses without altering other elements
for entity in entities_to_remove:
    # Remove all statements where the entity is subject
    elementkg_graph.remove((entity, None, None))
    elementkg_graph.remove((None, None, entity))


# Serialize and save the modified graph without changing the rest of the structure
elementkg_graph.serialize(destination="temp/elementkg_modified.owl", format="xml")
print(f"Removed functionalGroup and its subclasses. Total removed: {len(entities_to_remove)}")
