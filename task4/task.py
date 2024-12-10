import math
from collections import Counter

def calculate_entropy(probabilities):
    entropy = 0
    for p in probabilities:
        if p > 0:
            entropy -= p * math.log2(p)
    return round(entropy, 2)


def calculate_joint_entropy(joint_distribution):
    """Вычисляет совместную энтропию H(AB)."""
    flat_probs = [p for row in joint_distribution for p in row]
    return calculate_entropy(flat_probs)


def calculate_conditional_entropy(joint_distribution, marginal_prob_A):
    """Вычисляет условную энтропию H_A(B)."""
    conditional_entropy = 0
    for i, row in enumerate(joint_distribution):
        row_prob_sum = marginal_prob_A[i]
        if row_prob_sum > 0:
            row_entropy = calculate_entropy([p / row_prob_sum for p in row if p > 0])
            conditional_entropy += row_prob_sum * row_entropy
    return round(conditional_entropy, 2)


def calculate_mutual_information(h_a, h_b, h_a_b):
    """Вычисляет информацию I(A, B) = H(B) - H_A(B)."""
    return round(h_b - h_a_b, 2)


def get_distributions():
    outcomes = [(i, j) for i in range(1, 7) for j in range(1, 7)]
    
    # Событие A (сумма)
    sums = [i + j for i, j in outcomes]
    sum_counts = Counter(sums)
    sum_probs = [sum_counts[k] / 36 for k in range(2, 13)]
    
    # Событие B (произведение)
    products = [i * j for i, j in outcomes]
    product_counts = Counter(products)
    unique_products = sorted(set(products))
    product_probs = [product_counts[k] / 36 for k in unique_products]
    
    # Совместное распределение A и B
    joint_distribution = []
    for a in range(2, 13):
        row = []
        for b in unique_products:
            prob = sum(1 for i, j in outcomes if i + j == a and i * j == b) / 36
            row.append(prob)
        joint_distribution.append(row)
    
    return sum_probs, product_probs, joint_distribution


def main():
    marginal_prob_A, marginal_prob_B, joint_distribution = get_distributions()
    
    h_a = calculate_entropy(marginal_prob_A)  # Энтропия H(A)
    h_b = calculate_entropy(marginal_prob_B)  # Энтропия H(B)
    h_ab = calculate_joint_entropy(joint_distribution)  # Энтропия H(AB)
    h_a_b = calculate_conditional_entropy(joint_distribution, marginal_prob_A)  # Условная энтропия H_A(B)
    i_a_b = calculate_mutual_information(h_b, h_a_b)  # Информация I(A, B)

    return [h_ab, h_a, h_b, h_a_b, i_a_b]


result = main()
print(result)
