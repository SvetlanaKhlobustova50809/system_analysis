import csv
import math
from io import StringIO

def calculate_entropy(matrix):
    n = len(matrix)
    if n <= 1:
        return 0.0
    k = len(matrix[0])

    total_entropy = 0.0
    for j in range(n):
        for i in range(k):
            lij = matrix[j][i]
            if lij > 0: 
                probability = lij / (n - 1)
                total_entropy -= probability * math.log2(probability)

    return round(total_entropy, 1)


def parse_csv_matrix(csv_string):
    matrix = []
    csv_reader = csv.reader(StringIO(csv_string), delimiter='\t')
    for row in csv_reader:
        matrix.append(list(map(int, row)))
    return matrix


def task(csv_string):
    matrix = parse_csv_matrix(csv_string)
    entropy = calculate_entropy(matrix)
    return entropy


csv_input = """2\t0\t2\t0\t0
0\t1\t0\t0\t1
2\t1\t0\t0\t1
0\t1\t0\t1\t1
0\t1\t0\t1\t1"""

result = task(csv_input)
print(result)
