#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import subprocess

def run(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        return result.returncode == 0
    except:
        return False

print("="*70)
print("🚀 ВЫПОЛНЕНИЕ АВТОМАТИЧЕСКОГО ДЕПЛОЯ")
print("="*70)

# Проверка файлов
print("\n[1/5] Проверка файлов...")
files = ['simple_web_app.py', 'advanced_neural_chemistry.py', 'requirements_web.txt', 'render.yaml']
if all(os.path.exists(f) for f in files):
    print("✅ Все файлы найдены")
else:
    print("❌ Файлы отсутствуют")
    sys.exit(1)

# Git init
print("\n[2/5] Инициализация Git...")
if not os.path.exists('.git'):
    if run('git init'):
        run('git config user.name "Deploy"')
        run('git config user.email "deploy@local"')
        print("✅ Git инициализирован")
    else:
        print("⚠️  Git не найден")
else:
    print("✅ Git уже настроен")

# Git add & commit
print("\n[3/5] Создание коммита...")
run('git add .')
run('git commit -m "Deploy to Render.com"')
run('git branch -M main')
print("✅ Коммит создан")

# Попытка GitHub CLI
print("\n[4/5] Попытка создать репозиторий...")
if run('gh repo create chemistry-ai-web-app --public --source=. --remote=origin --push'):
    print("✅ Репозиторий создан и код загружен!")
    print("\n" + "="*70)
    print("✅ ГОТОВО! Теперь на Render.com:")
    print("   1. New + → Blueprint")
    print("   2. Выберите: chemistry-ai-web-app")
    print("   3. Apply")
    print("="*70)
else:
    print("⚠️  GitHub CLI не найден или требуется авторизация")
    print("\n" + "="*70)
    print("📋 РУЧНЫЕ ШАГИ:")
    print("   1. https://github.com/new → chemistry-ai-web-app")
    print("   2. git remote add origin https://github.com/ВАШ_USERNAME/chemistry-ai-web-app.git")
    print("   3. git push -u origin main")
    print("   4. https://render.com → New + → Blueprint")
    print("="*70)

print("\n[5/5] ✅ Локальная подготовка завершена!")



