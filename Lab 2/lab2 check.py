
class ClassroomAgent:

    def act(self, temp, occupied):

        if not occupied:
            return "ECO"

        if temp > 26:
            return "COOL"

        if temp < 20:
            return "WARM"

        return "IDLE"


class StatefulClassroomAgent:

    def __init__(self):
        self.previous_mode = "IDLE"

    def act(self, temp, occupied):

        old_mode = self.previous_mode

        # Decide the required mode
        if not occupied:
            new_mode = "ECO"

        elif temp > 26:
            new_mode = "COOL"

        elif temp < 20:
            new_mode = "WARM"

        else:
            new_mode = "IDLE"

        # Send a command only when the mode changes
        if new_mode != old_mode:
            self.previous_mode = new_mode
            return old_mode, new_mode, True, "Command sent"

        return old_mode, new_mode, False, "No change needed"


def run_tests():

    reflex = ClassroomAgent()
    stateful = StatefulClassroomAgent()

    # Standard classroom test cases
    sequence = [
        (29, True),
        (29, True),
        (20, True),
        (26, True),
        (19, True),
        (29, False)
    ]

    print("REFLEX VS STATEFUL AGENT")
    print("-" * 65)
    print("Step | Percept | Reflex | Previous | Target | Outcome")
    print("-" * 65)

    reflex_count = 0
    stateful_count = 0

    for step, percept in enumerate(sequence, 1):

        temp, occupied = percept

        reflex_result = reflex.act(temp, occupied)

        old, target, sent, outcome = stateful.act(
            temp, occupied
        )

        reflex_count += 1

        if sent:
            stateful_count += 1

        print(
            str(step) + " | " +
            str(percept) + " | " +
            reflex_result + " | " +
            old + " | " +
            target + " | " +
            outcome
        )

    print("\nTOTAL COMMANDS")
    print("Reflex Agent:", reflex_count)
    print("Stateful Agent:", stateful_count)

    # Test sensor noise around 26 degrees
    print("\nNOISY SENSOR TEST")
    print("-" * 55)

    noisy_agent = StatefulClassroomAgent()

    noisy_sequence = [
        (26.1, True),
        (25.9, True),
        (26.2, True),
        (25.8, True),
        (26.1, True)
    ]

    noisy_count = 0

    for step, percept in enumerate(noisy_sequence, 1):

        old, target, sent, outcome = noisy_agent.act(
            percept[0], percept[1]
        )

        if sent:
            noisy_count += 1

        print(
            "Step " + str(step) +
            " | Previous: " + old +
            " | Temperature: " + str(percept[0]) +
            " | Target: " + target +
            " | " + outcome
        )

    print("\nCommands during noisy test:", noisy_count, "/ 5")


if __name__ == "__main__":
    run_tests()
