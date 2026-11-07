


from collections import deque
import heapq


WEIGHTED_GRAPH = {
    "A": [("B", 1), ("C", 2)],
    "B": [("D", 2), ("E", 1)],
    "C": [("F", 3), ("G", 10)],
    "D": [],
    "E": [("G", 1)],
    "F": [],
    "G": []
}


def sum_path_cost(graph, path):
    if path is None:
        return None

    total = 0

    for u, v in zip(path, path[1:]):
        edges = dict(graph.get(u, []))
        total += edges[v]

    return total


def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = {start}
    processing_order = []

    while queue:
        node, path = queue.popleft()
        processing_order.append(node)

        if node == goal:
            return path, processing_order

        for nxt, weight in graph.get(node, []):
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [nxt]))

    return None, processing_order


def ucs(graph, start, goal):
    priority_queue = [(0, start, [start])]
    best_cost = {start: 0}
    processing_order = []
    trace = []

    while priority_queue:
        cost, node, path = heapq.heappop(priority_queue)

        if cost != best_cost.get(node):
            continue

        processing_order.append(node)

        if node == goal:
            frontier = sorted(
                (c, n) for c, n, p in priority_queue
            )
            trace.append((node, cost, path, frontier))
            return cost, path, processing_order, trace

        for nxt, weight in graph.get(node, []):
            new_cost = cost + weight

            if new_cost < best_cost.get(nxt, float("inf")):
                best_cost[nxt] = new_cost
                heapq.heappush(
                    priority_queue,
                    (new_cost, nxt, path + [nxt])
                )

        frontier = sorted(
            (c, n) for c, n, p in priority_queue
        )
        trace.append((node, cost, path, frontier))

    return None, None, processing_order, trace


def run_experiment():
    print("TASK 3: EXTENDED WEIGHTED GRAPH")
    print("-" * 55)

    for node, edges in WEIGHTED_GRAPH.items():
        if edges:
            print(node, ":", edges)
        else:
            print(node, ": No outgoing edges")

    print("\nUCS STEP-BY-STEP TRACE")
    print("-" * 80)
    print("Step | Processed | Cost | Path                 | Priority Queue")

    ucs_cost, ucs_path, ucs_order, trace = ucs(
        WEIGHTED_GRAPH, "A", "G"
    )

    for step, (node, cost, path, frontier) in enumerate(trace, 1):
        print(
            f"{step:4} | {node:9} | {cost:4} | "
            f"{str(path):20} | {frontier}"
        )

    bfs_path, bfs_order = bfs(WEIGHTED_GRAPH, "A", "G")

    bfs_cost = sum_path_cost(WEIGHTED_GRAPH, bfs_path)
    verified_ucs_cost = sum_path_cost(WEIGHTED_GRAPH, ucs_path)

    print("\nBFS AND UCS COMPARISON")
    print("-" * 80)

    print("Algorithm | Path                 | Hops | Path Cost | Processing Order")
    print("-" * 80)

    print(
        f"BFS       | {str(bfs_path):20} | "
        f"{len(bfs_path) - 1:4} | {bfs_cost:9} | {bfs_order}"
    )

    print(
        f"UCS       | {str(ucs_path):20} | "
        f"{len(ucs_path) - 1:4} | {ucs_cost:9} | {ucs_order}"
    )

    print("\nUCS COST VERIFICATION")
    print("Reported UCS Cost:", ucs_cost)
    print("Independently Calculated Cost:", verified_ucs_cost)

    print("\nSECTION 3.8: EDGE CASE TESTS")
    print("-" * 65)

    cost, path, order, trace = ucs(WEIGHTED_GRAPH, "A", "A")
    print("1. Start equals Goal:")
    print("Status: FOUND")
    print("Path:", path, "| Cost:", cost, "| Processed:", order)

    cost, path, order, trace = ucs(WEIGHTED_GRAPH, "A", "Z")
    print("\n2. Unreachable Goal:")
    print("Status: FAILURE")
    print("Path:", path, "| Cost:", cost, "| Processed:", order)

    cyclic_graph = {
        "A": [("B", 2), ("C", 5)],
        "B": [("A", 1), ("C", 1)],
        "C": [("A", 2), ("G", 2)],
        "G": []
    }

    cost, path, order, trace = ucs(cyclic_graph, "A", "G")

    print("\n3. Cyclic Weighted Graph:")
    print("Path:", path)
    print("Cost:", cost)
    print("Verified Cost:", sum_path_cost(cyclic_graph, path))
    print("Processing Order:", order)


if __name__ == "__main__":
    run_experiment()
