import main


STAGES = [
    (4, "main_12-03", 21),
    (5, "main_12-04", 21),
    (6, "main_12-05", 21),
    (7, "main_12_06", 21),
    (8, "main_12_07", 21),
    (10, "main_12-09", 21),
    (12, "main_12-10", 21),
    (13, "main_12-11", 24),
    (14, "main_12-12", 21),
    (17, "main_12-15", 21),
    (18, "main_12-16", 21),
    (19, "main_12-17", 24),
    (20, "main_12-18", 24),
]

results = []
for stage in STAGES:
    print("running w/ stage", stage[0])
    result = main.main(["lmao", stage[1], str(stage[2])])
    results.append((stage[0], result[0], result[1]))

print()
print("stage_num, efficiency, main_drop")
for result in results:
    print(f"{result[0]}, {result[1]}, {result[2]}")
