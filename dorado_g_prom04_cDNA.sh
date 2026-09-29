#!/bin/bash
# ==============================================================================
# Script to run Dorado Basecaller inside an Apptainer container with GPU support
# ==============================================================================

# Exit immediately if a command exits with a non-zero status
set -e

# set the group before declare var
newgrp g_promethion04

# --- 1. CONFIGURATION PATHS (Update these to match your system) ---
# Path to your Apptainer/Singularity SIF image
APPTAINER_IMG=/home/cfrias/rebasecalling_eugene/software
IMAGE_SIF=${APPTAINER_IMG}/mi_dorado_estable.sif

# Host directories for inputs, outputs, and model files
INPUT_DIR=/home/cfrias/rebasecalling_eugene/input
FC="$1"
INPUT_DIR_FC=${INPUT_DIR}/${FC}
OUTPUT_BAM=/home/cfrias/rebasecalling_eugene/output


# Dorado Settings
dorado_version=dorado-2.1.1
# Example: 'dna_r10.4.1_e8.2_400bps_hac@v4.1.0' or just 'hac' for automatic detection
MODEL=dna_r10.4.1_e8.2_400bps_sup@v5.2.0
MODEL_NAME=${MODEL}
#only if is barcoded kit, this give an error is only a Ligatin kit
#kit=SQK-LSK114


# OUTPUT DIR NAME
#molecule=dna(or cDNA) or rna # cDNA
molecule=cDNA

OUTPUT_DIR_FC="${OUTPUT_BAM}/${FC}_${MODEL_NAME}_${molecule}_${dorado_version}_rebasecalling"
mkdir -p ${OUTPUT_DIR_FC}

# We mount your specific host folders as subfolders inside the container's existing /mnt
apptainer exec --nv --cleanenv \
    --bind "${INPUT_DIR_FC}"/pod5/:/mnt/input \
    --bind "${OUTPUT_DIR_FC}":/mnt/output \
    "$IMAGE_SIF" \
    dorado basecaller \
    -vv --recursive \
    --device "cuda:all" \
    --min-qscore 10 \
     "${MODEL_NAME}" \
    /mnt/input \
    --estimate-poly-a \
    --output-dir /mnt/output/ \
    --emit-summary
