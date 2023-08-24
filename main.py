import pandas as pd
import requests
import sys

import pengstats

PETERYR_URL = "https://docs.google.com/spreadsheets/d/1PPtMMKODlSgosKYefDwiIs68elS_t5SrltvBC2s-YD0/export?gid=0&range=A:B&format=csv"
GAME_DATA_URL = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/item_table.json"

NAME_OVERRIDES = {
    "Purchase Certificate": "Shop Voucher",
    "Transmuted Salt Agglomerate": "Aggloromated Salt",
    "Nucleic Crystal Sinter": "烧结核凝晶",
    "Skill Summary - 1": "Skill Summary 1",
    "Skill Summary - 2": "Skill Summary 2",
    "Skill Summary - 3": "Skill Summary 3",
}
# { actual name : peteryr name }

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
    id_to_name: dict[str, str] = {}  # will include non-official names
    for id, data in game_data.items():
        name = data["name"]
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
        print(f"Usage: python {sys.argv[0]} <stage_id> <sanity cost> [extra LMD/san]")
        sys.exit()

    stage_id = sys.argv[1]
    sanity_cost = int(sys.argv[2])
    extra_lmd = 0

    if len(sys.argv) >= 4:
        extra_lmd = int(sys.argv[3])
    assert sanity_cost > 0

    # stage_id = "act15side_06"
    # sancost = 18

    pengstats.initialize_matrix()
    rates = pengstats.stage_rates(stage_id)

    total = 0

    print("\tID", "Name", "Value", "Rate", sep=", ")

    id_to_name = get_id_to_name()
    peteryr_sanvals = get_sanval_map()

    ######## MH COLLAB TEMPORARY MEASURE ########

    # special 2k LMD "item" on penguin stats
    id_to_name["4001_2000"] = "2k LMD"
    peteryr_sanvals["2k LMD"] = peteryr_sanvals["LMD"] * 2000

    # add gacha pull to sanvals map
    mh_rates = pengstats.stage_rates("act24side_gacha")
    peteryr_sanvals["mh_gacha"] = 0
    for id, rate in mh_rates.items():
        name = id_to_name.get(id, None)
        sanval = peteryr_sanvals.get(name, 0)
        peteryr_sanvals["mh_gacha"] += sanval * rate

    #############################################

    for id, rate in rates.items():
        name = id_to_name.get(id, None)
        sanval = peteryr_sanvals.get(name, 0)
        print("\t" + id, name, sanval, rate, sep=", ")
        total += sanval * rate

    total += (extra_lmd + 12) * sanity_cost * peteryr_sanvals["LMD"]

    print("Efficiency:", total / sanity_cost)

    # # print(peteryr_sanvals)
    # for en_name in peteryr_sanvals["en_name"]:
    #     if en_name not in id_to_name.values():
    #         print(en_name)
    #         ...
    #         # problematic item name


if __name__ == "__main__":
    main()
