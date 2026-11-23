from pathlib import Path

import pandas as pd

PF = 0.95
SELECTED_HOUSES = [1, 2, 3]  # Update if assigned different profiles
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROFILE_DIR = PROJECT_ROOT / "data" / "household_profiles"
PLAYER_DIR = PROJECT_ROOT / "GridLAB-D_models"

for idx, h in enumerate(SELECTED_HOUSES, start=1):
    df = pd.read_csv(PROFILE_DIR / f"house_profile_{h}.csv")
    # Convert real power (kW) to apparent base_power_12 (VA) at 0.95 PF
    s_va = (df["house power (kW)"] * 1000.0) / PF
    
    player_df = pd.DataFrame({
        "Time": df["Time"],
        "Value": s_va.round(4)
    })
    # GridLAB-D player format: no header, comma-separated
    player_df.to_csv(PLAYER_DIR / f"house_{idx}_load.player", index=False, header=False)

print("Player files generated successfully.")