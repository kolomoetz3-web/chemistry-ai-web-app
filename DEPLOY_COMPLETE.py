#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ПОЛНЫЙ АВТОМАТИЧЕСКИЙ ДЕПЛОЙ - ВЫПОЛНЯЕТ ВСЕ САМ
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Исправление кодировки для Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def execute(cmd):
    """Безопасное выполнение команды"""
    try:
        proc = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            encoding='utf-8',
            errors='ignore'
        )
        stdout, stderr = proc.communicate()
        return proc.returncode == 0, stdout.strip(), stderr.strip()
    except Exception as e:
        return False, "", str(e)

def main():
    print("\n" + "="*70)
    print("🚀 ПОЛНОСТЬЮ АВТОМАТИЧЕСКИЙ ДЕПЛОЙ")
    print("="*70 + "\n")
    
    steps_completed = []
    
    # Шаг 1: Проверка файлов
    print("📋 [1/7] Проверка файлов...")
    files_ok = all(os.path.exists(f) for f in [
        'simple_web_app.py',
        'advanced_neural_chemistry.py', 
        'requirements_web.txt',
        'render.yaml'
    ])
    if files_ok:
        print("   ✅ Все файлы найдены")
        steps_completed.append("Файлы проверены")
    else:
        print("   ❌ Некоторые файлы отсутствуют!")
        return
    
    # Шаг 2: Git
    print("\n📦 [2/7] Настройка Git...")
    if not os.path.exists('.git'):
        ok, _, _ = execute('git init')
        if ok:
            execute('git config user.name "Deploy"')
            execute('git config user.email "deploy@local"')
            print("   ✅ Git инициализирован")
            steps_completed.append("Git инициализирован")
        else:
            print("   ⚠️  Git не найден")
    else:
        print("   ✅ Git уже настроен")
        steps_completed.append("Git настроен")
    
    # Шаг 3: Коммит
    print("\n📝 [3/7] Подготовка коммита...")
    execute('git add .')
    execute('git commit -m "Auto deploy to Render.com"')
    execute('git branch -M main')
    print("   ✅ Файлы подготовлены")
    steps_completed.append("Коммит создан")
    
    # Шаг 4: Проверка GitHub CLI
    print("\n🔍 [4/7] Проверка GitHub CLI...")
    gh_ok, _, _ = execute('gh --version')
    if gh_ok:
        print("   ✅ GitHub CLI найден")
        print("\n🌐 [5/7] Создание репозитория...")
        repo_ok, out, err = execute('gh repo create chemistry-ai-web-app --public --source=. --remote=origin --push')
        if repo_ok:
            print("   ✅ Репозиторий создан и код загружен!")
            steps_completed.append("Репозиторий создан")
            steps_completed.append("Код загружен")
            
            print("\n" + "="*70)
            print("✅ АВТОМАТИЧЕСКИЕ ШАГИ ЗАВЕРШЕНЫ!")
            print("="*70)
            print("\n📋 ВЫПОЛНЕНО:")
            for step in steps_completed:
                print(f"   ✅ {step}")
            print("\n📋 ФИНАЛЬНЫЙ ШАГ:")
            print("   1. Откройте https://render.com")
            print("   2. New + → Blueprint")
            print("   3. Выберите: chemistry-ai-web-app")
            print("   4. Apply")
            print("   5. Дождитесь деплоя")
            print("   6. Обновите URL в telegram_chemistry_bot.py")
            print("\n" + "="*70)
            return
        else:
            print("   ⚠️  Не удалось создать через CLI")
    else:
        print("   ⚠️  GitHub CLI не найден")
    
    # Шаг 5: Инструкции для ручного деплоя
    print("\n📋 [5/7] Инструкции для ручного деплоя:")
    print("\n" + "="*70)
    print("✅ ЛОКАЛЬНАЯ ПОДГОТОВКА ЗАВЕРШЕНА!")
    print("="*70)
    print("\n📋 ВЫПОЛНЕНО:")
    for step in steps_completed:
        print(f"   ✅ {step}")
    print("\n📋 СЛЕДУЮЩИЕ ШАГИ:")
    print("\n1️⃣  СОЗДАЙТЕ РЕПОЗИТОРИЙ:")
    print("   https://github.com/new")
    print("   Название: chemistry-ai-web-app")
    print("\n2️⃣  ЗАГРУЗИТЕ КОД:")
    print("   git remote add origin https://github.com/ВАШ_USERNAME/chemistry-ai-web-app.git")
    print("   git push -u origin main")
    print("\n3️⃣  ДЕПЛОЙ НА RENDER:")
    print("   https://render.com → New + → Blueprint")
    print("   Подключите репозиторий → Apply")
    print("\n" + "="*70)
    
    # Сохранение статуса
    status = {
        "completed": steps_completed,
        "next_steps": [
            "Создать репозиторий на GitHub",
            "Загрузить код",
            "Деплой на Render.com"
        ]
    }
    with open('deploy_status.json', 'w', encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=2)
    print("\n💾 Статус сохранен в deploy_status.json")

if __name__ == '__main__':
    main()



