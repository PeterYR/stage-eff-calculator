import pandas as pd
import requests


# Penguin stats docs: https://penguin-stats.cn/swagger/index.html

PENGUIN_URL = "https://penguin-stats.io/PenguinStats/api/v2"
PENGUIN_COLUMNS = {
    "stageId": "string",
    "itemId": "string",
    "times": int,
    "quantity": int,
}


def get_matrix():
    """Request and load drop matrix into memory"""

    global matrix

    r = requests.get(PENGUIN_URL + "/result/matrix", params={"show_closed_zones": True})
    matrix = pd.DataFrame.from_records(
        r.json()["matrix"],
        columns=PENGUIN_COLUMNS.keys(),
    )

    return matrix.astype(PENGUIN_COLUMNS)


def stage_rates(stage_id: str, matrix: pd.DataFrame) -> dict[str, float]:
    """Get drop data for given stage

    `{ stageId : rate }`"""

    assert matrix is not None, "Matrix not initialized"

    filtered_matrix = matrix[matrix["stageId"] == stage_id]
    output: dict[str, float] = {}
    for _, row in filtered_matrix.iterrows():
        output[row["itemId"]] = row["quantity"] / row["times"]

    return output
