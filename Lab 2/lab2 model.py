
class StatefulClassroomAgent:

    def __init__(self):
        self.previous_mode = None

    def get_mode(self, temp, occupied):

        if not occupied:
            return "ECO"

        elif temp > 26:
            return "COOL"

        elif temp < 20:
            return "WARM"

        else:
            return "IDLE"

    def act(self, temp, occupied):

        old_mode = self.previous_mode
        new_mode = self.get_mode(temp, occupied)

        if old_mode != new_mode:
            result = "SEND COMMAND"
        else:
            result = "NO COMMAND"

        self.previous_mode = new_mode

        return old_mode, new_mode, result


def run_test():

    agent = StatefulClassroomAgent()

    tests = [
        ((29, True), "High temperature"),
        ((29, True), "Repeated temperature"),
        ((20, True), "Exact lower boundary"),
        ((26, True), "Exact upper boundary"),
        ((19, True), "Low temperature"),
        ((19, True), "Repeated low temperature"),
        ((29, False), "Empty room priority"),
        ((22, False), "Repeated empty room")
    ]

    print("STATEFUL CLASSROOM AGENT")
    print("-" * 75)
    print("Step | Previous | Percept | Target | Result")
    print("-" * 75)

    for step, (percept, description) in enumerate(tests, 1):

        temp, occupied = percept

        old, new, result = agent.act(temp, occupied)

        print(
            str(step) + " | " +
            str(old) + " | " +
            str(percept) + " | " +
            new + " | " +
            result
        )

        print("Test:", description)
        print("-" * 75)


if __name__ == "__main__":
    run_test()
