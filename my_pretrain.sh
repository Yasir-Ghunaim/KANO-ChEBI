#!/bin/bash
EXP_NAME="pre-train"
LOG_FILE="logs/${EXP_NAME}-log.txt"
ERROR_FILE="logs/${EXP_NAME}-error.txt"

# Ensure the logs directory exists
mkdir -p logs


export CUDA_VISIBLE_DEVICES=0
# nohup and the & at the end will run the script in the background
python pretrain.py \
    --exp_name "$EXP_NAME" \
    --exp_id 1 \
    --step pretrain \
    --kg_name elementkg 
