
def symbolic(score, complete):
    if complete and score >= 70:
        return "Review"
    else:
        return "Hold"


def threshold(probability):
    if probability >= 0.70:
        return "Review"
    else:
        return "Hold"


cases = [
    ("complete_high", 82, True, 0.81),
    ("complete_low", 68, True, 0.74),
    ("incomplete_high", 91, False, 0.88),
    ("boundary", 70, True, 0.70)
]


print("Scholarship Screening Comparison")
print("case | symbolic | threshold | disagreement")

for name, score, complete, probability in cases:

    rule_result = symbolic(score, complete)
    prob_result = threshold(probability)

    difference = rule_result != prob_result

    print(name, rule_result, prob_result, difference, sep=" | ")
