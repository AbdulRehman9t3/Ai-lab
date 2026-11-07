import math

count = 0


def minimax(depth, index, max_turn, scores, target):
    global count
    if depth == target:
        count += 1
        return scores[index]
    vals = [minimax(depth + 1, index * 2 + i, not max_turn, scores, target) for i in range(2)]
    return max(vals) if max_turn else min(vals)


def alphabeta(depth, index, max_turn, scores, target, alpha, beta):
    global count
    if depth == target:
        count += 1
        return scores[index]
    if max_turn:
        value = float('-inf')
        for i in range(2):
            value = max(value, alphabeta(depth + 1, index * 2 + i, False, scores, target, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    value = float('inf')
    for i in range(2):
        value = min(value, alphabeta(depth + 1, index * 2 + i, True, scores, target, alpha, beta))
        beta = min(beta, value)
        if alpha >= beta:
            break
    return value


scores = [3, 5, 2, 9, 3, 5, 2, 9]
depth = int(math.log2(len(scores)))

count = 0
mm = minimax(0, 0, True, scores, depth)
mm_leaves = count

count = 0
ab = alphabeta(0, 0, True, scores, depth, float('-inf'), float('inf'))
ab_leaves = count

print("Minimax:    value =", mm, " leaves evaluated =", mm_leaves)
print("Alpha-beta: value =", ab, " leaves evaluated =", ab_leaves)
