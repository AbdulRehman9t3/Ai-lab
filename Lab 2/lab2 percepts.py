
class ClassroomAgent:

    def act(self, temp, occupied):

        # Save energy when the classroom is empty
        if not occupied:
            return "ECO"

        # Check classroom temperature
        elif temp > 26:
            return "COOL"

        elif temp < 20:
            return "WARM"

        else:
            return "IDLE"


def run_test():

    agent = ClassroomAgent()

    # Temperature and occupancy readings
    percepts = [
        (29, True),
        (29, True),
        (20, True),
        (26, True),
        (19, True),
        (29, False)
    ]

    print("SIMPLE REFLEX CLASSROOM AGENT")
    print("-" * 40)
    print("Step | Percept | Target Mode")
    print("-" * 40)

    for step, percept in enumerate(percepts, 1):

        temp, occupied = percept

        mode = agent.act(temp, occupied)

        print(
            str(step) + " | " +
            str(percept) + " | " +
            mode
        )


if __name__ == "__main__":
    run_test()
