#!/bin/bash

# Allow current user to access X11 display
xhost +SI:localuser:$(whoami)

# Define paths
DICOM_FOLDER="$(pwd)"
SIF_IMAGE="./murfi-sif_latest.sif"
XML_FILE="$1"

# Run murfi via Singularity with X11 support
singularity exec \
  -B /tmp/.X11-unix:/tmp/.X11-unix \
  -B "${DICOM_FOLDER}" \
  -e \
  --env DISPLAY=$DISPLAY \
  --env QT_QPA_PLATFORM=xcb \
  "${SIF_IMAGE}" \
  murfi -f "${XML_FILE}"

