#!/usr/bin/env python3
"""
Мини-приложение для демонстрации нейронной сети в химии
Простое консольное приложение с ИИ для предсказания реакций
"""

from simple_neural_chemistry import SimpleNeuralChemistry
import sys

class MiniChemistryApp:
    """Мини-приложение для химии с ИИ"""

    def __init__(self):
        self.predictor = SimpleNeuralChemistry()
        print("🧪 МИНИ-ПРИЛОЖЕНИЕ ХИМИИ С ИИ 🤖")
        print("=" * 50)

    def show_menu(self):
        """Показать меню"""
        print("\n📋 МЕНЮ:")
        print("1. 🧪 Предсказать реакцию")
        print("2. 📚 Информация о нейронной сети")
        print("3. 🧪 Примеры реакций")
        print("4. ❌ Выход")
        print("-" * 30)

    def predict_reaction_interactive(self):
        """Интерактивное предсказание реакции"""
        print("\n🧪 ПРЕДСКАЗАНИЕ РЕАКЦИИ")
        print("Введите реагенты через '+' (например: Zn + HCl)")

        while True:
            try:
                reactants = input("\nВведите реагенты (или 'назад' для возврата): ").strip()

                if reactants.lower() in ['назад', 'back', 'exit']:
                    break

                if not reactants:
                    print("❌ Введите реагенты!")
                    continue

                # Предсказываем реакцию
                prediction = self.predictor.predict_reaction(reactants)

                if prediction:
                    print(f"\n✅ Найдена реакция!")
                    print(f"📥 Реагенты: {reactants}")
                    print(f"📤 Продукты: {prediction}")

                    # Предлагаем сбалансировать уравнение
                    full_equation = f"{reactants} -> {prediction}"
                    print(f"📊 Полное уравнение: {full_equation}")

                else:
                    print(f"\n❌ Реакция не найдена: {reactants}")
                    print("💡 Попробуйте другой пример или проверьте формулы")

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")

    def show_examples(self):
        """Показать примеры реакций"""
        print("\n🧪 ПРИМЕРЫ РЕАКЦИЙ")
        print("=" * 40)

        examples = [
            ("Zn + HCl", "ZnCl2 + H2", "Металл + кислота"),
            ("CH4 + O2", "CO2 + H2O", "Горение"),
            ("Na + O2", "Na2O", "Металл + кислород"),
            ("HCl + NaOH", "NaCl + H2O", "Кислота + основание"),
            ("CaCO3", "CaO + CO2", "Разложение"),
            ("Fe + CuSO4", "FeSO4 + Cu", "Вытеснение"),
        ]

        for i, (reactants, products, reaction_type) in enumerate(examples, 1):
            print(f"{i}. {reactants} → {products}")
            print(f"   Тип: {reaction_type}")
            print()

        print("💡 Попробуйте ввести эти реакции в предсказателе!")

    def show_neural_info(self):
        """Показать информацию о нейронной сети"""
        print("\n🤖 ИНФОРМАЦИЯ О НЕЙРОННОЙ СЕТИ")
        print(self.predictor.get_info())

    def run(self):
        """Запуск приложения"""
        while True:
            self.show_menu()

            try:
                choice = input("Выберите действие (1-4): ").strip()

                if choice == '1':
                    self.predict_reaction_interactive()
                elif choice == '2':
                    self.show_neural_info()
                    input("\nНажмите Enter для продолжения...")
                elif choice == '3':
                    self.show_examples()
                    input("\nНажмите Enter для продолжения...")
                elif choice == '4':
                    print("\n👋 До свидания! Спасибо за использование мини-приложения!")
                    break
                else:
                    print("❌ Неверный выбор. Выберите 1-4.")

            except KeyboardInterrupt:
                print("\n\n👋 Приложение завершено!")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")

def main():
    """Главная функция"""
    try:
        app = MiniChemistryApp()
        app.run()
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()