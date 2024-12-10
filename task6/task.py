import json

def membership(value, points):
    """
    Вычисляет степень принадлежности значения `value` заданной функции принадлежности.
    Функция принадлежности задается как список контрольных точек: [[x1, μ1], [x2, μ2], ...].
    """
    for i in range(len(points) - 1):
        x1, μ1 = points[i]
        x2, μ2 = points[i + 1]
        if x1 <= value <= x2:
            if x1 == x2:
                return max(μ1, μ2)
            return μ1 + (μ2 - μ1) * (value - x1) / (x2 - x1)
    return 0.0

def fuzzification(value, membership_functions):
    """
    Фаззификация: вычисляет степени принадлежности значения `value` всем термам.
    """
    return {term["id"]: membership(value, term["points"]) for term in membership_functions}

def apply_rules(temperature_membership, rules, heating_functions):
    """
    Применяет правила управления и возвращает набор нечетких выводов.
    """
    fuzzy_outputs = []
    for rule in rules:
        temp_term, heat_term = rule
        activation = temperature_membership.get(temp_term, 0.0)
        if activation > 0:
            for heat_func in heating_functions:
                if heat_func["id"] == heat_term:
                    fuzzy_outputs.append({"activation": activation, "points": heat_func["points"]})
    return fuzzy_outputs

def aggregate_fuzzy_outputs(fuzzy_outputs):
    """
    Объединяет все нечеткие выводы в одно нечеткое множество.
    """
    aggregated = {}
    for output in fuzzy_outputs:
        for x, μ in output["points"]:
            aggregated[x] = max(aggregated.get(x, 0.0), output["activation"] * μ)
    return sorted(aggregated.items())

def defuzzify(fuzzy_output):
    """
    Дефаззификация методом первого максимума.
    """
    max_membership = max(μ for _, μ in fuzzy_output)
    for x, μ in fuzzy_output:
        if μ == max_membership:
            return x
    return 0.0

def main(temp_json, heat_json, rules_json, current_temp):
    temp_data = json.loads(temp_json)["температура"]
    heat_data = json.loads(heat_json)["температура"]
    rules = json.loads(rules_json)
    
    # Фаззификация
    temp_membership = fuzzification(current_temp, temp_data)
    
    # Применение правил
    fuzzy_outputs = apply_rules(temp_membership, rules, heat_data)
    
    # Агрегация нечетких выводов
    aggregated_output = aggregate_fuzzy_outputs(fuzzy_outputs)
    
    # Дефаззификация
    optimal_control = defuzzify(aggregated_output)
    
    return optimal_control

temp_json = """
{
  "температура": [
      {
      "id": "холодно",
      "points": [
          [0,1],
          [18,1],
          [22,0],
          [50,0]
      ]
      },
      {
      "id": "комфортно",
      "points": [
          [18,0],
          [22,1],
          [24,1],
          [26,0]
      ]
      },
      {
      "id": "жарко",
      "points": [
          [0,0],
          [24,0],
          [26,1],
          [50,1]
      ]
      }
  ]
}
"""

heat_json = """
{
  "температура": [
      {
        "id": "слабый",
        "points": [
            [0,0],
            [0,1],
            [5,1],
            [8,0]
        ]
      },
      {
        "id": "умеренный",
        "points": [
            [5,0],
            [8,1],
            [13,1],
            [16,0]
        ]
      },
      {
        "id": "интенсивный",
        "points": [
            [13,0],
            [18,1],
            [23,1],
            [26,0]
        ]
      }
  ]
}
"""

rules_json = """
[
    ["холодно", "интенсивный"],
    ["комфортно", "умеренный"],
    ["жарко", "слабый"]
]
"""

current_temp = 20.0

result = main(temp_json, heat_json, rules_json, current_temp)
print(result)
