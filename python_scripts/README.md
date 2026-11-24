Planned contents:
    - Data processing.
    - Demand analysis.
    - ZIP model comparisons.
    - Plotting and visualization.

This folder contains Python scripts used for processing data, analyzing simulation results, and generating plots.

## Preparing GridLAB-D profiles

Run `python python_scripts/prepare_players.py` from the project root (or invoke the script by absolute path). It discovers every `data/household_profiles/house_profile_<number>.csv`, writes the corresponding `GridLAB-D_models/house_<number>_load.player`, and generates `GridLAB-D_models/generated_houses.glm` with a house, shared water-draw input, and recorders for each profile.

Run the model after preparing the files:

```powershell
gridlabd -D Z_FRAC=0.0 -D I_FRAC=0.0 -D P_FRAC=1.0 -D CASE_NAME=const_P -D XFMR_KVA=25 GridLAB-D_models/three_house_base.glm
```

Run the preparation script again whenever profiles are added, removed, or changed.