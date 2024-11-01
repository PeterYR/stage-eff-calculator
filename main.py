import pandas as pd
import requests
import sys

import pengstats

PETERYR_URL = "https://docs.google.com/spreadsheets/d/1PPtMMKODlSgosKYefDwiIs68elS_t5SrltvBC2s-YD0/export?gid=0&range=A:B&format=csv"
GAME_DATA_URL = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData_YoStar/main/en_US/gamedata/excel/item_table.json"

NAME_OVERRIDES = {
    "Purchase Certificate": "Shop Voucher",
    # "Transmuted Salt Agglomerate": "Aggloromated Salt",
    "Nucleic Crystal Sinter": "烧结核凝晶",
    "Skill Summary - 1": "Skill Summary 1",
    "Skill Summary - 2": "Skill Summary 2",
    "Skill Summary - 3": "Skill Summary 3",
}
# manage name discrepancies with interface spreadsheet
# { actual name : name on sheet }

SANITY_VALUE_OVERRIDES = {}

# add overrides for chips
for op_class in [
    "Vanguard",
    "Guard",
    "Defender",
    "Sniper",
    "Caster",
    "Medic",
    "Supporter",
    "Specialist",
]:
    for tier, chip_type in [
        ("T1", "Chip"),
        ("T2", "Chip Pack"),
        ("T3", "Dualchip"),
    ]:
        NAME_OVERRIDES[f"{op_class} {chip_type}"] = f"{tier} Chip"


def get_id_to_name() -> dict[str, str]:
    """Load map of itemId (from game data) to item name (for sanval map)"""
    game_data: dict = requests.get(GAME_DATA_URL).json()["items"]
    id_to_name: dict[str, str] = {}
    for id, data in game_data.items():
        name = data["name"]

        # use spreadsheet override if found
        id_to_name[data["itemId"]] = NAME_OVERRIDES.get(name, name)
    return id_to_name


def get_sanval_map() -> dict[str, float]:
    """Load sanity values map from interface Google Sheet"""
    peteryr_df = pd.read_csv(PETERYR_URL, header=None, names=["en_name", "sanval"])
    peteryr_sanvals = {}
    for _, row in peteryr_df.iterrows():
        en_name = row["en_name"]
        sanval = row["sanval"]
        peteryr_sanvals[en_name] = sanval
    return peteryr_sanvals


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <stage_id> <sanity cost> [extra LMD/san]")
        sys.exit()

    stage_id = sys.argv[1]
    sanity_cost = int(sys.argv[2])
    extra_lmd = 0

    if len(sys.argv) >= 4:
        extra_lmd = int(sys.argv[3])
    assert sanity_cost > 0

    matrix = pengstats.get_matrix()
    rates = pengstats.stage_rates(stage_id, matrix)

    id_to_name = get_id_to_name()
    peteryr_sanvals = get_sanval_map()

    print("ID", "Name", "Value", "Rate", sep=", ")

    total = 0
    for id, rate in rates.items():
        name = id_to_name.get(id, "n/a")
        sanval = peteryr_sanvals.get(name, 0)
        print(f"{id}, {name}, {sanval:.4f}, {rate:.4f}")
        total += sanval * rate

    total += (extra_lmd + 12) * sanity_cost * peteryr_sanvals["LMD"]

    print("\nStage efficiency:", total / sanity_cost)


if __name__ == "__main__":
    main()
