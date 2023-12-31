# PeterYR's Scuffed Stage Efficiency Calculator

## Usage

### Install dependencies

```
pip install -r requirements.txt
```

### Run program

```
main.py <stage_id> <sanity cost> [extra LMD/san]
```

- `<stage_id>`: Game ID of stage to analyze. Easy to check using Penguin Statistics.
- `<sanity cost>`: Sanity cost of stage.
- `[extra LMD/san]`: Extra LMD earned per sanity spent, usually from event shops. Do not include the base 12 LMD/sanity from all stages.

Example: IS-10 (Il Siracusano) costs 21 sanity, with unlimited 20 LMD offer in shop:

```
main.py act21side_10 21 20
```

## Acknowledgements

- Drop rates provided by [Penguin Statistics](https://penguin-stats.io/)
- Game data provided by [Kengxxiao's ArknightsGameData repository](https://github.com/Kengxxiao/ArknightsGameData)
- Sanity values provied by [Moe's Material Farming spreadsheet](https://docs.google.com/spreadsheets/d/12X0uBQaN7MuuMWWDTiUjIni_MOP015GnulggmBJgBaQ)
