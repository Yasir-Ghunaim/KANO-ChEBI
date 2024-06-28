#!/bin/bash
EXP_NAME="finetune"
LOG_FILE="logs/${EXP_NAME}-log.txt"
ERROR_FILE="logs/${EXP_NAME}-error.txt"

# Ensure the logs directory exists
mkdir -p logs

export CUDA_VISIBLE_DEVICES=0
python train.py \
    --no_matching_limit \
    --kg_name elementkg \
    --data_path ./data/qm7.csv \
    --metric 'mae' \
    --dataset_type regression \
    --epochs 100 \
    --num_runs 3 \
    --gpu 0 \
    --batch_size 256 \
    --seed 43 \
    --init_lr 1e-4  \
    --split_type 'scaffold_balanced' \
    --step 'functional_prompt' \
    --exp_name "$EXP_NAME" \
    --exp_id qm7 \
    --checkpoint_path "./dumped/pretrained_graph_encoder_reproduced/original_CMPN_0402_1558_12000th_epoch.pkl"
