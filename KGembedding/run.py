import argparse
import os
from configparser import ConfigParser
from owl2vec_star import owl2vec_star

parser = argparse.ArgumentParser(description='Process an OWL file for embeddings.')
parser.add_argument('--owl_file', type=str, required=True,
                    choices=['elementkg.owl', 'elementkg_chebi_replace.owl', 'elementkg_chebi_integrate.owl'],
                    help='Path to the OWL file')
args = parser.parse_args()
kg_folder = os.path.splitext(os.path.basename(args.owl_file))[0]

# Read and update the configuration file
config = ConfigParser()
config.read('default.cfg')
config.set('BASIC', 'ontology_file', args.owl_file)

# Save the updated configuration to a temporary file
temp_config_path = 'temp_config.cfg'
with open(temp_config_path, 'w') as configfile:
    config.write(configfile)

gensim_model = owl2vec_star.extract_owl2vec_model("elementkg.owl", "default.cfg", True, True, True)

# Updating output folder path to include the kg_folder name
output_folder = f"./../initial/{kg_folder}/"

# Ensure the directory exists
os.makedirs(output_folder, exist_ok=True)

# Save in txt format
gensim_model.wv.save_word2vec_format(output_folder+"elementkgontology.embeddings.txt", binary=False)

# Remove the temporary config file
os.remove(temp_config_path)