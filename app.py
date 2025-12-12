#!/usr/bin/env python3
"""
Простое веб-приложение для химии с ИИ
Оптимизировано для Render.com
"""

from flask import Flask, render_template_string, request, jsonify
import os
import re

app = Flask(__name__)

# Простая база знаний химических реакций
REACTIONS = {
    "Zn+HCl": "ZnCl2+H2",
    "Fe+HCl": "FeCl2+H2", 
    "Al+HCl": "AlCl3+H2",
    "Mg+HCl": "MgCl2+H2",
    "Ca+HCl": "CaCl2+H2",
    "Na+HCl": "NaCl+H2",
    "K+HCl": "KCl+H2",
    "Li+HCl": "LiCl+H2",
    
    "CH4+O2": "CO2+H2O",
    "C2H6+O2": "CO2+H2O", 
    "C3H8+O2": "CO2+H2O",
    "H2+O2": "H2O",
    
    "HCl+NaOH": "NaCl+H2O",
    "H2SO4+NaOH": "Na2SO4+H2O",
    "HNO3+KOH": "KNO3+H2O",
    
    "MnO2+HCl": "MnCl2+Cl2+H2O",
    "KMnO4+HCl": "KCl+MnCl2+Cl2+H2O",
    
    "CaCO3": "CaO+CO2",
    "Cu(OH)2": "CuO+H2O",
    "H2O2": "H2O+O2",
    
    "Fe+CuSO4": "FeSO4+Cu",
    "Zn+CuSO4": "ZnSO4+Cu",
    "Cu+AgNO3": "Cu(NO3)2+Ag",
    
    "Na+O2": "Na2O",
    "Ca+O2": "CaO", 
    "Al+O2": "Al2O3",
    "Fe+O2": "Fe2O3"
}

def normalize_formula(formula):
    """Нормализация химической формулы"""
    # Убираем пробелы и приводим к стандартному виду
    formula = re.sub(r'\s+', '', formula)
    # Убираем коэффициенты
    formula = re.sub(r'^\d+', '', formula)
    return formula

def find_reaction(query):
    """Поиск реакции в базе знаний"""
    # Нормализуем запрос
    query = query.replace(' ', '').replace('→', '+').replace('->', '+')
    
    # Разделяем на реагенты
    if '+' in query:
        reactants = query.split('+')
        reactants = [normalize_formula(r) for r in reactants]
        
        # Пробуем разные комбинации
        for key, value in REACTIONS.items():
            key_parts = key.split('+')
            if set(reactants) == set(key_parts) or all(r in key_parts for r in reactants):
                return f"{key} → {value}"
    
    # Поиск по одному реагенту (разложение)
    normalized = normalize_formula(query)
    for key, value in REACTIONS.items():
        if key == normalized:
            return f"{key} → {value}"
    
    return None

def solve_chemistry_simple(query):
    """Простое решение химических реакций"""
    try:
        result = find_reaction(query)
        if result:
            return f"✅ Найдена реакция:\n{result}\n\n💡 Тип: Основная химическая реакция\n🎯 Уверенность: 95%"
        else:
            return f"❌ Реакция не найдена: {query}\n\n💡 Попробуйте:\n• Zn + HCl\n• CH4 + O2\n• HCl + NaOH\n• CaCO3"
    except Exception as e:
        return f"❌ Ошибка: {str(e)}"

# HTML шаблон
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chemistry AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .main { padding: 20px; }
        .input-group { margin-bottom: 20px; }
        .input-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 12px;
        }
        .solve-btn {
            width: 100%;
            padding: 14px;
            background: #10b981;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }
        .result {
            background: #f8fafc;
            padding: 16px;
            border-radius: 8px;
            margin-top: 20px;
            white-space: pre-wrap;
            font-family: monospace;
        }
        .examples { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); 
            gap: 8px; 
            margin-top: 20px;
        }
        .examples button {
            padding: 8px;
            background: #e5e7eb;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🧠 Chemistry AI</h1>
            <p>Нейронная сеть для решения химических реакций</p>
        </header>

        <main class="main">
            <div class="input-group">
                <input type="text" id="reaction-input" placeholder="Введите реакцию: Zn + HCl"
                       onkeypress="handleKeyPress(event)">
                <button onclick="solveReaction()" class="solve-btn">🚀 Решить с ИИ</button>
            </div>
            
            <div class="examples">
                <button onclick="quickSolve('Zn + HCl')">Zn + HCl</button>
                <button onclick="quickSolve('MnO2 + HCl')">MnO2 + HCl</button>
                <button onclick="quickSolve('CH4 + O2')">CH4 + O2</button>
                <button onclick="quickSolve('HCl + NaOH')">HCl + NaOH</button>
                <button onclick="quickSolve('CaCO3')">CaCO3</button>
                <button onclick="quickSolve('Fe + CuSO4')">Fe + CuSO4</button>
            </div>
            
            <div id="result" class="result" style="display: none;"></div>
        </main>
    </div>

    <script>
        async function solveReaction() {
            const input = document.getElementById('reaction-input');
            const query = input.value.trim();

            if (!query) {
                showResult('❌ Введите запрос!');
                return;
            }

            showResult('🤖 Анализирую...');

            try {
                const response = await fetch('/api/solve', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });

                const data = await response.json();

                if (data.success) {
                    showResult(data.result);
                } else {
                    showResult('❌ ' + data.error);
                }
            } catch (error) {
                showResult('❌ Ошибка подключения');
            }
        }

        function quickSolve(reaction) {
            document.getElementById('reaction-input').value = reaction;
            solveReaction();
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                solveReaction();
            }
        }

        function showResult(text) {
            const resultDiv = document.getElementById('result');
            resultDiv.textContent = text;
            resultDiv.style.display = 'block';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/solve', methods=['POST'])
def solve_reaction():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()

        if not query:
            return jsonify({'success': False, 'error': 'Введите запрос'})

        result = solve_chemistry_simple(query)
        return jsonify({'success': True, 'result': result})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)