

ORIGINAL_GRAPH = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": []
}


def dls(graph, start, goal, limit):
    visit_order = []

    def search(node, path, depth):
        visit_order.append(node)

        if node == goal:
            return "FOUND", path

        if depth == limit:
            for nxt in graph.get(node, []):
                if nxt not in path:
                    return "CUTOFF", None
            return "FAILURE", None

        cutoff_found = False

        for nxt in graph.get(node, []):
            if nxt not in path:
                status, result = search(nxt, path + [nxt], depth + 1)

                if status == "FOUND":
                    return "FOUND", result

                if status == "CUTOFF":
                    cutoff_found = True

        if cutoff_found:
            return "CUTOFF", None

        return "FAILURE", None

    status, path = search(start, [start], 0)
    return status, path, visit_order


def iddfs(graph, start, goal, max_depth):
    limits_attempted = []
    visits_by_limit = {}

    for limit in range(max_depth + 1):
        limits_attempted.append(limit)

        status, path, visits = dls(graph, start, goal, limit)
        visits_by_limit[limit] = visits

        if status == "FOUND":
            return status, path, limits_attempted, visits_by_limit

        if status == "FAILURE":
            return status, None, limits_attempted, visits_by_limit

    return status, None, limits_attempted, visits_by_limit


def run_experiments():
    print("TASK 2A: DEPTH-LIMITED SEARCH")
    print("-" * 75)
    print("Limit | Status  | Returned Path       | Visit Order")

    for limit in [1, 2, 3, 4]:
        status, path, visits = dls(ORIGINAL_GRAPH, "A", "G", limit)
        print(f"{limit:5} | {status:7} | {str(path):19} | {visits}")

    print("\nTASK 2B: ITERATIVE DEEPENING DFS")
    print("-" * 75)

    for max_depth in [1, 2, 3, 4]:
        status, path, limits, visits = iddfs(
            ORIGINAL_GRAPH, "A", "G", max_depth
        )

        total = sum(len(order) for order in visits.values())

        print(f"\nMaximum Depth: {max_depth}")
        print(f"Status: {status}")
        print(f"Returned Path: {path}")
        print(f"Limits Attempted: {limits}")
        print(f"Nodes Processed: {total}")
        print(f"Visit Order: {visits}")

    print("\nSECTION 3.8: EDGE CASE TESTS")
    print("-" * 75)

    status, path, visits = dls(ORIGINAL_GRAPH, "A", "A", 1)
    print(f"1. Start equals Goal: {status}, Path: {path}, Visits: {visits}")

    status, path, visits = dls(ORIGINAL_GRAPH, "A", "Z", 2)
    print(f"2. Unreachable Goal, Limit 2: {status}, Path: {path}, Visits: {visits}")

    status, path, visits = dls(ORIGINAL_GRAPH, "A", "Z", 4)
    print(f"3. Unreachable Goal, Limit 4: {status}, Path: {path}, Visits: {visits}")

    cyclic_graph = {
        "A": ["B", "C"],
        "B": ["A", "E"],
        "C": ["A"],
        "E": ["G"],
        "G": []
    }

    status, path, limits, visits = iddfs(cyclic_graph, "A", "G", 3)
    print(f"4. Cyclic Graph: {status}, Path: {path}, Limits: {limits}")


if __name__ == "__main__":
    run_experiments()
