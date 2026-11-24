Planned contents:
    - Data processing.
    - Demand analysis.
    - ZIP model comparisons.
    - Plotting and visualization.

This folder contains Python scripts used for processing data, analyzing simulation results, and generating plots.

## Preparing GridLAB-D profiles

Run `python python_scripts/prepare_players.py` from the project root (or invoke the script by absolute path). It uses `house_profile_1.csv`, `house_profile_2.csv`, and `house_profile_3.csv` to generate the three load players and `GridLAB-D_models/generated_houses.glm` with the corresponding three houses, shared water-draw input, and recorders. Other profile files in the folder are ignored.

The running model follows the upstream Node 1-to-Node 4 feeder topology and center-tapped service-transformer structure in `GridLAB-D_models/IEEE_Node_4_Feeder.glm`. The generated houses connect to the service transformer's split-phase secondary.

Run the model after preparing the files:

```powershell
gridlabd -D Z_FRAC=0.0 -D I_FRAC=0.0 -D P_FRAC=1.0 -D CASE_NAME=const_P -D XFMR_KVA=25 GridLAB-D_models/three_house_base.glm
```

Run the preparation script again whenever one of the three selected profiles changes.