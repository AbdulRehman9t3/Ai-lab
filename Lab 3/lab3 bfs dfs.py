
from collections import deque

# Original graph 
ORIGINAL_GRAPH = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": []
}


# Breadth First Search
def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = {start}
    visit_order = []
    trace = []

    while queue:
        node, path = queue.popleft()
        visit_order.append(node)

        if node == goal:
            trace.append((node, path, [item[0] for item in queue]))
            return path, visit_order, trace

        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, path + [neighbour]))

        trace.append((node, path, [item[0] for item in queue]))

    return None, visit_order, trace


# Depth First Search
def dfs(graph, start, goal):
    stack = [(start, [start])]
    visited = set()
    visit_order = []
    trace = []

    while stack:
        node, path = stack.pop()

        if node in visited:
            continue

        visited.add(node)
        visit_order.append(node)

        if node == goal:
            trace.append((node, path, [item[0] for item in stack]))
            return path, visit_order, trace

        for neighbour in reversed(graph.get(node, [])):
            if neighbour not in visited:
                stack.append((neighbour, path + [neighbour]))

        trace.append((node, path, [item[0] for item in stack]))

    return None, visit_order, trace


# Display the search trace
def print_trace(title, path, visit_order, trace, frontier_name):
    print("=== " + title + " ===")
    print("Step | Processed | Path to Node       | " + frontier_name)
    print("-" * 78)

    for step, (node, path_to_node, frontier) in enumerate(trace, 1):
        print(f"{step:4} | {node:9} | {str(path_to_node):18} | {frontier}")

    if path is None:
        hops = "N/A"
    else:
        hops = len(path) - 1

    print("Returned Path:", path, "| Hops:", hops)
    print("Visit Order:", visit_order)
    print("Total Processed:", len(visit_order))
    print()


# Run BFS, DFS and edge-case tests
def run_all():

    # BFS test
    bfs_path, bfs_order, bfs_trace = bfs(ORIGINAL_GRAPH, "A", "G")

    print_trace(
        "TASK 1A: BFS TRACE",
        bfs_path,
        bfs_order,
        bfs_trace,
        "Queue (front to back)"
    )

    # DFS test
    dfs_path, dfs_order, dfs_trace = dfs(ORIGINAL_GRAPH, "A", "G")

    print_trace(
        "TASK 1B: DFS TRACE",
        dfs_path,
        dfs_order,
        dfs_trace,
        "Stack (bottom to top)"
    )

    # Edge Case 1
    print("=== EDGE-CASE TESTS ===")

    bfs_path, bfs_order, _ = bfs(ORIGINAL_GRAPH, "A", "A")
    dfs_path, dfs_order, _ = dfs(ORIGINAL_GRAPH, "A", "A")

    print("1. Start equals Goal (A -> A)")
    print("BFS:", bfs_path, "| Visited:", bfs_order)
    print("DFS:", dfs_path, "| Visited:", dfs_order)

    # Edge Case 2
    bfs_path, bfs_order, _ = bfs(ORIGINAL_GRAPH, "A", "Z")
    dfs_path, dfs_order, _ = dfs(ORIGINAL_GRAPH, "A", "Z")

    print("2. Unreachable Goal (A -> Z)")
    print("BFS:", bfs_path, "| Visited:", bfs_order)
    print("DFS:", dfs_path, "| Visited:", dfs_order)

    # Edge Case 3
    cyclic_graph = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["B"],
        "D": ["G"],
        "G": []
    }

    bfs_path, bfs_order, _ = bfs(cyclic_graph, "A", "G")
    dfs_path, dfs_order, _ = dfs(cyclic_graph, "A", "G")

    print("3. Cyclic Graph")
    print("BFS:", bfs_path, "| Visited:", bfs_order)
    print("DFS:", dfs_path, "| Visited:", dfs_order)


if __name__ == "__main__":
    run_all()
