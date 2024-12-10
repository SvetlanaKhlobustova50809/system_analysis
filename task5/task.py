import json
import numpy as np


def build_relation_matrix(ranking):
    n = sum(len(block) if isinstance(block, list) else 1 for block in ranking)
    matrix = np.zeros((n, n), dtype=int)
    
    current_index = 0
    for block in ranking:
        if isinstance(block, list):
            for i in block:
                for j in range(current_index + 1, n):
                    matrix[i - 1][j] = 1  # i левее j
            current_index += len(block)
        else:
            for j in range(current_index + 1, n):
                matrix[block - 1][j] = 1  # block левее j
            current_index += 1
    return matrix

def find_core_conflicts(ranking_a, ranking_b):
    ya = build_relation_matrix(ranking_a)
    yb = build_relation_matrix(ranking_b)

    ya_t = ya.T
    yb_t = yb.T

    yab = np.logical_and(ya, yb)
    yab_t = np.logical_and(ya_t, yb_t)

    conflicts = []
    n = len(ya)
    for i in range(n):
        for j in range(i + 1, n):
            if yab[i][j] == 0 and yab_t[i][j] == 0:
                conflicts.append((i + 1, j + 1))

    return conflicts

def main(json_ranking_a, json_ranking_b):
    ranking_a = json.loads(json_ranking_a)
    ranking_b = json.loads(json_ranking_b)

    core_conflicts = find_core_conflicts(ranking_a, ranking_b)

    return json.dumps(core_conflicts, ensure_ascii=False)


if __name__ == "__main__":
    ranking_a = json.dumps([1, [2, 3], 4, [5, 6, 7], 8, 9, 10])
    ranking_b = json.dumps([[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]])

    result = main(ranking_a, ranking_b)
    print(result)
