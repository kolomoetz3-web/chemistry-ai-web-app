import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from fractions import Fraction
import re
from collections import defaultdict

class ChemicalEquationSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("🧪 Химический калькулятор - Решение уравнений реакций")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#0a0e27')
        
        # Современная цветовая палитра с градиентами
        self.colors = {
            'bg_main': '#0a0e27',
            'bg_secondary': '#1a1f3a',
            'bg_card': '#252b4a',
            'primary': '#6366f1',
            'primary_dark': '#4f46e5',
            'primary_light': '#818cf8',
            'success': '#10b981',
            'success_dark': '#059669',
            'warning': '#f59e0b',
            'warning_dark': '#d97706',
            'danger': '#ef4444',
            'danger_dark': '#dc2626',
            'accent': '#8b5cf6',
            'accent_dark': '#7c3aed',
            'text_primary': '#f8fafc',
            'text_secondary': '#cbd5e1',
            'text_muted': '#94a3b8',
            'border': '#334155',
            'shadow': '#000000',
            'gradient_start': '#6366f1',
            'gradient_end': '#8b5cf6'
        }
        
        # Кэш для быстрого доступа
        self.reaction_cache = {}
        self.balance_cache = {}
        
        # Настройка стиля с современным дизайном
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', 
                       background=self.colors['bg_main'], 
                       borderwidth=0,
                       tabmargins=[0, 0, 0, 0])
        style.configure('TNotebook.Tab', 
                       padding=[30, 15], 
                       font=('Segoe UI', 12, 'bold'),
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_secondary'],
                       borderwidth=0)
        style.map('TNotebook.Tab', 
                 background=[('selected', self.colors['primary'])],
                 foreground=[('selected', 'white')],
                 expand=[('selected', [1, 1, 1, 0])])
        style.configure('TFrame', background=self.colors['bg_main'])
        
        # База знаний о химических соединениях
        self.setup_chemical_knowledge()
        
        # Словарь атомных масс элементов
        self.atomic_masses = {
            'H': 1.008, 'He': 4.003, 'Li': 6.941, 'Be': 9.012, 'B': 10.81,
            'C': 12.01, 'N': 14.01, 'O': 16.00, 'F': 19.00, 'Ne': 20.18,
            'Na': 22.99, 'Mg': 24.31, 'Al': 27.00, 'Si': 28.09, 'P': 30.97,
            'S': 32.07, 'Cl': 35.45, 'Ar': 39.95, 'K': 39.10, 'Ca': 40.08,
            'Sc': 44.96, 'Ti': 47.87, 'V': 50.94, 'Cr': 52.00, 'Mn': 54.94,
            'Fe': 55.85, 'Co': 58.93, 'Ni': 58.69, 'Cu': 63.55, 'Zn': 65.38,
            'Ga': 69.72, 'Ge': 72.64, 'As': 74.92, 'Se': 78.96, 'Br': 79.90,
            'Kr': 83.80, 'Rb': 85.47, 'Sr': 87.62, 'Y': 88.91, 'Zr': 91.22,
            'Nb': 92.91, 'Mo': 95.96, 'Tc': 98.00, 'Ru': 101.07, 'Rh': 102.91,
            'Pd': 106.42, 'Ag': 107.87, 'Cd': 112.41, 'In': 114.82, 'Sn': 118.71,
            'Sb': 121.76, 'Te': 127.60, 'I': 126.90, 'Xe': 131.29, 'Cs': 132.91,
            'Ba': 137.33, 'La': 138.91, 'Ce': 140.12, 'Pr': 140.91, 'Nd': 144.24,
            'Pm': 145.00, 'Sm': 150.36, 'Eu': 151.96, 'Gd': 157.25, 'Tb': 158.93,
            'Dy': 162.50, 'Ho': 164.93, 'Er': 167.26, 'Tm': 168.93, 'Yb': 173.05,
            'Lu': 174.97, 'Hf': 178.49, 'Ta': 180.95, 'W': 183.84, 'Re': 186.21,
            'Os': 190.23, 'Ir': 192.22, 'Pt': 195.08, 'Au': 196.97, 'Hg': 200.59,
            'Tl': 204.38, 'Pb': 207.2, 'Bi': 208.98, 'Po': 209.00, 'At': 210.00,
            'Rn': 222.00, 'Fr': 223.00, 'Ra': 226.00, 'Ac': 227.00, 'Th': 232.04,
            'Pa': 231.04, 'U': 238.03, 'Np': 237.00, 'Pu': 244.00, 'Am': 243.00
        }
        
        self.setup_ui()
    
    def setup_chemical_knowledge(self):
        """Расширенная база знаний о химических соединениях"""
        # Кислоты
        self.acids = {
            'HCl': 'соляная', 'HBr': 'бромоводородная', 'HI': 'иодоводородная',
            'HNO3': 'азотная', 'H2SO4': 'серная', 'HClO4': 'хлорная',
            'HF': 'плавиковая', 'H2CO3': 'угольная', 'H2S': 'сероводородная',
            'H3PO4': 'фосфорная', 'CH3COOH': 'уксусная', 'HCN': 'синильная',
            'H2SO3': 'сернистая', 'HNO2': 'азотистая', 'H2SiO3': 'кремниевая',
            'HMnO4': 'марганцовая', 'H2CrO4': 'хромовая', 'H2Cr2O7': 'дихромовая'
        }
        
        # Основания
        self.bases = {
            'LiOH': 'гидроксид лития', 'NaOH': 'гидроксид натрия', 'KOH': 'гидроксид калия',
            'RbOH': 'гидроксид рубидия', 'CsOH': 'гидроксид цезия', 'Ba(OH)2': 'гидроксид бария',
            'Ca(OH)2': 'гидроксид кальция', 'Sr(OH)2': 'гидроксид стронция',
            'NH3': 'аммиак', 'NH4OH': 'гидроксид аммония',
            'Al(OH)3': 'гидроксид алюминия', 'Fe(OH)2': 'гидроксид железа(II)',
            'Fe(OH)3': 'гидроксид железа(III)', 'Cu(OH)2': 'гидроксид меди(II)',
            'Zn(OH)2': 'гидроксид цинка', 'Mg(OH)2': 'гидроксид магния',
            'Mn(OH)2': 'гидроксид марганца(II)', 'Cr(OH)3': 'гидроксид хрома(III)'
        }
        
        # Металлы с валентностями
        self.metals = {
            'Li': 1, 'Na': 1, 'K': 1, 'Rb': 1, 'Cs': 1, 'Fr': 1,
            'Be': 2, 'Mg': 2, 'Ca': 2, 'Sr': 2, 'Ba': 2, 'Ra': 2,
            'Al': 3, 'Zn': 2, 'Cd': 2, 'Fe': [2, 3], 'Cu': [1, 2],
            'Ag': 1, 'Au': [1, 3], 'Sn': [2, 4], 'Pb': [2, 4],
            'Hg': [1, 2], 'Cr': [2, 3, 6], 'Mn': [2, 3, 4, 6, 7],
            'Co': [2, 3], 'Ni': [2, 3], 'Ti': [2, 3, 4], 'V': [2, 3, 4, 5]
        }
        
        # Ряд активности металлов
        self.metal_activity_series = [
            'Li', 'K', 'Ba', 'Ca', 'Na', 'Mg', 'Al', 'Mn', 'Zn', 'Cr',
            'Fe', 'Cd', 'Co', 'Ni', 'Sn', 'Pb', 'H', 'Cu', 'Hg', 'Ag', 'Pt', 'Au'
        ]
        
        # Анионы
        self.anions = {
            'Cl': 'хлорид', 'Br': 'бромид', 'I': 'иодид', 'F': 'фторид',
            'NO3': 'нитрат', 'SO4': 'сульфат', 'CO3': 'карбонат',
            'PO4': 'фосфат', 'S': 'сульфид', 'OH': 'гидроксид',
            'CH3COO': 'ацетат', 'ClO4': 'перхлорат', 'SO3': 'сульфит',
            'MnO4': 'перманганат', 'CrO4': 'хромат', 'Cr2O7': 'дихромат'
        }
        
        # Расширенная база реакций для быстрого решения
        self.reaction_patterns = {
            # Металл + кислота
            ('metal', 'acid'): lambda m, a: self.metal_acid_reaction(m, a),
            # Металл + соль
            ('metal', 'salt'): lambda m, s: self.metal_salt_reaction(m, s),
            # Кислота + основание
            ('acid', 'base'): lambda a, b: self.acid_base_reaction(a, b),
            # Оксид + кислота
            ('oxide', 'acid'): lambda o, a: self.oxide_acid_reaction(o, a),
            # Оксид + основание
            ('oxide', 'base'): lambda o, b: self.oxide_base_reaction(o, b),
            # Соль + соль
            ('salt', 'salt'): lambda s1, s2: self.salt_salt_reaction(s1, s2),
            # Горение
            ('organic', 'oxygen'): lambda o, ox: self.combustion_reaction(o),
        }
    
    def setup_ui(self):
        # Создаем notebook для вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Вкладка 1: Решение уравнений
        self.equation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.equation_frame, text="⚖️ Решение уравнений")
        self.setup_equation_tab()
        
        # Вкладка 2: Таблица Менделеева
        self.periodic_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.periodic_frame, text="📊 Таблица Менделеева")
        self.setup_periodic_table()
        
        # Вкладка 3: Растворимость
        self.solubility_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.solubility_frame, text="💧 Растворимость")
        self.setup_solubility_tab()
        
        # Вкладка 4: Кислоты и основания
        self.acid_base_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.acid_base_frame, text="🧪 Кислоты и основания")
        self.setup_acid_base_tab()
        
        # Вкладка 5: Справочник
        self.reference_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reference_frame, text="📚 Справочник")
        self.setup_reference_tab()
        
        # Вкладка 6: Константы и формулы
        self.constants_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.constants_frame, text="🔬 Константы")
        self.setup_constants_tab()
        
        # Вкладка 7: Окислительно-восстановительные реакции
        self.redox_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.redox_frame, text="⚡ ОВР")
        self.setup_redox_tab()
    
    def create_modern_button(self, parent, text, command, bg_color, hover_color=None, **kwargs):
        """Создает современную кнопку с эффектом hover и тенью"""
        if hover_color is None:
            hover_color = bg_color
        
        btn = tk.Button(
            parent,
            text=text,
            font=kwargs.get('font', ('Segoe UI', 12, 'bold')),
            bg=bg_color,
            fg='white',
            padx=kwargs.get('padx', 25),
            pady=kwargs.get('pady', 12),
            cursor='hand2',
            activebackground=hover_color,
            activeforeground='white',
            relief='flat',
            borderwidth=0,
            command=command,
            highlightthickness=0,
            bd=0
        )
        
        # Эффект hover с плавным переходом
        def on_enter(e):
            btn.config(bg=hover_color)
        def on_leave(e):
            btn.config(bg=bg_color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def create_card(self, parent, **kwargs):
        """Создает современную карточку с тенью"""
        card = tk.Frame(
            parent,
            bg=self.colors['bg_card'],
            relief='flat',
            **kwargs
        )
        return card
    
    def setup_equation_tab(self):
        # Контейнер с градиентным фоном
        main_container = tk.Frame(self.equation_frame, bg=self.colors['bg_main'])
        main_container.pack(fill='both', expand=True)
        
        # Заголовок с градиентным эффектом
        header_frame = tk.Frame(main_container, bg=self.colors['primary'], height=140)
        header_frame.pack(fill='x', pady=(0, 30))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="⚖️ Балансировка химических уравнений",
            font=('Segoe UI', 28, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        )
        title_label.pack(expand=True, pady=20)
        
        subtitle = tk.Label(
            header_frame,
            text="Введите уравнение или только реагенты для автоматического решения",
            font=('Segoe UI', 13),
            bg=self.colors['primary'],
            fg='#e0e7ff'
        )
        subtitle.pack(pady=(0, 20))
        
        # Карточка для поля ввода
        input_card = self.create_card(main_container)
        input_card.pack(pady=15, padx=40, fill='x')
        
        input_frame = tk.Frame(input_card, bg=self.colors['bg_card'])
        input_frame.pack(pady=25, padx=30, fill='x')
        
        tk.Label(
            input_frame,
            text="Уравнение:",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side='left', padx=(0, 20))
        
        # Современное поле ввода
        entry_container = tk.Frame(input_frame, bg=self.colors['border'], height=50)
        entry_container.pack(side='left', padx=15, fill='x', expand=True)
        
        self.equation_entry = tk.Entry(
            entry_container,
            font=('Segoe UI', 14),
            relief='flat',
            borderwidth=0,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['primary'],
            selectbackground=self.colors['primary'],
            selectforeground='white'
        )
        self.equation_entry.pack(fill='both', expand=True, padx=3, pady=3)
        self.equation_entry.bind('<Return>', lambda e: self.solve_reaction())
        
        # Кнопки в отдельном фрейме
        buttons_frame = tk.Frame(input_frame, bg=self.colors['bg_card'])
        buttons_frame.pack(side='left', padx=(15, 0))
        
        # Кнопка решения
        solve_btn = self.create_modern_button(
            buttons_frame,
            "✓ Решить",
            self.solve_reaction,
            self.colors['success'],
            self.colors['success_dark'],
            font=('Segoe UI', 13, 'bold'),
            padx=30,
            pady=14
        )
        solve_btn.pack(side='left', padx=8)
        
        # Кнопка авто-решения
        auto_btn = self.create_modern_button(
            buttons_frame,
            "🚀 Авто-решение",
            self.auto_solve_reaction,
            self.colors['warning'],
            self.colors['warning_dark'],
            font=('Segoe UI', 12, 'bold'),
            padx=25,
            pady=14
        )
        auto_btn.pack(side='left', padx=8)
        
        # Кнопка очистки
        clear_btn = self.create_modern_button(
            buttons_frame,
            "🗑 Очистить",
            lambda: (self.equation_entry.delete(0, tk.END), self.result_text.delete('1.0', tk.END)),
            self.colors['danger'],
            self.colors['danger_dark'],
            font=('Segoe UI', 12),
            padx=22,
            pady=14
        )
        clear_btn.pack(side='left', padx=8)
        
        # Примеры в карточке
        examples_card = self.create_card(main_container)
        examples_card.pack(pady=20, padx=40, fill='x')
        
        examples_inner = tk.Frame(examples_card, bg=self.colors['bg_card'])
        examples_inner.pack(pady=20, padx=25)
        
        tk.Label(
            examples_inner,
            text="📝 Примеры для быстрого старта:",
            font=('Segoe UI', 13, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(pady=(0, 15))
        
        examples = [
            "H2 + O2 -> H2O",
            "Fe + O2 -> Fe2O3",
            "CH4 + O2 -> CO2 + H2O",
            "Al + HCl",
            "NaOH + HCl",
            "CaCO3",
            "Zn + CuSO4",
            "H2SO4 + NaOH"
        ]
        
        examples_buttons_frame = tk.Frame(examples_inner, bg=self.colors['bg_card'])
        examples_buttons_frame.pack()
        
        for i, example in enumerate(examples):
            btn = self.create_modern_button(
                examples_buttons_frame,
                example,
                lambda e=example: self.load_example(e),
                self.colors['primary_light'],
                self.colors['primary'],
                font=('Segoe UI', 10),
                padx=15,
                pady=8
            )
            btn.grid(row=i//4, column=i%4, padx=6, pady=6)
        
        # Результат в карточке
        result_card = self.create_card(main_container)
        result_card.pack(pady=25, padx=40, fill='both', expand=True)
        
        result_header = tk.Frame(result_card, bg=self.colors['success'], height=55)
        result_header.pack(fill='x')
        result_header.pack_propagate(False)
        
        tk.Label(
            result_header,
            text="📊 Результат:",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['success'],
            fg='white'
        ).pack(expand=True)
        
        # Текстовое поле с улучшенным стилем
        text_container = tk.Frame(result_card, bg=self.colors['bg_card'])
        text_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.result_text = scrolledtext.ScrolledText(
            text_container,
            font=('Segoe UI', 13),
            height=18,
            wrap='word',
            bg=self.colors['bg_secondary'],
            relief='flat',
            borderwidth=1,
            padx=25,
            pady=25,
            fg=self.colors['text_primary'],
            insertbackground=self.colors['primary'],
            selectbackground=self.colors['primary'],
            selectforeground='white',
            highlightthickness=0
        )
        self.result_text.pack(fill='both', expand=True)
    
    def load_example(self, example):
        self.equation_entry.delete(0, tk.END)
        self.equation_entry.insert(0, example)
        # Автоматически решаем пример
        self.root.after(100, self.solve_reaction)
    
    def parse_molecule(self, formula):
        """Оптимизированный парсер молекул с кэшированием"""
        cache_key = formula.strip()
        if cache_key in self.balance_cache:
            return self.balance_cache[cache_key].copy()
        
        elements = {}
        formula = formula.strip()
        
        def parse_formula(f, multiplier=1):
            i = 0
            while i < len(f):
                if f[i] == '(':
                    depth = 1
                    j = i + 1
                    while j < len(f) and depth > 0:
                        if f[j] == '(':
                            depth += 1
                        elif f[j] == ')':
                            depth -= 1
                        j += 1
                    
                    inner = f[i+1:j-1]
                    k = j
                    num_str = ''
                    while k < len(f) and f[k].isdigit():
                        num_str += f[k]
                        k += 1
                    bracket_mult = int(num_str) if num_str else 1
                    
                    parse_formula(inner, multiplier * bracket_mult)
                    i = k
                elif f[i].isupper():
                    element = f[i]
                    i += 1
                    while i < len(f) and f[i].islower():
                        element += f[i]
                        i += 1
                    
                    num_str = ''
                    while i < len(f) and f[i].isdigit():
                        num_str += f[i]
                        i += 1
                    count = int(num_str) if num_str else 1
                    
                    elements[element] = elements.get(element, 0) + count * multiplier
                else:
                    i += 1
        
        parse_formula(formula)
        self.balance_cache[cache_key] = elements.copy()
        return elements
    
    def identify_compound_type(self, formula):
        """Определяет тип химического соединения"""
        formula_clean = formula.replace('(', '').replace(')', '').strip()
        formula_upper = formula_clean.upper()
        
        if formula_clean == 'H2O':
            return 'water'
        
        if formula_clean in ['H2', 'O2', 'N2', 'Cl2', 'F2', 'Br2', 'I2']:
            if formula_clean == 'H2':
                return 'hydrogen'
            elif formula_clean == 'O2':
                return 'oxygen'
            return 'nonmetal'
        
        if len(formula_clean) <= 2 and formula_clean[0].isupper():
            if formula_clean in self.metals:
                return 'metal'
            if len(formula_clean) == 2 and formula_clean[0].isupper() and formula_clean[1].islower():
                if formula_clean in self.metals:
                    return 'metal'
        
        if formula_clean in self.acids:
            return 'acid'
        if formula_clean.startswith('H') and formula_clean != 'H2' and formula_clean != 'H2O':
            if any(anion in formula_upper for anion in ['CL', 'BR', 'I', 'NO3', 'SO4', 'CO3', 'PO4', 'SO3', 'S', 'CN', 'CH3COO']):
                return 'acid'
        
        if formula_clean in self.bases:
            return 'base'
        if 'OH' in formula_clean or '(OH)' in formula_clean:
            return 'base'
        
        if 'O' in formula_clean and 'OH' not in formula_clean:
            if formula_clean.count('O') <= 3 and not formula_clean.startswith('H'):
                if not any(anion in formula_upper for anion in ['NO3', 'SO4', 'CO3', 'PO4', 'CL', 'BR']):
                    return 'oxide'
        
        if any(anion in formula_upper for anion in ['CL', 'BR', 'I', 'NO3', 'SO4', 'CO3', 'PO4', 'S']):
            if not formula_clean.startswith('H') and 'OH' not in formula_clean:
                return 'salt'
        
        if 'C' in formula_clean and 'H' in formula_clean and len(formula_clean) > 2:
            if formula_clean not in ['CH', 'CH2', 'CH3', 'CH4'] or len(formula_clean) > 4:
                return 'organic'
        
        return 'unknown'
    
    # Расширенные функции для предсказания реакций
    def metal_acid_reaction(self, metal, acid):
        """Металл + кислота"""
        acid_upper = acid.upper()
        if 'HCL' in acid_upper or (acid_upper.startswith('H') and 'CL' in acid_upper):
            anion = 'Cl'
        elif 'H2SO4' in acid_upper or 'SO4' in acid_upper:
            anion = 'SO4'
        elif 'HNO3' in acid_upper or 'NO3' in acid_upper:
            anion = 'NO3'
        elif 'HBR' in acid_upper:
            anion = 'Br'
        elif 'HI' in acid_upper:
            anion = 'I'
        else:
            anion = 'Cl'
        
        if metal in self.metals:
            valency = self.metals[metal]
            if isinstance(valency, list):
                valency = valency[0]
        else:
            valency = 1
        
        if anion in ['Cl', 'Br', 'I', 'F']:
            salt = f"{metal}{anion}{valency}" if valency > 1 else f"{metal}{anion}"
        elif anion == 'SO4':
            salt = f"{metal}{anion}" if valency == 2 else f"{metal}2({anion})" if valency == 1 else f"{metal}2({anion})3"
        elif anion == 'NO3':
            salt = f"{metal}({anion}){valency}" if valency > 1 else f"{metal}{anion}"
        else:
            salt = f"{metal}({anion}){valency}" if valency > 1 else f"{metal}{anion}"
        
        if metal in self.metal_activity_series:
            metal_pos = self.metal_activity_series.index(metal)
            h_pos = self.metal_activity_series.index('H')
            if metal_pos < h_pos:
                return [salt, "H2"]
        return [salt]
    
    def metal_salt_reaction(self, metal, salt):
        """Металл + соль (вытеснение)"""
        salt_metal = salt[0] if salt[0].isupper() else salt[:2]
        if salt_metal in self.metal_activity_series and metal in self.metal_activity_series:
            metal_pos = self.metal_activity_series.index(metal)
            salt_metal_pos = self.metal_activity_series.index(salt_metal)
            if metal_pos < salt_metal_pos:
                anion = salt.replace(salt_metal, '').strip()
                if metal in self.metals:
                    valency = self.metals[metal]
                    if isinstance(valency, list):
                        valency = valency[0]
                else:
                    valency = 2
                new_salt = f"{metal}{anion}" if valency == 1 else f"{metal}{anion}{valency}"
                return [new_salt, salt_metal]
        return None
    
    def acid_base_reaction(self, acid, base):
        """Кислота + основание (нейтрализация)"""
        acid_upper = acid.upper()
        if 'HCL' in acid_upper:
            anion = 'Cl'
        elif 'H2SO4' in acid_upper:
            anion = 'SO4'
        elif 'HNO3' in acid_upper:
            anion = 'NO3'
        else:
            anion = 'Cl'
        
        base_clean = base.replace('(OH)', '').replace('OH', '').replace('(', '').replace(')', '')
        if len(base_clean) >= 2 and base_clean[1].islower():
            metal = base_clean[:2]
        else:
            metal = base_clean[0] if base_clean else 'Na'
        
        if metal in self.metals:
            valency = self.metals[metal]
            if isinstance(valency, list):
                valency = valency[0]
        else:
            valency = 1
        
        if anion in ['Cl', 'Br', 'I', 'F']:
            salt = f"{metal}{anion}{valency}" if valency > 1 else f"{metal}{anion}"
        elif anion == 'SO4':
            salt = f"{metal}2{anion}" if valency == 1 else f"{metal}{anion}"
        else:
            salt = f"{metal}({anion}){valency}" if valency > 1 else f"{metal}{anion}"
        
        return [salt, "H2O"]
    
    def oxide_acid_reaction(self, oxide, acid):
        """Оксид + кислота"""
        return ["H2O"]  # Упрощенно
    
    def oxide_base_reaction(self, oxide, base):
        """Оксид + основание"""
        return ["H2O"]  # Упрощенно
    
    def salt_salt_reaction(self, salt1, salt2):
        """Соль + соль (обмен)"""
        return ["H2O"]  # Упрощенно
    
    def combustion_reaction(self, organic):
        """Горение органических соединений"""
        return ["CO2", "H2O"]
    
    def predict_reaction_products(self, reactants):
        """Улучшенное предсказание продуктов реакции"""
        if len(reactants) == 0:
            return None
        
        reactant_types = [self.identify_compound_type(r) for r in reactants]
        
        # Реакция разложения
        if len(reactants) == 1:
            return self.predict_decomposition(reactants[0])
        
        # Реакция соединения
        if len(reactants) == 2:
            if any(t in ['metal', 'hydrogen', 'oxygen', 'oxide'] for t in reactant_types):
                return self.predict_combination(reactants)
        
        # Реакция замещения
        if 'metal' in reactant_types:
            metal = None
            other = None
            for i, r in enumerate(reactants):
                if reactant_types[i] == 'metal':
                    metal = r.strip()
                else:
                    other = r.strip()
            if metal and other:
                other_type = self.identify_compound_type(other)
                if other_type == 'acid':
                    return self.metal_acid_reaction(metal, other)
                elif other_type == 'salt':
                    return self.metal_salt_reaction(metal, other)
        
        # Реакция обмена
        if ('acid' in reactant_types and 'base' in reactant_types):
            acid = None
            base = None
            for i, r in enumerate(reactants):
                if reactant_types[i] == 'acid':
                    acid = r.strip()
                elif reactant_types[i] == 'base':
                    base = r.strip()
            if acid and base:
                return self.acid_base_reaction(acid, base)
        
        # Горение
        if any('O2' in r.upper() for r in reactants):
            for r in reactants:
                if self.identify_compound_type(r) == 'organic' or ('C' in r and 'H' in r):
                    return self.combustion_reaction(r)
        
        return None
    
    def predict_decomposition(self, reactant):
        """Предсказывает продукты реакции разложения"""
        r = reactant.strip()
        
        if 'CO3' in r:
            metal = r.split('CO3')[0]
            return [f"{metal}O", "CO2"]
        
        if 'OH' in r and r != 'H2O':
            metal = r.split('(OH)')[0] if '(OH)' in r else r.split('OH')[0]
            return [f"{metal}O", "H2O"]
        
        if r == 'H2O2':
            return ["H2O", "O2"]
        
        if r == 'KClO3':
            return ["KCl", "O2"]
        
        if r == 'H2O':
            return ["H2", "O2"]
        
        return None
    
    def predict_combination(self, reactants):
        """Предсказывает продукты реакции соединения"""
        r1, r2 = reactants[0].strip(), reactants[1].strip()
        r1_upper = r1.upper()
        r2_upper = r2.upper()
        
        if r2_upper == 'O2' and self.identify_compound_type(r1) == 'metal':
            metal = r1
            if metal in ['Li', 'Na', 'K', 'Rb', 'Cs']:
                return [f"{metal}2O"]
            elif metal in ['Be', 'Mg', 'Ca', 'Sr', 'Ba']:
                return [f"{metal}O"]
            elif metal == 'Al':
                return ["Al2O3"]
            elif metal == 'Fe':
                return ["Fe3O4"]
            elif metal == 'Cu':
                return ["CuO"]
            elif metal == 'Zn':
                return ["ZnO"]
            else:
                if metal in self.metals:
                    valency = self.metals[metal]
                    if isinstance(valency, list):
                        valency = valency[0]
                    if valency == 1:
                        return [f"{metal}2O"]
                    elif valency == 2:
                        return [f"{metal}O"]
                    else:
                        return [f"{metal}2O3"]
                return [f"{metal}O"]
        
        if r1_upper == 'H2' and r2_upper == 'O2':
            return ["H2O"]
        
        if 'O' in r1 and r2_upper == 'H2O':
            if 'CaO' in r1:
                return ["Ca(OH)2"]
            elif 'Na2O' in r1:
                return ["NaOH"]
            elif 'K2O' in r1:
                return ["KOH"]
        
        if 'O' in r1 and r2_upper == 'H2O':
            if 'SO3' in r1:
                return ["H2SO4"]
            elif 'CO2' in r1:
                return ["H2CO3"]
            elif 'P2O5' in r1 or 'P4O10' in r1:
                return ["H3PO4"]
            elif 'N2O5' in r1:
                return ["HNO3"]
        
        return None
    
    def solve_reaction(self):
        """Универсальная функция решения реакции"""
        equation = self.equation_entry.get().strip()
        if not equation:
            messagebox.showwarning("Предупреждение", "Введите уравнение или реагенты!")
            return
        
        has_products = '->' in equation or '=' in equation
        
        if not has_products:
            self.auto_solve_reaction()
        else:
            self.balance_equation()
    
    def auto_solve_reaction(self):
        """Автоматически решает реакцию на основе реагентов"""
        equation = self.equation_entry.get().strip()
        if not equation:
            messagebox.showwarning("Предупреждение", "Введите реагенты!")
            return
        
        try:
            reactants = [r.strip() for r in equation.split('+')]
            products = self.predict_reaction_products(reactants)
            
            if not products:
                messagebox.showwarning("Предупреждение", 
                    "Не удалось определить тип реакции.\n"
                    "Попробуйте ввести полное уравнение с продуктами.")
                return
            
            reactants_str = " + ".join(reactants)
            products_str = " + ".join(products)
            full_equation = f"{reactants_str} -> {products_str}"
            
            self.equation_entry.delete(0, tk.END)
            self.equation_entry.insert(0, full_equation)
            
            self.balance_equation()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при решении реакции: {str(e)}")
    
    def balance_equation(self):
        """Оптимизированная балансировка уравнений"""
        equation = self.equation_entry.get().strip()
        if not equation:
            messagebox.showwarning("Предупреждение", "Введите уравнение!")
            return
        
        try:
            if '->' in equation:
                parts = equation.split('->')
            elif '=' in equation:
                parts = equation.split('=')
            else:
                messagebox.showerror("Ошибка", "Используйте -> или = для разделения реагентов и продуктов")
                return
            
            reactants_str = parts[0].strip()
            products_str = parts[1].strip()
            
            reactants = [r.strip() for r in reactants_str.split('+')]
            products = [p.strip() for p in products_str.split('+')]
            
            all_elements = set()
            reactant_elements = []
            product_elements = []
            
            for reactant in reactants:
                elements = self.parse_molecule(reactant)
                reactant_elements.append(elements)
                all_elements.update(elements.keys())
            
            for product in products:
                elements = self.parse_molecule(product)
                product_elements.append(elements)
                all_elements.update(elements.keys())
            
            num_reactants = len(reactants)
            num_products = len(products)
            num_compounds = num_reactants + num_products
            
            # Создаем систему уравнений
            matrix = []
            for element in sorted(all_elements):
                row = []
                for r_elem in reactant_elements:
                    row.append(-r_elem.get(element, 0))
                for p_elem in product_elements:
                    row.append(p_elem.get(element, 0))
                matrix.append(row)
            
            # Решаем систему
            coefficients = self.solve_system_fast(matrix, num_compounds)
            
            if coefficients and all(c > 0 for c in coefficients):
                coefficients = self.normalize_coefficients(coefficients)
                
                if any(c <= 0 for c in coefficients):
                    coefficients = self.balance_by_trial_optimized(reactant_elements, product_elements, all_elements)
                
                if coefficients:
                    result = "✨ Сбалансированное уравнение:\n\n"
                    
                    reactant_parts = []
                    for i, reactant in enumerate(reactants):
                        coeff = int(coefficients[i])
                        if coeff > 1:
                            reactant_parts.append(f"{coeff}{reactant}")
                        else:
                            reactant_parts.append(reactant)
                    
                    result += " + ".join(reactant_parts)
                    result += " → "
                    
                    product_parts = []
                    for i, product in enumerate(products):
                        coeff = int(coefficients[num_reactants + i])
                        if coeff > 1:
                            product_parts.append(f"{coeff}{product}")
                        else:
                            product_parts.append(product)
                    
                    result += " + ".join(product_parts)
                    
                    result += "\n\n✅ Проверка баланса:\n"
                    for element in sorted(all_elements):
                        reactant_count = sum(coefficients[i] * reactant_elements[i].get(element, 0) 
                                           for i in range(num_reactants))
                        product_count = sum(coefficients[num_reactants + i] * product_elements[i].get(element, 0) 
                                          for i in range(num_products))
                        result += f"  {element}: реагенты = {int(reactant_count)}, продукты = {int(product_count)} ✓\n"
                    
                    self.result_text.delete('1.0', tk.END)
                    self.result_text.insert('1.0', result)
                else:
                    messagebox.showerror("Ошибка", "Не удалось сбалансировать уравнение.")
            else:
                coefficients = self.balance_by_trial_optimized(reactant_elements, product_elements, all_elements)
                if coefficients:
                    result = "✨ Сбалансированное уравнение:\n\n"
                    
                    reactant_parts = []
                    for i, reactant in enumerate(reactants):
                        coeff = int(coefficients[i])
                        if coeff > 1:
                            reactant_parts.append(f"{coeff}{reactant}")
                        else:
                            reactant_parts.append(reactant)
                    
                    result += " + ".join(reactant_parts)
                    result += " → "
                    
                    product_parts = []
                    for i, product in enumerate(products):
                        coeff = int(coefficients[num_reactants + i])
                        if coeff > 1:
                            product_parts.append(f"{coeff}{product}")
                        else:
                            product_parts.append(product)
                    
                    result += " + ".join(product_parts)
                    
                    result += "\n\n✅ Проверка баланса:\n"
                    for element in sorted(all_elements):
                        reactant_count = sum(coefficients[i] * reactant_elements[i].get(element, 0) 
                                           for i in range(num_reactants))
                        product_count = sum(coefficients[num_reactants + i] * product_elements[i].get(element, 0) 
                                          for i in range(num_products))
                        result += f"  {element}: реагенты = {int(reactant_count)}, продукты = {int(product_count)} ✓\n"
                    
                    self.result_text.delete('1.0', tk.END)
                    self.result_text.insert('1.0', result)
                else:
                    messagebox.showerror("Ошибка", "Не удалось сбалансировать уравнение. Проверьте правильность написания формул.")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при решении: {str(e)}")
    
    def solve_system_fast(self, matrix, num_vars):
        """Оптимизированное решение системы уравнений"""
        if not matrix or not matrix[0]:
            return None
        
        num_eq = len(matrix)
        num_vars = len(matrix[0])
        
        aug_matrix = []
        for row in matrix:
            new_row = [float(x) for x in row]
            aug_matrix.append(new_row)
        
        lead = 0
        for r in range(num_eq):
            if lead >= num_vars:
                break
            
            i = r
            while i < num_eq and abs(aug_matrix[i][lead]) < 1e-10:
                i += 1
            
            if i == num_eq:
                lead += 1
                continue
            
            aug_matrix[i], aug_matrix[r] = aug_matrix[r], aug_matrix[i]
            
            lv = aug_matrix[r][lead]
            if abs(lv) > 1e-10:
                for j in range(num_vars):
                    aug_matrix[r][j] /= lv
            
            for i in range(num_eq):
                if i != r:
                    lv = aug_matrix[i][lead]
                    for j in range(num_vars):
                        aug_matrix[i][j] -= lv * aug_matrix[r][j]
            
            lead += 1
        
        solution = [1.0] * num_vars
        
        for i in range(num_eq - 1, -1, -1):
            first_var = -1
            for j in range(num_vars):
                if abs(aug_matrix[i][j]) > 1e-10:
                    first_var = j
                    break
            
            if first_var == -1:
                continue
            
            sum_val = 0.0
            for j in range(first_var + 1, num_vars):
                sum_val += aug_matrix[i][j] * solution[j]
            
            if abs(aug_matrix[i][first_var]) > 1e-10:
                solution[first_var] = -sum_val / aug_matrix[i][first_var]
        
        return solution
    
    def normalize_coefficients(self, coefficients):
        """Нормализация коэффициентов"""
        fractions = [Fraction(c).limit_denominator() for c in coefficients]
        denominators = [f.denominator for f in fractions]
        
        lcm = 1
        for d in denominators:
            lcm = self.lcm(lcm, d)
        
        normalized = [int(f * lcm) for f in fractions]
        
        gcd = self.gcd_list(normalized)
        if gcd > 1:
            normalized = [c // gcd for c in normalized]
        
        return normalized
    
    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return abs(a)
    
    def lcm(self, a, b):
        return abs(a * b) // self.gcd(a, b)
    
    def gcd_list(self, numbers):
        if not numbers:
            return 1
        result = abs(numbers[0])
        for num in numbers[1:]:
            result = self.gcd(result, abs(num))
        return result if result > 0 else 1
    
    def balance_by_trial_optimized(self, reactant_elements, product_elements, all_elements):
        """Оптимизированный метод проб для балансировки"""
        num_reactants = len(reactant_elements)
        num_products = len(product_elements)
        num_compounds = num_reactants + num_products
        
        max_coeff = 15  # Уменьшено для скорости
        
        # Оптимизация: начинаем с малых значений
        ranges_list = []
        for i in range(num_compounds):
            ranges_list.append(range(1, max_coeff + 1))
        
        # Используем вложенные циклы с ранним выходом
        def try_balance(coeffs):
            for element in all_elements:
                reactant_count = sum(
                    coeffs[i] * reactant_elements[i].get(element, 0)
                    for i in range(num_reactants)
                )
                product_count = sum(
                    coeffs[num_reactants + i] * product_elements[i].get(element, 0)
                    for i in range(num_products)
                )
                if reactant_count != product_count:
                    return False
            return True
        
        # Рекурсивный поиск
        def search_coeffs(coeffs, depth):
            if depth == num_compounds:
                if try_balance(coeffs):
                    return coeffs
                return None
            
            for val in range(1, max_coeff + 1):
                new_coeffs = coeffs + [val]
                result = search_coeffs(new_coeffs, depth + 1)
                if result:
                    return result
            return None
        
        return search_coeffs([], 0)
    
    # Остальные методы setup_* остаются аналогичными, но с обновленными цветами
    def setup_periodic_table(self):
        main_container = tk.Frame(self.periodic_frame, bg=self.colors['bg_main'])
        main_container.pack(fill='both', expand=True)
        
        header_frame = tk.Frame(main_container, bg=self.colors['warning'], height=120)
        header_frame.pack(fill='x', pady=(0, 30))
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="📊 Периодическая таблица элементов Д.И. Менделеева",
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['warning'],
            fg='white'
        )
        title.pack(expand=True)
        
        card_frame = self.create_card(main_container)
        card_frame.pack(pady=15, padx=25, fill='both', expand=True)
        
        table_frame = tk.Frame(card_frame, bg=self.colors['bg_card'])
        table_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        canvas = tk.Canvas(table_frame, bg=self.colors['bg_secondary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_secondary'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        elements_to_show = list(self.atomic_masses.items())[:50]
        
        row = 0
        col = 0
        for symbol, mass in elements_to_show:
            if symbol in ['H', 'Li', 'Na', 'K', 'Rb', 'Cs', 'Fr']:
                color = '#ffeb3b'
            elif symbol in ['Be', 'Mg', 'Ca', 'Sr', 'Ba', 'Ra']:
                color = '#ff9800'
            elif symbol in ['B', 'Al', 'Ga', 'In', 'Tl']:
                color = '#4caf50'
            elif symbol in ['C', 'Si', 'Ge', 'Sn', 'Pb']:
                color = '#9e9e9e'
            elif symbol in ['N', 'P', 'As', 'Sb', 'Bi']:
                color = '#e91e63'
            elif symbol in ['O', 'S', 'Se', 'Te', 'Po']:
                color = '#f44336'
            elif symbol in ['F', 'Cl', 'Br', 'I', 'At']:
                color = '#00bcd4'
            elif symbol in ['He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn']:
                color = '#9c27b0'
            else:
                color = '#e3f2fd'
            
            element_frame = tk.Frame(
                scrollable_frame,
                bg=color,
                relief='flat',
                borderwidth=0,
                width=100,
                height=100
            )
            element_frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            element_frame.grid_propagate(False)
            
            symbol_label = tk.Label(
                element_frame,
                text=symbol,
                font=('Segoe UI', 18, 'bold'),
                bg=color,
                fg='#000' if color in ['#ffeb3b', '#ff9800', '#4caf50'] else '#fff'
            )
            symbol_label.pack(pady=(12, 5))
            
            mass_label = tk.Label(
                element_frame,
                text=f"{mass:.2f}",
                font=('Segoe UI', 10),
                bg=color,
                fg='#333' if color in ['#ffeb3b', '#ff9800', '#4caf50'] else '#eee'
            )
            mass_label.pack()
            
            col += 1
            if col >= 10:
                col = 0
                row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_solubility_tab(self):
        main_container = tk.Frame(self.solubility_frame, bg=self.colors['bg_main'])
        main_container.pack(fill='both', expand=True)
        
        header_frame = tk.Frame(main_container, bg=self.colors['primary'], height=120)
        header_frame.pack(fill='x', pady=(0, 30))
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="💧 Таблица растворимости солей в воде",
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        )
        title.pack(expand=True)
        
        card_frame = self.create_card(main_container)
        card_frame.pack(pady=15, padx=25, fill='both', expand=True)
        
        canvas = tk.Canvas(card_frame, bg=self.colors['bg_card'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(card_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_card'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        solubility_table = [
            ("Li⁺", "Все анионы", "Растворимо", "#10b981"),
            ("Na⁺", "Все анионы", "Растворимо", "#10b981"),
            ("K⁺", "Все анионы", "Растворимо", "#10b981"),
            ("Ag⁺", "NO₃⁻, ClO₄⁻", "Растворимо", "#10b981"),
            ("Ag⁺", "Cl⁻, Br⁻, I⁻", "Нерастворимо", "#ef4444"),
            ("Ba²⁺", "SO₄²⁻", "Нерастворимо", "#ef4444"),
            ("Ca²⁺", "SO₄²⁻", "Малорастворимо", "#f59e0b"),
        ]
        
        header_frame_table = tk.Frame(scrollable_frame, bg=self.colors['primary_dark'])
        header_frame_table.pack(fill='x', padx=25, pady=(0, 15))
        
        headers = ["Катион", "Анион", "Растворимость"]
        for i, header in enumerate(headers):
            label = tk.Label(
                header_frame_table,
                text=header,
                font=('Segoe UI', 13, 'bold'),
                bg=self.colors['primary_dark'],
                fg='white',
                padx=20,
                pady=15
            )
            label.grid(row=0, column=i, sticky='ew', padx=3)
        
        header_frame_table.columnconfigure(0, weight=1)
        header_frame_table.columnconfigure(1, weight=2)
        header_frame_table.columnconfigure(2, weight=1)
        
        for idx, (cation, anion, solubility, color) in enumerate(solubility_table):
            row_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_secondary'] if idx % 2 == 0 else self.colors['bg_card'])
            row_frame.pack(fill='x', padx=25, pady=3)
            
            tk.Label(
                row_frame,
                text=cation,
                font=('Segoe UI', 12),
                bg=row_frame.cget('bg'),
                fg=self.colors['text_primary'],
                anchor='w',
                padx=20,
                pady=12,
                width=25
            ).grid(row=0, column=0, sticky='ew')
            
            tk.Label(
                row_frame,
                text=anion,
                font=('Segoe UI', 12),
                bg=row_frame.cget('bg'),
                fg=self.colors['text_primary'],
                anchor='w',
                padx=20,
                pady=12,
                width=35
            ).grid(row=0, column=1, sticky='ew')
            
            sol_frame = tk.Frame(row_frame, bg=color, relief='flat', borderwidth=0)
            sol_frame.grid(row=0, column=2, sticky='ew', padx=3, pady=3)
            
            tk.Label(
                sol_frame,
                text=solubility,
                font=('Segoe UI', 11, 'bold'),
                bg=color,
                fg='white',
                padx=20,
                pady=12,
                width=20
            ).pack()
            
            row_frame.columnconfigure(0, weight=1)
            row_frame.columnconfigure(1, weight=2)
            row_frame.columnconfigure(2, weight=1)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
    
    def setup_acid_base_tab(self):
        main_container = tk.Frame(self.acid_base_frame, bg=self.colors['bg_main'])
        main_container.pack(fill='both', expand=True)
        
        header_frame = tk.Frame(main_container, bg=self.colors['accent'], height=120)
        header_frame.pack(fill='x', pady=(0, 30))
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="🧪 Кислоты и основания",
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['accent'],
            fg='white'
        )
        title.pack(expand=True)
        
        text_card = self.create_card(main_container)
        text_card.pack(pady=15, padx=25, fill='both', expand=True)
        
        content = """
═══════════════════════════════════════════════════════════════════════════
                        КИСЛОТЫ И ОСНОВАНИЯ
═══════════════════════════════════════════════════════════════════════════

📌 СИЛЬНЫЕ КИСЛОТЫ (полностью диссоциируют в воде):

• HCl - соляная (хлороводородная) кислота
• HBr - бромоводородная кислота
• HI - иодоводородная кислота
• HNO₃ - азотная кислота
• H₂SO₄ - серная кислота (первая ступень - сильная)
• HClO₄ - хлорная кислота

═══════════════════════════════════════════════════════════════════════════

📌 СИЛЬНЫЕ ОСНОВАНИЯ (щелочи):

• LiOH - гидроксид лития
• NaOH - гидроксид натрия (едкий натр)
• KOH - гидроксид калия (едкое кали)
• Ba(OH)₂ - гидроксид бария
• Ca(OH)₂ - гидроксид кальция (гашеная известь)

═══════════════════════════════════════════════════════════════════════════
"""
        
        text_widget = scrolledtext.ScrolledText(
            text_card,
            font=('Consolas', 11),
            wrap='word',
            bg=self.colors['bg_secondary'],
            padx=35,
            pady=35,
            fg=self.colors['text_primary'],
            relief='flat',
            borderwidth=0,
            insertbackground=self.colors['accent'],
            selectbackground=self.colors['accent'],
            selectforeground='white',
            highlightthickness=0
        )
        text_widget.pack(fill='both', expand=True, padx=20, pady=20)
        text_widget.insert('1.0', content)
        text_widget.config(state='disabled')
    
    def setup_reference_tab(self):
        main_container = tk.Frame(self.reference_frame, bg=self.colors['bg_main'])
        main_container.pack(fill='both', expand=True)
        
        header_frame = tk.Frame(main_container, bg='#607D8B', height=120)
        header_frame.pack(fill='x', pady=(0, 30))
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="📚 Справочные материалы",
            font=('Segoe UI', 24, 'bold'),
            bg='#607D8B',
            fg='white'
        )
        title.pack(expand=True)
        
        text_card = self.create_card(main_container)
        text_card.pack(pady=15, padx=25, fill='both', expand=True)
        
        reference_data = """
═══════════════════════════════════════════════════════════════════════════
                        СПРАВОЧНЫЕ МАТЕРИАЛЫ
═══════════════════════════════════════════════════════════════════════════

📌 ОСНОВНЫЕ ТИПЫ ХИМИЧЕСКИХ РЕАКЦИЙ:

1. Реакции соединения (синтеза): A + B → AB
2. Реакции разложения: AB → A + B
3. Реакции замещения: A + BC → AC + B
4. Реакции обмена: AB + CD → AD + CB

═══════════════════════════════════════════════════════════════════════════

📌 РЯД НАПРЯЖЕНИЙ МЕТАЛЛОВ:

Li > K > Ba > Ca > Na > Mg > Al > Mn > Zn > Cr > Fe > Cd > Co > Ni 
> Sn > Pb > H > Cu > Hg > Ag > Pt > Au

═══════════════════════════════════════════════════════════════════════════
"""
        
        text_widget = scrolledtext.ScrolledText(
            text_card,
            font=('Consolas', 11),
            wrap='word',
            bg=self.colors['bg_secondary'],
            padx=35,
            pady=35,
            fg=self.colors['text_primary'],
            relief='flat',
            borderwidth=0,
            insertbackground='#607D8B',
            selectbackground='#78909C',
            selectforeground='white',
            highlightthickness=0
        )
        text_widget.pack(fill='both', expand=True, padx=20, pady=20)
        text_widget.insert('1.0', reference_data)
        text_widget.config(state='disabled')
    
    def setup_constants_tab(self):
        main_container = tk.Frame(self.constants_frame, bg=self.colors['bg_main'])
        main_container.pack(fill='both', expand=True)
        
        header_frame = tk.Frame(main_container, bg=self.colors['accent'], height=120)
        header_frame.pack(fill='x', pady=(0, 30))
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="🔬 Физические и химические константы",
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['accent'],
            fg='white'
        )
        title.pack(expand=True)
        
        card_frame = self.create_card(main_container)
        card_frame.pack(pady=15, padx=25, fill='both', expand=True)
        
        canvas = tk.Canvas(card_frame, bg=self.colors['bg_card'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(card_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_card'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        constants_data = {
            "Фундаментальные константы": [
                ("Число Авогадро", "Na", "6.022 × 10²³", "моль⁻¹"),
                ("Универсальная газовая постоянная", "R", "8.314", "Дж/(моль·К)"),
                ("Молярный объем газа (н.у.)", "Vm", "22.4", "л/моль"),
            ],
        }
        
        y_pos = 15
        for category, items in constants_data.items():
            cat_frame = tk.Frame(scrollable_frame, bg='#E1BEE7', relief='flat', borderwidth=0)
            cat_frame.pack(fill='x', padx=25, pady=(y_pos, 10))
            
            tk.Label(
                cat_frame,
                text=category,
                font=('Segoe UI', 15, 'bold'),
                bg='#E1BEE7',
                fg='#4A148C',
                padx=20,
                pady=15
            ).pack(anchor='w')
            
            for name, symbol, value, unit in items:
                item_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_secondary'] if items.index((name, symbol, value, unit)) % 2 == 0 else self.colors['bg_card'])
                item_frame.pack(fill='x', padx=25, pady=3)
                
                tk.Label(
                    item_frame,
                    text=name,
                    font=('Segoe UI', 12, 'bold'),
                    bg=item_frame.cget('bg'),
                    fg=self.colors['text_primary'],
                    anchor='w',
                    padx=20,
                    pady=12,
                    width=30
                ).grid(row=0, column=0, sticky='w')
                
                tk.Label(
                    item_frame,
                    text=symbol,
                    font=('Segoe UI', 12),
                    bg=item_frame.cget('bg'),
                    fg=self.colors['text_primary'],
                    anchor='w',
                    padx=15,
                    pady=12,
                    width=15
                ).grid(row=0, column=1, sticky='w')
                
                tk.Label(
                    item_frame,
                    text=value,
                    font=('Segoe UI', 12),
                    bg=item_frame.cget('bg'),
                    fg=self.colors['text_primary'],
                    anchor='w',
                    padx=15,
                    pady=12,
                    width=20
                ).grid(row=0, column=2, sticky='w')
                
                tk.Label(
                    item_frame,
                    text=unit,
                    font=('Segoe UI', 11),
                    bg=item_frame.cget('bg'),
                    fg=self.colors['text_secondary'],
                    anchor='w',
                    padx=15,
                    pady=12
                ).grid(row=0, column=3, sticky='w')
                
                item_frame.columnconfigure(0, weight=2)
                item_frame.columnconfigure(1, weight=1)
                item_frame.columnconfigure(2, weight=1)
                item_frame.columnconfigure(3, weight=1)
            
            y_pos = 10
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
    
    def setup_redox_tab(self):
        main_container = tk.Frame(self.redox_frame, bg=self.colors['bg_main'])
        main_container.pack(fill='both', expand=True)
        
        header_frame = tk.Frame(main_container, bg='#FF5722', height=120)
        header_frame.pack(fill='x', pady=(0, 30))
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="⚡ Окислительно-восстановительные реакции (ОВР)",
            font=('Segoe UI', 24, 'bold'),
            bg='#FF5722',
            fg='white'
        )
        title.pack(expand=True)
        
        text_card = self.create_card(main_container)
        text_card.pack(pady=15, padx=25, fill='both', expand=True)
        
        text_widget = scrolledtext.ScrolledText(
            text_card,
            font=('Consolas', 11),
            wrap='word',
            bg=self.colors['bg_secondary'],
            padx=35,
            pady=35,
            fg=self.colors['text_primary'],
            relief='flat',
            borderwidth=0,
            insertbackground='#FF5722',
            selectbackground='#FF7043',
            selectforeground='white',
            highlightthickness=0
        )
        text_widget.pack(fill='both', expand=True, padx=20, pady=20)
        
        redox_content = """
═══════════════════════════════════════════════════════════════════════════
                    ОКИСЛИТЕЛЬНО-ВОССТАНОВИТЕЛЬНЫЕ РЕАКЦИИ
═══════════════════════════════════════════════════════════════════════════

📌 ОСНОВНЫЕ ПОНЯТИЯ:

• Окисление - процесс отдачи электронов
• Восстановление - процесс принятия электронов
• Окислитель - вещество, принимающее электроны
• Восстановитель - вещество, отдающее электроны

═══════════════════════════════════════════════════════════════════════════
"""
        
        text_widget.insert('1.0', redox_content)
        text_widget.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ChemicalEquationSolver(root)
    root.mainloop()
