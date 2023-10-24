import main


STAGES = [
    (4, "tough_12-03", 21),
    (5, "tough_12-04", 21),
    (6, "tough_12-05", 21),
    (7, "tough_12-06", 24),
    (8, "tough_12-07", 21),
    (10, "tough_12-09", 21),
    (12, "tough_12-10", 21),
    (13, "tough_12-11", 24),
    (14, "tough_12-12", 21),
    (17, "tough_12-15", 21),
    (18, "tough_12-16", 21),
    (19, "tough_12-17", 24),
    (20, "tough_12-18", 24),
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
