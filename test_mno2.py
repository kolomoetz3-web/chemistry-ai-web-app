#!/usr/bin/env python3
"""
Тест реакции MnO2 + HCl
"""

from simple_neural_chemistry import SimpleNeuralChemistry

def test_mno2_reaction():
    """Тестирование реакции MnO2 + HCl"""
    ai = SimpleNeuralChemistry()

    test_reactions = [
        "MnO2 + HCl",
        "MnO2+HCl",
        "KMnO4 + HCl",
        "K2Cr2O7 + HCl"
    ]

    print("🧪 Тестирование ОВР реакций:")
    print("=" * 40)

    for reaction in test_reactions:
        print(f"📥 Вход: {reaction}")

        # Прямой поиск в базе
        normalized = ai.normalize_formula(reaction)
        if normalized in ai.knowledge_base:
            result = ai.knowledge_base[normalized]
            print(f"📚 Найдено в базе: {result}")
        else:
            print("📚 Не найдено в базе, анализ по паттернам...")

        # Предсказание через ИИ
        prediction = ai.predict_reaction(reaction)
        if prediction:
            print(f"🤖 ИИ предсказал: {prediction}")
            print("✅ УСПЕХ")
        else:
            print("❌ Не удалось предсказать")
        print("-" * 30)

if __name__ == "__main__":
    test_mno2_reaction()