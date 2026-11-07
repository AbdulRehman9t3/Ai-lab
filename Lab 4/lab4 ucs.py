
import heapq


CAMPUS_GRAPH = {
    "S": [("A", 1), ("B", 4)],
    "A": [("C", 2)],
    "B": [("G", 5)],
    "C": [("G", 3)],
    "G": []
}


ZERO_HEURISTIC = {
    "S": 0,
    "A": 0,
    "B": 0,
    "C": 0,
    "G": 0
}


def sum_path_cost(graph, path):
    if path is None:
        return None

    total = 0

    for u, v in zip(path, path[1:]):
        edges = dict(graph.get(u, []))
        total += edges[v]

    return total


def priority_search(graph, h, start, goal):
    pq = [(h[start], 0, start, [start])]
    best = {start: 0}

    processed_nodes = []
    expanded_nodes = []
    stale_skipped = []
    expansion_trace = []

    while pq:
        f, g, node, path = heapq.heappop(pq)

        if g != best.get(node):
            stale_skipped.append((f, g, node, path))
            continue

        processed_nodes.append(node)

        if node == goal:
            return {
                "path": path,
                "cost": g,
                "independent_cost": sum_path_cost(graph, path),
                "processed_nodes": processed_nodes,
                "expanded_nodes": expanded_nodes,
                "expansion_count": len(expanded_nodes),
                "stale_skipped": stale_skipped,
                "expansion_trace": expansion_trace
            }

        expanded_nodes.append(node)

        for nxt, weight in graph.get(node, []):
            new_cost = g + weight

            if new_cost < best.get(nxt, float("inf")):
                best[nxt] = new_cost

                new_f = new_cost + h[nxt]

                heapq.heappush(
                    pq,
                    (new_f, new_cost, nxt, path + [nxt])
                )

        frontier = sorted(pq)

        expansion_trace.append({
            "step": len(expanded_nodes),
            "node": node,
            "g": g,
            "h": h[node],
            "f": f,
            "path": path,
            "frontier": frontier
        })

    return {
        "path": None,
        "cost": None,
        "independent_cost": None,
        "processed_nodes": processed_nodes,
        "expanded_nodes": expanded_nodes,
        "expansion_count": len(expanded_nodes),
        "stale_skipped": stale_skipped,
        "expansion_trace": expansion_trace
    }


def ucs_control(graph, start, goal):
    zero_h = {node: 0 for node in graph}
    return priority_search(graph, zero_h, start, goal)


def run_experiment():
    print("TASK: ZERO-HEURISTIC UCS CONTROL")
    print("-" * 65)

    result = ucs_control(CAMPUS_GRAPH, "S", "G")

    print("Returned Path:", result["path"])
    print("Reported Cost:", result["cost"])
    print("Verified Cost:", result["independent_cost"])
    print("Processed Nodes:", result["processed_nodes"])
    print("Expanded Nodes:", result["expanded_nodes"])
    print("Expansion Count:", result["expansion_count"])
    print("Stale Entries Skipped:", result["stale_skipped"])

    print("\nUCS SEARCH TRACE")
    print("-" * 85)
    print("Step | Node | g(n) | h(n) | f(n) | Remaining Frontier")

    for entry in result["expansion_trace"]:
        print(
            f"{entry['step']:4} | "
            f"{entry['node']:4} | "
            f"{entry['g']:4} | "
            f"{entry['h']:4} | "
            f"{entry['f']:4} | "
            f"{entry['frontier']}"
        )

    print("\nEDGE CASE: STALE QUEUE ENTRY")
    print("-" * 65)

    stale_graph = {
        "S": [("A", 1), ("B", 10)],
        "A": [("B", 2)],
        "B": [("G", 10)],
        "G": []
    }

    stale_result = ucs_control(stale_graph, "S", "G")

    print("Returned Path:", stale_result["path"])
    print("Reported Cost:", stale_result["cost"])
    print("Verified Cost:", stale_result["independent_cost"])
    print("Processed Nodes:", stale_result["processed_nodes"])
    print("Expanded Nodes:", stale_result["expanded_nodes"])
    print("Expansion Count:", stale_result["expansion_count"])
    print("Stale Entries Ignored:", stale_result["stale_skipped"])


if __name__ == "__main__":
    run_experiment()
