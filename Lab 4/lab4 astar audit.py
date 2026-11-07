

import heapq


CAMPUS_GRAPH = {
    "S": [("A", 1), ("B", 4)],
    "A": [("C", 2)],
    "B": [("G", 5)],
    "C": [("G", 3)],
    "G": []
}

SUPPLIED_HEURISTIC = {
    "S": 5,
    "A": 4,
    "B": 4,
    "C": 2,
    "G": 0
}

ZERO_HEURISTIC = {
    "S": 0,
    "A": 0,
    "B": 0,
    "C": 0,
    "G": 0
}

TRUE_REMAINING_COST = {
    "S": 6,
    "A": 5,
    "B": 5,
    "C": 3,
    "G": 0
}


def calculate_path_cost(graph, path):
    if path is None:
        return None

    total = 0

    for u, v in zip(path, path[1:]):
        edges = dict(graph.get(u, []))
        total += edges[v]

    return total


def priority_search(graph, heuristic, start, goal):
    priority_queue = [
        (heuristic[start], 0, start, [start])
    ]

    best_cost = {start: 0}
    processed_nodes = []
    expanded_nodes = []
    expansion_trace = []

    while priority_queue:
        f, g, node, path = heapq.heappop(priority_queue)

        if g != best_cost.get(node):
            continue

        processed_nodes.append(node)

        if node == goal:
            frontier = sorted(priority_queue)
            expansion_trace.append({
                "step": len(processed_nodes),
                "node": node,
                "g": g,
                "h": heuristic[node],
                "f": f,
                "path": path,
                "frontier": frontier
            })

            return {
                "path": path,
                "cost": g,
                "independent_cost": calculate_path_cost(graph, path),
                "processed_nodes": processed_nodes,
                "expanded_nodes": expanded_nodes,
                "expansion_count": len(expanded_nodes),
                "expansion_trace": expansion_trace
            }

        expanded_nodes.append(node)

        for nxt, weight in graph.get(node, []):
            new_cost = g + weight

            if new_cost < best_cost.get(nxt, float("inf")):
                best_cost[nxt] = new_cost
                new_f = new_cost + heuristic[nxt]

                heapq.heappush(
                    priority_queue,
                    (new_f, new_cost, nxt, path + [nxt])
                )

        expansion_trace.append({
            "step": len(processed_nodes),
            "node": node,
            "g": g,
            "h": heuristic[node],
            "f": f,
            "path": path,
            "frontier": sorted(priority_queue)
        })

    return {
        "path": None,
        "cost": None,
        "independent_cost": None,
        "processed_nodes": processed_nodes,
        "expanded_nodes": expanded_nodes,
        "expansion_count": len(expanded_nodes),
        "expansion_trace": expansion_trace
    }


def audit_heuristic(graph, heuristic, true_cost):
    print("\nHEURISTIC AUDIT")
    print("-" * 65)

    print("Admissibility Check")
    print("Node | h(n) | True Cost | Admissible")

    all_admissible = True

    for node in graph:
        result = heuristic[node] <= true_cost[node]
        all_admissible = all_admissible and result

        print(
            f"{node:4} | {heuristic[node]:4} | "
            f"{true_cost[node]:9} | {result}"
        )

    print("\nConsistency Check")
    print("Edge | Cost | h(u) | Cost + h(v) | Consistent")

    all_consistent = True

    for u, edges in graph.items():
        for v, weight in edges:
            rhs = weight + heuristic[v]
            result = heuristic[u] <= rhs
            all_consistent = all_consistent and result

            print(
                f"{u}->{v:3} | {weight:4} | "
                f"{heuristic[u]:4} | {rhs:11} | {result}"
            )

    print("\nAdmissible:", all_admissible)
    print("Consistent:", all_consistent)


def print_trace(title, result):
    print("\n" + title)
    print("-" * 100)

    print("Step | Node | g(n) | h(n) | f(n) | Path | Frontier")

    for entry in result["expansion_trace"]:
        print(
            f"{entry['step']:4} | "
            f"{entry['node']:4} | "
            f"{entry['g']:4} | "
            f"{entry['h']:4} | "
            f"{entry['f']:4} | "
            f"{str(entry['path']):18} | "
            f"{entry['frontier']}"
        )

    print("\nReturned Path:", result["path"])
    print("Reported Cost:", result["cost"])
    print("Verified Cost:", result["independent_cost"])
    print("Processed Nodes:", result["processed_nodes"])
    print("Expanded Nodes:", result["expanded_nodes"])
    print("Expansion Count:", result["expansion_count"])


def run_experiments():
    print("TASK 1: SUPPLIED HEURISTIC AUDIT")

    audit_heuristic(
        CAMPUS_GRAPH,
        SUPPLIED_HEURISTIC,
        TRUE_REMAINING_COST
    )

    astar_result = priority_search(
        CAMPUS_GRAPH,
        SUPPLIED_HEURISTIC,
        "S",
        "G"
    )

    print_trace(
        "TASK 1: A* SEARCH TRACE",
        astar_result
    )

    print("\nTASK 2: A* VS UCS COMPARISON")

    ucs_result = priority_search(
        CAMPUS_GRAPH,
        ZERO_HEURISTIC,
        "S",
        "G"
    )

    print_trace(
        "UCS CONTROL TRACE",
        ucs_result
    )

    print("\nCOMPARISON SUMMARY")
    print("-" * 75)
    print("Algorithm | Path              | Cost | Expanded Nodes | Count")

    print(
        f"A*        | {str(astar_result['path']):17} | "
        f"{astar_result['cost']:4} | "
        f"{str(astar_result['expanded_nodes']):14} | "
        f"{astar_result['expansion_count']}"
    )

    print(
        f"UCS       | {str(ucs_result['path']):17} | "
        f"{ucs_result['cost']:4} | "
        f"{str(ucs_result['expanded_nodes']):14} | "
        f"{ucs_result['expansion_count']}"
    )

    print("\nTASK 3: OVERESTIMATING HEURISTIC")

    overestimated_heuristic = dict(SUPPLIED_HEURISTIC)
    overestimated_heuristic["C"] = 10

    audit_heuristic(
        CAMPUS_GRAPH,
        overestimated_heuristic,
        TRUE_REMAINING_COST
    )

    over_result = priority_search(
        CAMPUS_GRAPH,
        overestimated_heuristic,
        "S",
        "G"
    )

    print_trace(
        "A* TRACE WITH h(C) = 10",
        over_result
    )

    print("\nFINAL COMPARISON")
    print("-" * 85)
    print("Search             | Path              | Cost | Expanded Count")

    results = [
        ("A* Supplied", astar_result),
        ("UCS Control", ucs_result),
        ("A* Overestimate", over_result)
    ]

    for name, result in results:
        print(
            f"{name:18} | "
            f"{str(result['path']):17} | "
            f"{str(result['cost']):4} | "
            f"{result['expansion_count']}"
        )

    print("\nADDITIONAL EDGE CASES")

    same_result = priority_search(
        CAMPUS_GRAPH,
        SUPPLIED_HEURISTIC,
        "S",
        "S"
    )

    print("\n1. Start equals Goal")
    print("Path:", same_result["path"])
    print("Cost:", same_result["cost"])
    print("Processed:", same_result["processed_nodes"])
    print("Expanded:", same_result["expanded_nodes"])

    unreachable_graph = dict(CAMPUS_GRAPH)
    unreachable_graph["Z"] = []

    unreachable_heuristic = dict(SUPPLIED_HEURISTIC)
    unreachable_heuristic["Z"] = 0

    unreachable_result = priority_search(
        unreachable_graph,
        unreachable_heuristic,
        "S",
        "Z"
    )

    print("\n2. Unreachable Goal")
    print("Path:", unreachable_result["path"])
    print("Cost:", unreachable_result["cost"])
    print("Processed:", unreachable_result["processed_nodes"])
    print("Expanded:", unreachable_result["expanded_nodes"])


if __name__ == "__main__":
    run_experiments()
