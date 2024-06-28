#!/bin/bash
EXP_NAME="finetune"

DATASETS=(qm7.csv qm8.csv qm9.csv)

# Ensure the logs directory exists
mkdir -p logs

# Loop over the datasets
for i in "${!DATASETS[@]}"; do
    # Calculate GPU ID (0-1) in a round-robin fashion
    # GPU_ID=$((i % 2))
    GPU_ID=0

    # Define log and error files for each dataset
    LOG_FILE="logs/${EXP_NAME}-${DATASETS[$i]}-log.txt"
    ERROR_FILE="logs/${EXP_NAME}-${DATASETS[$i]}-error.txt"
    
    # Export the GPU to be used for this job
    export CUDA_VISIBLE_DEVICES=$GPU_ID

    # Run the training command
    # nohup and the & at the end will run the script in the background
    nohup python train.py \
        --no_matching_limit \
        --kg_name elementkg \
        --data_path "./data/${DATASETS[$i]}" \
        --metric 'mae' \
        --dataset_type regression \
        --epochs 100 \
        --num_runs 3 \
        --gpu 0 \
        --batch_size 256 \
        --seed 43 \
        --init_lr 1e-4 \
        --split_type 'scaffold_balanced' \
        --step 'functional_prompt' \
        --exp_name "$EXP_NAME" \
        --exp_id "${DATASETS[$i]}" \
        --checkpoint_path "./dumped/pretrained_graph_encoder_reproduced/original_CMPN_0402_1558_12000th_epoch.pkl" > "$LOG_FILE" 2> "$ERROR_FILE" &
    
    sleep 5
done

echo "All fine-tuning processes have started."
