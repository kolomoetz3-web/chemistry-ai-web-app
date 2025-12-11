#!/usr/bin/env python3
"""
🌐 Telegram Web App для решения химических реакций с ИИ

Flask сервер для веб-приложения, которое работает внутри Telegram
"""

from flask import Flask, render_template, request, jsonify
from advanced_neural_chemistry import solve_chemistry_chatgpt
import json
import os

app = Flask(__name__)

# Хранилище данных пользователей (в памяти, для демо)
user_data = {}

@app.route('/')
def index():
    """Главная страница веб-приложения"""
    return render_template('index.html')

@app.route('/api/solve', methods=['POST'])
def solve_reaction():
    """API для решения химических реакций"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        user_id = data.get('user_id', 'anonymous')

        if not query:
            return jsonify({
                'success': False,
                'error': 'Введите запрос'
            })

        # Используем ChatGPT-стиль ИИ
        result = solve_chemistry_chatgpt(query)

        # Сохраняем в историю пользователя
        if user_id not in user_data:
            user_data[user_id] = {'history': [], 'favorites': []}

        user_data[user_id]['history'].append({
            'query': query,
            'result': result,
            'timestamp': str(data.get('timestamp', ''))
        })

        # Ограничиваем историю
        if len(user_data[user_id]['history']) > 50:
            user_data[user_id]['history'] = user_data[user_id]['history'][-50:]

        return jsonify({
            'success': True,
            'result': result,
            'query': query
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/history/<user_id>', methods=['GET'])
def get_history(user_id):
    """Получить историю пользователя"""
    if user_id in user_data:
        return jsonify({
            'success': True,
            'history': user_data[user_id]['history']
        })
    return jsonify({
        'success': True,
        'history': []
    })

@app.route('/api/favorites/<user_id>', methods=['GET'])
def get_favorites(user_id):
    """Получить избранное пользователя"""
    if user_id in user_data:
        return jsonify({
            'success': True,
            'favorites': user_data[user_id]['favorites']
        })
    return jsonify({
        'success': True,
        'favorites': []
    })

@app.route('/api/favorites/<user_id>', methods=['POST'])
def add_favorite(user_id):
    """Добавить в избранное"""
    try:
        data = request.get_json()
        reaction = data.get('reaction', '')

        if user_id not in user_data:
            user_data[user_id] = {'history': [], 'favorites': []}

        if reaction and reaction not in user_data[user_id]['favorites']:
            user_data[user_id]['favorites'].append(reaction)

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Получить примеры реакций"""
    examples = {
        'metal_acid': [
            'Zn + HCl',
            'Fe + H2SO4',
            'Al + HNO3',
            'Ca + HCl'
        ],
        'metal_oxygen': [
            'Na + O2',
            'Ca + O2',
            'Al + O2',
            'Cu + O2'
        ],
        'acid_base': [
            'HCl + NaOH',
            'H2SO4 + KOH',
            'HNO3 + Ca(OH)2',
            'CH3COOH + NaOH'
        ],
        'combustion': [
            'CH4 + O2',
            'C2H6 + O2',
            'C3H8 + O2',
            'H2 + O2'
        ],
        'redox': [
            'MnO2 + HCl',
            'KMnO4 + HCl',
            'Zn + CuSO4',
            'Fe + CuSO4'
        ],
        'decomposition': [
            'CaCO3',
            'Cu(OH)2',
            'H2O2',
            'KClO3'
        ]
    }

    return jsonify({
        'success': True,
        'examples': examples
    })

@app.route('/api/info', methods=['GET'])
def get_info():
    """Информация о приложении"""
    info = {
        'name': 'Chemistry AI Solver',
        'version': '2.0',
        'ai_type': 'ChatGPT-style Neural Network',
        'reactions_count': '100+',
        'reaction_types': '12',
        'features': [
            'Reaction prediction with AI',
            'Educational explanations',
            'Personal history',
            'Interactive examples',
            'Confidence scoring'
        ]
    }

    return jsonify({
        'success': True,
        'info': info
    })

if __name__ == '__main__':
    print("🚀 Запуск Telegram Web App сервера...")
    print("🌐 URL: http://localhost:5000")
    print("📱 Откройте в Telegram Web App")

    # В продакшене используйте HTTPS
    app.run(host='0.0.0.0', port=5000, debug=True)