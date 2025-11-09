# MIND-BPD Project Code & Materials
Mindfulness Intervention using Neurofeedback for Borderline Personality Disorder (MIND-BPD)

This repository contains research protocols, analysis pipelines, and implementation materials for a novel mindfulness-based real-time fMRI neurofeedback (mbNF) intervention targeting emotion dysregulation and Default Mode Network (DMN) hyperconnectivity in individuals with Borderline Personality Disorder.

## Background & Rationale

Borderline Personality Disorder (BPD) is characterized by severe emotion dysregulation, interpersonal difficulties, and impulsivity, affecting approximately 1.6% of the general population and up to 20% of psychiatric inpatients. Current treatments show limited efficacy for many patients, highlighting the need for novel interventions targeting core neurobiological mechanisms.

### Key Research Insights

- **Emotion Dysregulation in BPD**: Maladaptive emotional responses, difficulty regulating intense emotions, and impaired ability to return to emotional baseline following distress
- **Neural Correlates**: Emotion dysregulation in BPD is associated with altered functional connectivity within the default mode network (DMN) and reduced top-down cognitive control
- **DMN Alterations**: Aberrant DMN connectivity consistently demonstrated in BPD across multiple neuroimaging studies, linked to rumination and self-referential processing difficulties
- **Mindfulness as Treatment**: Dialectical Behavior Therapy (DBT) incorporates mindfulness as a core component, but neural mechanisms of therapeutic change remain unclear
- **Neurofeedback Potential**: Real-time fMRI neurofeedback may enhance mindfulness training by providing direct feedback on brain states associated with adaptive emotion regulation

## Study Overview

MIND-BPD employs mindfulness-based neurofeedback (mbNF) to train individuals with BPD to modulate their DMN activity patterns. Participants practice mindful describing (moment-to-moment awareness of sensory experience) while receiving real-time visual feedback based on their brain activity.

### Intervention Components

1. **Mindfulness Training**: Adapted mindful describing practice focusing on present-moment sensory awareness
2. **Real-time fMRI Neurofeedback**: Visual feedback (ball movement) reflecting DMN vs. Central Executive Network (CEN) activity balance
3. **Yoked Control Design**: SHAM participants receive pre-recorded feedback from matched REAL participants to control for visual stimulation effects

### Primary Outcomes

- Reduction in emotion dysregulation symptoms
- Improved DMN functional connectivity patterns
- Enhanced self-regulation capacity
- Neural signatures of successful neurofeedback learning

## Repository Contents

This repository contains all experimental code and analysis pipelines:

- **Installing the latest (XA30 compatible) version of MURFI**: [https://github.com/gablab/murfi2](https://github.com/gablab/murfi2)
- **Running MURFI for real-time processing**: [murfi-rt-PyProject](murfi-rt-PyProject)
- **Running the mindfulness neurofeedback ball task**: [psychopy/balltask](psychopy/balltask)
- **Running the self-reference task**: [self_reference](self_reference)
- **Running the Continuous Performance Task (gradCPT)**: [CPT](gradCPT)

## Key Features

### Real-time fMRI Neurofeedback System
- Processes fMRI data in real-time using MURFI
- Extracts DMN and CEN activity on a volume-by-volume basis (TR = 1.2s)
- Provides visual feedback via moving ball interface
- Implements yoked-control SHAM condition for rigorous experimental design

### Optimized Performance
- **80% reduction in frame file sizes** through intelligent downsampling
- **Smooth 60Hz visual feedback** for SHAM participants
- **Virtual hit counting** tracks SHAM participants' neural control capability
- **Automatic SHAM setup** with matched participant data copying
- **Complete data collection** ensures all 150 volumes captured for both groups

### Experimental Design
- **REAL mode**: Live neurofeedback based on participant's actual brain activity
- **SHAM mode**: Yoked visual feedback from matched REAL participant while still recording brain activity
- **Virtual hits**: Quantifies what SHAM participants' brains would have achieved if receiving real feedback
- **Adaptive difficulty**: Scale factor automatically adjusts between runs based on performance

## Clinical Significance

This intervention combines:
- Evidence-based mindfulness practices from DBT
- Cutting-edge real-time neuroimaging technology
- Rigorous yoked-control experimental design
- Personalized neural feedback for enhanced learning

The goal is to develop a neuroscience-informed intervention that enhances existing mindfulness-based treatments for BPD by directly targeting underlying neural mechanisms of emotion dysregulation.

## Getting Started

See individual directories for detailed setup instructions:
- [Ball Task Setup & Usage](psychopy/balltask/README.md)
- [MURFI Configuration](murfi-rt-PyProject/README.md)

## Citation

If you use this code or methods in your research, please cite:

```
[Citation to be added upon publication]
```

## Funding

This research is supported by the National Institute of Mental Health (NIMH) [Grant information to be added].

## Contact

For questions about the protocol or code, please contact:
- Clemens Bauer, PhD - Northeastern University / Massachusetts General Hospital
- [Additional contact information]

## License

[License information to be added]
