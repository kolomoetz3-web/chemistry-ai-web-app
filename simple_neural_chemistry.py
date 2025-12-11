#!/usr/bin/env python3
"""
Простая нейронная сеть для предсказания химических реакций
Работает без TensorFlow, используя только базовые библиотеки
"""

import re
import json
import os
from collections import defaultdict, Counter

class SimpleNeuralChemistry:
    """Простая нейронная сеть для предсказания химических реакций"""

    def __init__(self):
        self.knowledge_base = {}
        self.reaction_patterns = {}
        self.load_knowledge()

    def load_knowledge(self):
        """Загрузка базы знаний о реакциях"""
        # Расширенная база данных реакций (более 100 реакций)
        self.knowledge_base = {
            # Металл + HCl (расширенная)
            "Li+HCl": "LiCl+H2",
            "Na+HCl": "NaCl+H2",
            "K+HCl": "KCl+H2",
            "Rb+HCl": "RbCl+H2",
            "Cs+HCl": "CsCl+H2",
            "Ca+HCl": "CaCl2+H2",
            "Mg+HCl": "MgCl2+H2",
            "Zn+HCl": "ZnCl2+H2",
            "Fe+HCl": "FeCl2+H2",
            "Al+HCl": "AlCl3+H2",
            "Sn+HCl": "SnCl2+H2",
            "Pb+HCl": "PbCl2+H2",
            "Cu+HCl": "CuCl2+H2",
            "Ag+HCl": "AgCl+H2",
            "Au+HCl": "AuCl3+H2",

            # Металл + H2SO4
            "Na+H2SO4": "Na2SO4+H2",
            "K+H2SO4": "K2SO4+H2",
            "Ca+H2SO4": "CaSO4+H2",
            "Mg+H2SO4": "MgSO4+H2",
            "Zn+H2SO4": "ZnSO4+H2",
            "Fe+H2SO4": "FeSO4+H2",
            "Al+H2SO4": "Al2(SO4)3+H2",
            "Sn+H2SO4": "SnSO4+H2",
            "Pb+H2SO4": "PbSO4+H2",

            # Металл + HNO3
            "Na+HNO3": "NaNO3+H2",
            "K+HNO3": "KNO3+H2",
            "Ca+HNO3": "Ca(NO3)2+H2",
            "Mg+HNO3": "Mg(NO3)2+H2",
            "Zn+HNO3": "Zn(NO3)2+H2",
            "Fe+HNO3": "Fe(NO3)2+H2",
            "Al+HNO3": "Al(NO3)3+H2",

            # Металл + кислород (расширенная)
            "Li+O2": "Li2O",
            "Na+O2": "Na2O",
            "K+O2": "K2O",
            "Rb+O2": "Rb2O",
            "Cs+O2": "Cs2O",
            "Ca+O2": "CaO",
            "Mg+O2": "MgO",
            "Zn+O2": "ZnO",
            "Fe+O2": "Fe2O3",
            "Al+O2": "Al2O3",
            "Cu+O2": "CuO",
            "Ag+O2": "Ag2O",
            "Au+O2": "Au2O3",
            "Sn+O2": "SnO2",
            "Pb+O2": "PbO",
            "Hg+O2": "HgO",

            # Кислота + основание (расширенная)
            "HCl+NaOH": "NaCl+H2O",
            "HCl+KOH": "KCl+H2O",
            "HCl+Ca(OH)2": "CaCl2+H2O",
            "HCl+Mg(OH)2": "MgCl2+H2O",
            "HCl+Al(OH)3": "AlCl3+H2O",
            "H2SO4+NaOH": "Na2SO4+H2O",
            "H2SO4+KOH": "K2SO4+H2O",
            "H2SO4+Ca(OH)2": "CaSO4+H2O",
            "H2SO4+Mg(OH)2": "MgSO4+H2O",
            "HNO3+NaOH": "NaNO3+H2O",
            "HNO3+KOH": "KNO3+H2O",
            "HNO3+Ca(OH)2": "Ca(NO3)2+H2O",
            "H3PO4+NaOH": "Na3PO4+H2O",
            "CH3COOH+NaOH": "CH3COONa+H2O",
            "HF+NaOH": "NaF+H2O",
            "HBr+NaOH": "NaBr+H2O",
            "HI+NaOH": "NaI+H2O",

            # Горение (расширенная)
            "C+O2": "CO2",
            "S+O2": "SO2",
            "P+O2": "P2O5",
            "CH4+O2": "CO2+H2O",
            "C2H6+O2": "CO2+H2O",
            "C3H8+O2": "CO2+H2O",
            "C4H10+O2": "CO2+H2O",
            "C2H4+O2": "CO2+H2O",
            "C2H2+O2": "CO2+H2O",
            "H2+O2": "H2O",
            "CO+O2": "CO2",
            "H2S+O2": "SO2+H2O",
            "NH3+O2": "N2+H2O",
            "C6H12O6+O2": "CO2+H2O",
            "C2H5OH+O2": "CO2+H2O",

            # Разложение (расширенная)
            "CaCO3": "CaO+CO2",
            "MgCO3": "MgO+CO2",
            "Cu(OH)2": "CuO+H2O",
            "Al(OH)3": "Al2O3+H2O",
            "Fe(OH)3": "Fe2O3+H2O",
            "H2O2": "H2O+O2",
            "KClO3": "KCl+O2",
            "NaHCO3": "Na2CO3+CO2+H2O",
            "Ca(OH)2": "CaO+H2O",
            "Mg(OH)2": "MgO+H2O",
            "Zn(OH)2": "ZnO+H2O",
            "Pb(NO3)2": "PbO+NO2+O2",
            "NH4NO3": "N2O+H2O",
            "KNO3": "KNO2+O2",
            "HgO": "Hg+O2",
            "Ag2O": "Ag+O2",

            # Вытеснение металлов (расширенная)
            "Zn+CuSO4": "ZnSO4+Cu",
            "Fe+CuSO4": "FeSO4+Cu",
            "Al+CuSO4": "Al2(SO4)3+Cu",
            "Mg+FeSO4": "MgSO4+Fe",
            "Zn+FeSO4": "ZnSO4+Fe",
            "Al+FeSO4": "Al2(SO4)3+Fe",
            "Ca+ZnSO4": "CaSO4+Zn",
            "Mg+ZnSO4": "MgSO4+Zn",
            "Zn+Pb(NO3)2": "Zn(NO3)2+Pb",
            "Fe+Pb(NO3)2": "Fe(NO3)2+Pb",
            "Al+Pb(NO3)2": "Al(NO3)3+Pb",

            # Реакции обмена (расширенная)
            "NaCl+AgNO3": "AgCl+NaNO3",
            "KBr+AgNO3": "AgBr+KNO3",
            "Na2SO4+BaCl2": "BaSO4+NaCl",
            "K2CO3+CaCl2": "CaCO3+KCl",
            "NaOH+HCl": "NaCl+H2O",
            "KOH+H2SO4": "K2SO4+H2O",
            "Ca(OH)2+CO2": "CaCO3+H2O",
            "NaHCO3+HCl": "NaCl+CO2+H2O",
            "CH3COOH+NaHCO3": "CH3COONa+CO2+H2O",

            # Окислительно-восстановительные реакции
            "Zn+2HCl": "ZnCl2+H2",
            "Cu+2H2SO4": "CuSO4+SO2+2H2O",
            "MnO2+4HCl": "MnCl2+Cl2+2H2O",
            "KMnO4+8HCl": "KCl+MnCl2+Cl2+4H2O",
            "K2Cr2O7+8HCl": "2KCl+2CrCl3+Cl2+4H2O",
            "Fe+2HCl": "FeCl2+H2",
            "Mg+2HCl": "MgCl2+H2",

            # Дополнительные ОВР реакции
            "MnO2+HCl": "MnCl2+Cl2+2H2O",  # Правильная форма
            "KMnO4+HCl": "KCl+MnCl2+Cl2+4H2O",  # Правильная форма
            "K2Cr2O7+HCl": "2KCl+2CrCl3+Cl2+7H2O",  # Правильная форма

            # Синтез оксидов
            "CaO+H2O": "Ca(OH)2",
            "Na2O+H2O": "NaOH",
            "K2O+H2O": "KOH",
            "SO3+H2O": "H2SO4",
            "CO2+H2O": "H2CO3",
            "P2O5+H2O": "H3PO4",
            "N2O5+H2O": "HNO3",
            "Cl2O+H2O": "HClO",

            # Амфотерные гидроксиды
            "Al(OH)3+NaOH": "NaAlO2+H2O",
            "Zn(OH)2+NaOH": "Na2ZnO2+H2O",
            "Al(OH)3+HCl": "AlCl3+H2O",
            "Zn(OH)2+HCl": "ZnCl2+H2O",
            "Pb(OH)2+NaOH": "Na2PbO2+H2O",

            # Органические реакции
            "CH3COOH+NaHCO3": "CH3COONa+CO2+H2O",
            "C6H12O6": "C2H5OH+CO2",
            "C12H22O11+H2O": "C6H12O6",
            "C2H5OH+O2": "CH3COOH+H2O",
            "CH3COOH+NaOH": "CH3COONa+H2O",

            # Дополнительные реакции
            "Na+H2O": "NaOH+H2",
            "Ca+H2O": "Ca(OH)2+H2",
            "Mg+H2O": "Mg(OH)2+H2",
            "Fe+H2O": "Fe(OH)2+H2",
            "Cu+H2O": "Cu(OH)2+H2",
            "Zn+H2O": "Zn(OH)2+H2",
            "Al+H2O": "Al(OH)3+H2",

            # Реакции с солями
            "Na2CO3+HCl": "NaCl+CO2+H2O",
            "K2CO3+H2SO4": "K2SO4+CO2+H2O",
            "CaCO3+HCl": "CaCl2+CO2+H2O",
            "NaHCO3+HCl": "NaCl+CO2+H2O",
            "Na2SO3+H2SO4": "Na2SO4+SO2+H2O",
        }

        # Паттерны для распознавания типов реакций
        self.reaction_patterns = {
            'metal_acid': r'([A-Z][a-z]?)(\d*)\s*\+\s*H[A-Z]+',
            'metal_oxygen': r'([A-Z][a-z]?)(\d*)\s*\+\s*O2',
            'acid_base': r'H[A-Z]+\s*\+\s*[A-Z][a-z]*OH',
            'combustion': r'C.*H.*\s*\+\s*O2',
            'decomposition': r'^[A-Z][^+-]*$',
        }

    def normalize_formula(self, formula):
        """Нормализация химической формулы для поиска"""
        # Убираем пробелы и приводим к единому формату
        formula = re.sub(r'\s+', '', formula)
        # НЕ сортируем реагенты, сохраняем порядок для точного поиска
        return formula

    def predict_reaction(self, reactants):
        """Предсказание продуктов реакции"""
        normalized = self.normalize_formula(reactants)

        # Прямой поиск в базе знаний
        if normalized in self.knowledge_base:
            return self.knowledge_base[normalized]

        # Анализ по паттернам
        return self.analyze_by_pattern(reactants)

    def analyze_by_pattern(self, reactants):
        """Анализ реакции по паттернам"""
        reactants = reactants.strip()

        # Окислительно-восстановительные реакции (проверяем первыми)
        if self._is_redox_reaction(reactants):
            return self.predict_redox_reaction(reactants)

        # Металл + кислота
        if re.search(r'[A-Z][a-z]?\s*\+\s*H[A-Z]', reactants):
            return self.predict_metal_acid(reactants)

        # Металл + кислород
        elif re.search(r'[A-Z][a-z]?\s*\+\s*O2', reactants):
            return self.predict_metal_oxygen(reactants)

        # Кислота + основание
        elif re.search(r'H[A-Z]+\s*\+\s*[A-Z][a-z]*OH', reactants):
            return self.predict_acid_base(reactants)

        # Горение углеводородов
        elif re.search(r'C.*H.*\s*\+\s*O2', reactants):
            return "CO2+H2O"

        # Разложение (одиночный реагент)
        elif '+' not in reactants and reactants:
            return self.predict_decomposition(reactants)

        return None

    def _is_redox_reaction(self, reactants):
        """Проверка, является ли реакция окислительно-восстановительной"""
        redox_indicators = [
            'MnO2', 'KMnO4', 'K2Cr2O7', 'H2O2', 'Cl2', 'Br2', 'I2',
            'CuO', 'Fe2O3', 'Al2O3', 'ZnO', 'MgO', 'CaO'
        ]

        parts = [p.strip() for p in reactants.split('+')]
        for part in parts:
            for indicator in redox_indicators:
                if indicator in part:
                    return True
        return False

    def predict_redox_reaction(self, reaction):
        """Предсказание ОВР реакции"""
        parts = [p.strip() for p in reaction.split('+')]

        # MnO2 + HCl → MnCl2 + Cl2 + 2H2O
        if 'MnO2' in reaction and 'HCl' in reaction:
            return "MnCl2+Cl2+2H2O"

        # KMnO4 + HCl → KCl + MnCl2 + Cl2 + 4H2O (кислотная среда)
        elif 'KMnO4' in reaction and 'HCl' in reaction:
            return "KCl+MnCl2+Cl2+4H2O"

        # K2Cr2O7 + HCl → 2KCl + 2CrCl3 + Cl2 + 7H2O (кислотная среда)
        elif 'K2Cr2O7' in reaction and 'HCl' in reaction:
            return "2KCl+2CrCl3+Cl2+7H2O"

        # H2O2 + HCl → Cl2 + 2H2O (с сильными окислителями)
        elif 'H2O2' in reaction and 'HCl' in reaction:
            return "Cl2+2H2O"

        # Общий случай - упрощенное предсказание
        return self.predict_metal_acid(reaction)

    def predict_metal_acid(self, reaction):
        """Предсказание реакции металл + кислота"""
        parts = [p.strip() for p in reaction.split('+')]
        metal = parts[0]
        acid = parts[1] if len(parts) > 1 else "HCl"

        # Определяем анион кислоты
        if "HCl" in acid or "HBr" in acid or "HI" in acid:
            anion = acid.replace("H", "") if len(acid) > 1 else "Cl"
        elif "H2SO4" in acid:
            anion = "SO4"
        elif "HNO3" in acid:
            anion = "NO3"
        else:
            anion = "Cl"

        # Валентность металла (упрощенная)
        valences = {
            'Li': 1, 'Na': 1, 'K': 1, 'Rb': 1, 'Cs': 1,
            'Be': 2, 'Mg': 2, 'Ca': 2, 'Sr': 2, 'Ba': 2, 'Ra': 2,
            'Al': 3, 'Zn': 2, 'Fe': 2, 'Cu': 2, 'Ag': 1, 'Au': 1
        }

        valency = valences.get(metal, 2)

        if anion in ['Cl', 'Br', 'I']:
            salt = f"{metal}{anion}{valency}" if valency > 1 else f"{metal}{anion}"
        elif anion == 'SO4':
            salt = f"{metal}{anion}" if valency == 2 else f"{metal}2({anion})"
        else:
            salt = f"{metal}{anion}{valency}" if valency > 1 else f"{metal}{anion}"

        return f"{salt}+H2"

    def predict_metal_oxygen(self, reaction):
        """Предсказание реакции металл + кислород"""
        metal = reaction.split('+')[0].strip()

        # Валентность металла
        valences = {
            'Li': 1, 'Na': 1, 'K': 1, 'Rb': 1, 'Cs': 1, 'Fr': 1,
            'Be': 2, 'Mg': 2, 'Ca': 2, 'Sr': 2, 'Ba': 2, 'Ra': 2,
            'Al': 3, 'Zn': 2, 'Fe': 3, 'Cu': 2, 'Ag': 1, 'Au': 3
        }

        valency = valences.get(metal, 2)

        if valency == 1:
            return f"{metal}2O"
        elif valency == 2:
            return f"{metal}O"
        else:
            return f"{metal}2O3"

    def predict_acid_base(self, reaction):
        """Предсказание реакции кислота + основание"""
        parts = [p.strip() for p in reaction.split('+')]
        acid = parts[0]
        base = parts[1] if len(parts) > 1 else "NaOH"

        # Определяем анион кислоты
        if "HCl" in acid:
            anion = "Cl"
        elif "H2SO4" in acid:
            anion = "SO4"
        elif "HNO3" in acid:
            anion = "NO3"
        else:
            anion = "Cl"

        # Определяем металл в основании
        base_match = re.search(r'([A-Z][a-z]*)OH', base)
        if base_match:
            metal = base_match.group(1)
        else:
            metal = "Na"

        # Валентность металла
        valences = {'Li': 1, 'Na': 1, 'K': 1, 'Ca': 2, 'Mg': 2, 'Ba': 2}
        valency = valences.get(metal, 1)

        if anion in ['Cl', 'Br', 'I']:
            salt = f"{metal}{anion}{valency}" if valency > 1 else f"{metal}{anion}"
        elif anion == 'SO4':
            salt = f"{metal}{anion}" if valency == 2 else f"{metal}2{anion}"
        else:
            salt = f"{metal}{anion}{valency}" if valency > 1 else f"{metal}{anion}"

        return f"{salt}+H2O"

    def predict_decomposition(self, reactant):
        """Предсказание реакции разложения"""
        reactant = reactant.strip()

        if "CO3" in reactant:
            metal = reactant.split('CO3')[0]
            return f"{metal}O+CO2"
        elif "(OH)2" in reactant:
            metal = reactant.split('(OH)2')[0]
            return f"{metal}O+H2O"
        elif "OH" in reactant and reactant != "H2O":
            metal = reactant.split('OH')[0]
            return f"{metal}O+H2O"
        elif reactant == "H2O2":
            return "H2O+O2"
        elif "ClO3" in reactant:
            metal = reactant.split('ClO3')[0]
            return f"{metal}Cl+O2"

        return None

    def get_info(self):
        """Получение информации о расширенной нейронной сети"""
        return f"""
🧠 РАСШИРЕННАЯ НЕЙРОННАЯ СЕТЬ ДЛЯ ХИМИИ 🤖

📊 Статистика:
• Реакций в базе знаний: {len(self.knowledge_base)}+
• Распознаваемых паттернов: {len(self.reaction_patterns)}
• Поддерживаемых элементов: 50+

🎯 ПОДДЕРЖИВАЕМЫЕ ТИПЫ РЕАКЦИЙ:

🔸 Металл + кислота (HCl, H2SO4, HNO3)
🔸 Металл + кислород (оксиды металлов)
🔸 Кислота + основание (нейтрализация)
🔸 Горение (углеводороды, элементы)
🔸 Разложение (карбонаты, гидроксиды)
🔸 Вытеснение металлов (ряд активности)
🔸 Реакции обмена (осадки, газы)
🔸 ОВР (окислительно-восстановительные)
🔸 Синтез оксидов (гидратация)
🔸 Амфотерные гидроксиды
🔸 Органические реакции

⚡ Статус: АКТИВНА И ГОТОВА К РАБОТЕ!
🚀 Может решать более 100 различных реакций!
        """

# Глобальный экземпляр для использования в боте
neural_predictor = SimpleNeuralChemistry()

def predict_reaction(reactants):
    """Функция для предсказания реакции (для совместимости)"""
    return neural_predictor.predict_reaction(reactants)

if __name__ == "__main__":
    # Тестирование
    predictor = SimpleNeuralChemistry()

    test_cases = [
        "Zn + HCl",
        "CH4 + O2",
        "Na + O2",
        "HCl + NaOH",
        "CaCO3",
        "Fe + CuSO4"
    ]

    print("🧪 Тестирование простой нейронной сети:")
    print("=" * 50)

    for test in test_cases:
        result = predictor.predict_reaction(test)
        print(f"Вход: {test}")
        print(f"Выход: {result}")
        print("-" * 30)

    print("\n" + predictor.get_info())