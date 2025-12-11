#!/usr/bin/env python3
"""
Простая версия веб-приложения для бесплатного хостинга
Оптимизирована для Render.com, Heroku и подобных платформ
"""

from flask import Flask, render_template_string, request, jsonify
import os
from advanced_neural_chemistry import solve_chemistry_chatgpt

app = Flask(__name__)

# HTML шаблон встроен в код для простоты развертывания
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chemistry AI</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
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
        .tabs {
            display: flex;
            border-bottom: 2px solid #e5e7eb;
            margin-bottom: 20px;
        }
        .tab-btn {
            flex: 1;
            padding: 12px;
            border: none;
            background: #f3f4f6;
            cursor: pointer;
            font-size: 14px;
        }
        .tab-btn.active {
            background: #6366f1;
            color: white;
        }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .examples { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 8px; }
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
            <div class="tabs">
                <button class="tab-btn active" onclick="showTab('solve')">🧪 Решить</button>
                <button class="tab-btn" onclick="showTab('examples')">📚 Примеры</button>
                <button class="tab-btn" onclick="showTab('info')">🤖 О ИИ</button>
            </div>

            <div id="solve-tab" class="tab-content active">
                <div class="input-group">
                    <input type="text" id="reaction-input" placeholder="Введите реакцию: Zn + HCl"
                           onkeypress="handleKeyPress(event)">
                    <button onclick="solveReaction()" class="solve-btn">🚀 Решить с ИИ</button>
                </div>
                <div id="result" class="result" style="display: none;"></div>
            </div>

            <div id="examples-tab" class="tab-content">
                <h3>Примеры реакций:</h3>
                <div class="examples">
                    <button onclick="quickSolve('Zn + HCl')">Zn + HCl</button>
                    <button onclick="quickSolve('MnO2 + HCl')">MnO2 + HCl</button>
                    <button onclick="quickSolve('CH4 + O2')">CH4 + O2</button>
                    <button onclick="quickSolve('NaOH + HCl')">NaOH + HCl</button>
                    <button onclick="quickSolve('CaCO3')">CaCO3</button>
                    <button onclick="quickSolve('Fe + CuSO4')">Fe + CuSO4</button>
                </div>
            </div>

            <div id="info-tab" class="tab-content">
                <h3>🤖 О нейронной сети</h3>
                <p>ChatGPT-стиль ИИ для химии:</p>
                <ul>
                    <li>✅ 100+ обученных реакций</li>
                    <li>✅ 12 типов реакций</li>
                    <li>✅ Образовательные объяснения</li>
                    <li>✅ Оценка уверенности</li>
                </ul>
            </div>
        </main>
    </div>

    <script>
        let currentTab = 'solve';

        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));

            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
            currentTab = tabName;
        }

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
            showTab('solve');
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

        // Telegram Web App
        if (window.Telegram && window.Telegram.WebApp) {
            window.Telegram.WebApp.ready();
            window.Telegram.WebApp.expand();
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

        result = solve_chemistry_chatgpt(query)
        return jsonify({'success': True, 'result': result})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

# Для работы на Render.com и других хостингах
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
else:
    # Для gunicorn
    application = app