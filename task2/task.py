import csv
from io import StringIO
from collections import defaultdict, deque
import sys


def parse_csv_edges(path):
    edges = []
    with open(path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            edges.append((int(row[0]), int(row[1])))
        return edges


def build_graph(edges):
    graph = defaultdict(list)
    for parent, child in edges:
        graph[parent].append(child)
    return graph


def calculate_extensional_lengths(graph, nodes):
    result = []

    for node in nodes:
        l1 = len(graph[node])
        l2 = sum(1 for n in graph if node in graph[n])

        visited = set()
        queue = deque(graph[node])
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                queue.extend(graph[current])
        l3 = len(visited) - l1

        visited = set()
        for parent in graph:
            if node in graph[parent]:
                queue = deque([parent])
                while queue:
                    current = queue.popleft()
                    if current not in visited:
                        visited.add(current)
                        queue.extend(n for n in graph if current in graph[n])
        l4 = len(visited) - l2

        l5 = 0
        for parent in graph:
            children = graph[parent]
            if node in children:
                l5 += len(children) - 1

        result.append([l1, l2, l3, l4, l5])

    return result


def main(csv_string):
    edges = parse_csv_edges(csv_string)
    
    graph = build_graph(edges)
    
    nodes = sorted(set(node for edge in edges for node in edge))
    
    extensional_lengths = calculate_extensional_lengths(graph, nodes)
    
    output = StringIO()
    csv_writer = csv.writer(output, delimiter='\t')
    csv_writer.writerows(extensional_lengths)
    return output.getvalue().strip()


if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_csv>")
else:
    csv_input = sys.argv[1]

    result = main(csv_input)
    print(result)
