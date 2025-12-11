#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы нейронной сети
"""

try:
    from neural_chemistry import NeuralChemistryPredictor, TENSORFLOW_AVAILABLE
    print("✅ Импорт NeuralChemistryPredictor прошел успешно")

    # Создаем экземпляр
    predictor = NeuralChemistryPredictor()
    print("✅ Экземпляр NeuralChemistryPredictor создан")

    if TENSORFLOW_AVAILABLE:
        print("✅ TensorFlow доступен")

        # Проверяем создание данных
        reactions = predictor.create_training_data()
        print(f"✅ Создано {len(reactions)} обучающих примеров")

        # Проверяем токенизацию
        test_formula = "H2 + O2"
        tokens = predictor.tokenize_formula(test_formula)
        print(f"✅ Токенизация '{test_formula}' -> '{tokens}'")

        print("\n🎉 Все базовые функции работают корректно!")
        print("🤖 Нейронная сеть готова к использованию в Telegram боте")
    else:
        print("⚠️ TensorFlow недоступен")
        print("🔄 Бот будет работать с правиловым алгоритмом")

        # Проверяем базовую функциональность
        reactions = predictor.create_training_data()
        print(f"✅ Создано {len(reactions)} обучающих примеров")

        test_formula = "H2 + O2"
        tokens = predictor.tokenize_formula(test_formula)
        print(f"✅ Токенизация '{test_formula}' -> '{tokens}'")

        print("\n🎉 Базовые функции работают корректно!")
        print("🤖 Бот готов к работе с правиловым алгоритмом")

except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Убедитесь, что установлены базовые зависимости")

except Exception as e:
    print(f"❌ Ошибка выполнения: {e}")