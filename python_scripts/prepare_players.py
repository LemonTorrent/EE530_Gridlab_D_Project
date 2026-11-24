import re
from pathlib import Path

import pandas as pd

PF = 0.95
SELECTED_HOUSES = (1, 2, 3)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROFILE_DIR = PROJECT_ROOT / "data" / "household_profiles"
PLAYER_DIR = PROJECT_ROOT / "GridLAB-D_models"
MODEL_FRAGMENT = PLAYER_DIR / "generated_houses.glm"
PROFILE_NAME = re.compile(r"house_profile_(\d+)\.csv")

profiles = [
    (house_number, PROFILE_DIR / f"house_profile_{house_number}.csv")
    for house_number in SELECTED_HOUSES
]
missing_profiles = [path for _, path in profiles if not path.is_file()]
if missing_profiles:
    missing_names = ", ".join(path.name for path in missing_profiles)
    raise FileNotFoundError(f"Required household profile(s) not found in {PROFILE_DIR}: {missing_names}")

house_objects = []
for house_number, profile_path in profiles:
    df = pd.read_csv(profile_path)
    required_columns = {"Time", "house power (kW)"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        raise ValueError(f"{profile_path} is missing columns: {', '.join(sorted(missing_columns))}")

    apparent_power = (df["house power (kW)"] * 1000.0) / PF
    player_df = pd.DataFrame({
        "Time": df["Time"],
        "Value": apparent_power.round(4),
    })
    player_df.to_csv(
        PLAYER_DIR / f"house_{house_number}_load.player",
        index=False,
        header=False,
    )

    house_objects.append(f"""// HOUSE {house_number}
object triplex_line {{
    name line_h{house_number};
    phases AS;
    from xfmr_secondary;
    to meter_h{house_number};
    length 50 ft;
    configuration tp_line_config;
}}

object triplex_meter {{
    name meter_h{house_number};
    phases AS;
    nominal_voltage 120;
}}

object triplex_load {{
    name load_h{house_number};
    parent meter_h{house_number};
    phases AS;
    nominal_voltage 120;
    impedance_fraction_12 ${{Z_FRAC}};
    current_fraction_12   ${{I_FRAC}};
    power_fraction_12     ${{P_FRAC}};
    impedance_pf_12 0.95;
    current_pf_12   0.95;
    power_pf_12     0.95;
    object player {{
        property base_power_12;
        file "GridLAB-D_models/house_{house_number}_load.player";
    }};
}}

object house {{
    name house_host_{house_number};
    parent meter_h{house_number};
    heating_system_type NONE;
    cooling_system_type NONE;
    auxiliary_system_type NONE;
    object waterheater {{
        name wh_{house_number};
        location INSIDE;
        tank_volume 50.0;
        tank_setpoint 120.0;
        thermostat_deadband 2.0;
        heating_element_capacity 4.5 kW;
        inlet_water_temperature 60.0;
        tank_UA 3.0;
        temperature 120.0;
        object player {{
            property water_demand;
            file "data/water_draw/water_draw.csv";
        }};
    }};
}}

object recorder {{
    parent meter_h{house_number};
    property measured_real_power,measured_reactive_power,measured_voltage_1,measured_voltage_2,measured_current_1;
    interval 60;
    file "out_${{CASE_NAME}}_${{XFMR_KVA}}kVA_m{house_number}.csv";
}}

object recorder {{
    parent wh_{house_number};
    property actual_power,temperature,water_demand;
    interval 60;
    file "out_${{CASE_NAME}}_${{XFMR_KVA}}kVA_wh{house_number}.csv";
}}""")

MODEL_FRAGMENT.write_text("\n\n".join(house_objects) + "\n", encoding="utf-8")
print(f"Generated load players and model objects for {len(profiles)} houses.")
