
# Lab 1 - Scholarship Screening System
# Symbolic and Probability-Based Comparison


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


# Test cases provided in the lab manual

cases = [
    ("complete_high", 82, True, 0.81),
    ("complete_low", 68, True, 0.74),
    ("incomplete_high", 91, False, 0.88),
    ("boundary", 70, True, 0.70)
]


print("SCHOLARSHIP SCREENING SYSTEM")
print("-" * 65)
print("Case | Symbolic | Probability | Disagreement")
print("-" * 65)


for name, score, complete, probability in cases:

    rule_result = symbolic(score, complete)
    prob_result = threshold(probability)

    disagreement = rule_result != prob_result

    print(name, rule_result, prob_result, disagreement, sep=" | ")


# Additional edge-case testing

print("\nADDITIONAL EDGE CASE TESTING")
print("-" * 40)

# Test 1: Change the score from 70 to 69

score_result = symbolic(69, True)
print("Score changed to 69:", score_result)

# Test 2: Change the probability from 0.70 to 0.69

prob_result = threshold(0.69)
print("Probability changed to 0.69:", prob_result)

# Test 3: Incomplete documents with a high score

rule_result = symbolic(95, False)
prob_result = threshold(0.91)

print("\nIncomplete Application Test")
print("Symbolic Result:", rule_result)
print("Probability Result:", prob_result)
print("Disagreement:", rule_result != prob_result)
