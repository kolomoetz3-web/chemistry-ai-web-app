#!/usr/bin/env python3
"""
Быстрый тест реакции MnO2 + HCl
"""

from simple_neural_chemistry import SimpleNeuralChemistry

# Создаем экземпляр ИИ
ai = SimpleNeuralChemistry()

# Тестируем реакцию
test_input = "MnO2 + HCl"
print(f"Тестируем: {test_input}")

# Нормализуем
normalized = ai.normalize_formula(test_input)
print(f"Нормализованная: {normalized}")

# Ищем в базе
if normalized in ai.knowledge_base:
    result = ai.knowledge_base[normalized]
    print(f"Найдено в базе: {result}")
else:
    print("Не найдено в базе")

# Предсказываем
prediction = ai.predict_reaction(test_input)
print(f"Предсказание ИИ: {prediction}")

# Проверяем паттерн
is_redox = ai._is_redox_reaction(test_input)
print(f"Распознано как ОВР: {is_redox}")

if is_redox:
    redox_result = ai.predict_redox_reaction(test_input)
    print(f"ОВР предсказание: {redox_result}")