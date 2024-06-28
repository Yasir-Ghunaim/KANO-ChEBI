# Large-Scale Knowledge Integration for Enhanced Molecular Property Prediction

This repository is for the paper titled "Large-Scale Knowledge Integration for Enhanced Molecular Property Prediction," accepted as a short paper at NeSy 2024.

It is forked from [KANO](https://github.com/HICAI-ZJU/KANO) and follows the same training setup. We recommend reviewing the original README at [`Original_README.md`](Original_README.md) for foundational context.


## Project Overview
This project enhances the KANO model by expanding its ElementKG with the ChEBI knowledge graph, which includes over 2,840 functional groups—far exceeding the original 82. By integrating this vast chemical knowledge into both pre-training and fine-tuning phases, we aim to improve molecular property predictions. Our approach utilizes two methods, Replace and Integrate, to effectively incorporate these enhancements.

# Requirements
To set up the required environment, run the following command:
```sh
conda env create -f environment.yml
```

# Step-by-step guidelines

### Knowledge Graphs 
We maintain three versions of the knowledge graph:
- [`KGembedding/elementkg.owl`](KGembedding/elementkg.owl)
- [`KGembedding/elementkg_chebi_replace.owl`](KGembedding/elementkg_chebi_replace.owl)
- [`KGembedding/elementkg_chebi_integrate.owl`](KGembedding/elementkg_chebi_integrate.owl)

To generate `elementkg_chebi_replace.owl` and `elementkg_chebi_integrate.owl`, we run a series of scripts located in the [`preprocess`](preprocess) directory in the following sequence:
- `1_extract_chebi_groups.py`: Extracts ChEBI functional groups and reformats them to fit the ElementKG structure. The generated ChEBI files will be stored in `preprocess/temp`.
- `2_remove_elementkg_groups.py`: Used for the Replace operation, this script removes functional groups from ElementKG.
- `3_merge_graphs.py`: Merges graphs for the Replace and Integrate operations, creating both `elementkg_chebi_replace.owl` and `elementkg_chebi_integrate.owl`. 

The resulting knowledge graphs are stored in `preprocess/outputs`. Follow these steps for proper organization:

1. Manually move the `.owl` files to the [`KGembedding`](KGembedding) directory.
2. Rename `funcgroup_<operation>.txt` files to `funcgroup.txt`.
3. Move the renamed files to the appropriate directory: `chemprop/data/elementkg_chebi_<operation>`, where `<operation>` is either `replace` or `integrate`.



### Re-generating the Knowledge Graph Embeddings
To re-run the pre-training, you first need obtain the embeddings of the KGs by executing:
```sh
cd KGembedding
python run.py --owl_file <owl_file_name>
```

Replace `<owl_file_name>` with the appropriate OWL file name: `elementkg.owl`, `elementkg_chebi_replace.owl`, or `elementkg_chebi_integrate.owl`. Note that pre-trained embeddings are already provided at `initial/<knowledge_graph_name>/elementkgontology.embeddings.txt`, where `<knowledge_graph_name>` corresponds to the knowledge graph used.


After obtaining the embeddings, preprocess them for pre-training:
```sh
cd initial
python get_dict.py --kg_name <knowledge_graph_name>
```
Set <knowledge_graph_name> to `elementkg`, `elementkg_chebi_replace`, or `elementkg_chebi_integrate` as required.


### Pre-training
For pre-training, use the script [`my_pretrain.sh`](my_pretrain.sh). This script allows you to specify which knowledge graph to use by changing the `--kg_name` parameter inside the script. This parameter should be set to the same knowledge graph name used in previous steps, such as `elementkg`, `elementkg_chebi_replace`, or `elementkg_chebi_integrate`. Here's how you can run the script:
```sh
bash my_pretrain.sh
```
The script runs in the background and stores the results under the `logs` folder. The results of the pre-training will be stored in the [`dumped`](dumped) folder under the experiment name specified as `exp_name` in the script, prefixed with the date.


### Fine-tuning
For fine-tuning, we provide a script for running a single dataset under [`my_finetune_single.sh`](my_finetune_single.sh). This script introduces two additional parameters compared to the original KANO implementation:
- `--no_matching_limit`, which specifies the removal of the 13-match limit for functional group detection.
- `--kg_name <knowledge_graph_name>`, which determines which knowledge graph's embeddings to load. This parameter accepts the same values as previously used: `elementkg`, `elementkg_chebi_replace`, or `elementkg_chebi_integrate`

For running groups of datasets, we offer scripts that launch multiple experiments in parallel across the specified number of GPUs:
- [`my_finetune_classification.sh`](my_finetune_classification.sh) for classification tasks,
- [`my_finetune_regression_mae.sh`](my_finetune_regression_mae.sh) for regression tasks using MAE metric,
- [`my_finetune_regression.sh`](my_finetune_regression.sh) for other regression tasks using MSE metric.

Each script runs experiments in the background and stores the results under the `logs` folder. For each script, you will need to define `--kg_name` according to the desired knowledge graph.


### Citation
To be added