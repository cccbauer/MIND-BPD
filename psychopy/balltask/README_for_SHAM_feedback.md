# MIND-BPD Balltask - REAL vs SHAM Mode

## Overview
The Balltask can be run in **REAL** or **SHAM** mode based on the randomization assignment in `feedback/mgh_randlist.txt`.

---

## REAL Mode
- **Assignment**: Participants with 'R' designation in the randomization list
- **Data Source**: Live DMN/CEN data from `murfi_activation_communicator.py`
- **Behavior**: 
  - Ball movement is controlled by real-time fMRI neurofeedback
  - Frame data is automatically saved to `data/sub-mindbpdXXXX/` folder
  - Frame files are saved at ~30fps (every 5th frame) for efficiency
  - All 150 volumes of MURFI data are collected

---

## SHAM Mode
- **Assignment**: Participants with 'S' designation in the randomization list
- **Data Source**: Pre-recorded feedback frames from a matched REAL participant
- **Behavior**:
  - Ball movement replays yoked feedback from the matched participant
  - Visual feedback is displayed at smooth 60Hz
  - MURFI data is still collected (150 volumes) but not used for ball movement
  - Participant experiences identical visual feedback as their matched REAL participant

---

## Automatic SHAM Setup (Recommended)

The script now **automatically handles SHAM participant setup**:

1. **Randomization file determines assignment**:
   - The script reads `feedback/mgh_randlist.txt`
   - Subtracts 2000 from participant ID to find the row
   - 'R' in column 2 → REAL mode
   - 'S' in column 2 → SHAM mode

2. **Automatic matching and data copying**:
   - Script automatically identifies the matched REAL participant
   - Copies frame data from `data/sub-mindbpdXXXX/` to `feedback/sub-mindbpdXXXX/`
   - All `*_feedback_X_frames.csv` files are copied automatically
   - No manual intervention needed!

3. **Run the participant**:
   - Simply run the script with the SHAM participant ID
   - The script handles everything automatically

---

## Manual SHAM Setup (If Needed)

If automatic setup fails or you need to manually prepare a SHAM participant:

### Step 1: Identify the Matched Participant
Check `feedback/mgh_randlist.txt` to find which REAL participant is matched to your SHAM participant.

Example randomization file:
```
1    R    R001
2    S    S002
```
Here, S002 is matched to R001.

### Step 2: Create SHAM Feedback Folder
```bash
mkdir -p feedback/sub-mindbpd2002
```

### Step 3: Copy Frame Files from Matched Participant
```bash
cp data/sub-mindbpd2001/*_feedback_*_frames.csv feedback/sub-mindbpd2002/
```

### Step 4: Verify Files Exist
Ensure the following files are present for each run:
```
feedback/sub-mindbpd2002/sub-mindbpd2001_DMN_feedback_1_frames.csv
feedback/sub-mindbpd2002/sub-mindbpd2001_DMN_feedback_2_frames.csv
feedback/sub-mindbpd2002/sub-mindbpd2001_DMN_feedback_3_frames.csv
...
```

### Step 5: Run the SHAM Participant
The script will automatically detect the SHAM assignment and use the copied frame files.

---

## Key Improvements in Updated Script

### 1. **Optimized Frame Saving (REAL participants)**
- Saves every 5th frame (~30fps instead of 144fps)
- **80% reduction in file size** with no perceptible visual difference
- Typical frame file: ~3MB instead of ~15MB

### 2. **Smooth SHAM Playback**
- Pre-converts CSV data to numpy arrays (10x faster access)
- Automatically downsamples to 60Hz for smooth playback
- Proper timing control using dedicated playback clock
- **No more jerky or delayed ball movement!**

### 3. **Complete MURFI Data Collection**
- SHAM mode now collects all 150 volumes of MURFI data
- Continues collecting after visual playback ends
- Waits up to 5 TRs (6 seconds) for final volumes
- Ensures data completeness for both REAL and SHAM

### 4. **Automatic SHAM Preparation**
- Script automatically copies matched participant data
- No manual file copying required (but still supported)
- Error checking ensures matched data exists before running

### 5. **Harmonized Console Output**
- Both REAL and SHAM print every 10th frame to terminal
- Reduces console spam while maintaining progress visibility
- Consistent monitoring experience

---

## Troubleshooting

### "CSV file error" or "Folder does not exist"
**Cause**: Matched REAL participant hasn't been run yet, or frame files are missing.

**Solution**: 
1. Check if the matched REAL participant has completed at least one feedback run
2. Verify frame files exist in `data/sub-mindbpdXXXX/`
3. Manually copy files following the Manual SHAM Setup steps above

### "WARNING: Expected 150 volumes but only got X"
**Cause**: MURFI stopped sending data early or timing issue.

**Solution**: 
- Check MURFI is running and sending data
- Verify network connection between stimulus and MURFI computers
- Check for motion correction issues that might pause processing

### SHAM ball movement is jerky or delayed
**Cause**: Old script version without optimization.

**Solution**: 
- Ensure you're using the updated script with numpy array pre-conversion
- Check that downsampling is occurring (should see "Downsampled from XXXHz to ~60Hz" message)
- Verify frame files from REAL participant are not corrupted

### Participant assignment is wrong
**Cause**: Incorrect participant ID or randomization file error.

**Solution**:
- Verify participant ID is correct (should be 20XX format)
- Check `feedback/mgh_randlist.txt` has correct assignments
- Ensure randomization list row matches: `participant_id - 2000`

---

## File Structure

```
MIND-BPD/psychopy/balltask/
├── rt-network_feedback_mgh.py          # Main experiment script
├── feedback/
│   ├── mgh_randlist.txt                # Randomization assignments (R/S)
│   └── sub-mindbpdXXXX/                # SHAM participant folders (auto-created)
│       └── *_feedback_X_frames.csv     # Copied frame files
└── data/
    └── sub-mindbpdXXXX/                # REAL participant data
        ├── *_feedback_X_frames.csv     # Original frame recordings
        └── *_roi_outputs.csv           # MURFI data outputs
```

---

## Validation Checklist

Before running a SHAM participant, verify:

- [ ] Randomization file shows 'S' assignment for this participant
- [ ] Matched REAL participant has completed all required runs
- [ ] Frame files exist in either `data/` or `feedback/` folder
- [ ] Frame files contain data (file size >1MB typically)
- [ ] MURFI is running and communicating properly
- [ ] Script version includes numpy optimization (check for downsampling messages)

---

## Performance Metrics

**REAL Mode:**
- Frame saving: ~30fps (every 5th frame)
- Frame file size: ~3MB per run
- MURFI collection: 150 volumes
- Terminal updates: Every 10th frame

**SHAM Mode:**
- Playback rate: Smooth 60Hz
- Data loading: 10x faster (numpy arrays)
- MURFI collection: 150 volumes
- Visual timing: Synchronized to original recording
- Terminal updates: Every 10th frame

---

## Notes

- The script maintains backward compatibility with manual SHAM setup
- All MIND-BPD-specific randomization logic is preserved
- Frame files from REAL participants can be reused for multiple SHAM participants
- SHAM participants still generate complete MURFI data files for QC purposes
