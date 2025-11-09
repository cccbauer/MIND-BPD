#!/bin/bash


# Run the Python script (assumes Python 2 environment is handled in psychopy)
onedrive --synchronize --single-directory 'MIND-BPD/psychopy' >> onedrive_log.txt
python rt-network_feedback_mgh.py
onedrive --synchronize --single-directory 'MIND-BPD/psychopy' >> onedrive_log.txt
