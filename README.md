# NAC and Approach–Avoidance Bias Study

This repository contains the data processing and analysis pipeline for a randomized, double-blind, placebo-controlled study investigating the effects of **N-acetylcysteine (NAC)** on approach–avoidance biases and craving in cocaine-dependent patients undergoing inpatient detoxification.

---

## Study Design

### Summary
- **Population:** Cocaine-dependent adults (18–65 years)
- **Setting:** Addiction Medicine Unit 73, Brugmann University Hospital, Brussels
- **Design:** Randomized, double-blind, placebo-controlled
- **Duration:** 5 consecutive days

### Intervention
- **NAC group:** 2,400 mg/day oral N-acetylcysteine  
- **Placebo group:** Matching placebo capsules

### Outcomes
**Primary outcomes**
- Approach–avoidance bias (R-SRC score)
- Craving (CCQ-Brief)

**Secondary outcomes**
- Mood
- Anxiety
- Impulsivity
- Metacognition
- Hedonic capacity

---

## Data Description

### R-SRC / Approach–Avoidance Task
- **Stimuli:**
  - 16 cocaine-related images
  - 16 neutral images
- **Blocks:**
  - Compatible (approach cocaine / avoid neutral)
  - Incompatible (avoid cocaine / approach neutral)
- **Trials:**
  - 64 trials per block  
  - 128 trials total

---

## Requirements

### Software
- **Python ≥ 3.8**
- **Affect 4.0**

### Python Packages
- `pandas`
- `csv`
- `os`

---

## Notes
This repository is intended for research and analysis purposes only. Data are handled in accordance with ethical and institutional guidelines.
