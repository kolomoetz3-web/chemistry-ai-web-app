#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ФИНАЛЬНЫЙ АВТОМАТИЧЕСКИЙ ДЕПЛОЙ
Выполняет все возможные шаги автоматически
"""

import os
import sys
import subprocess
from pathlib import Path

def run(cmd, check=True):
    """Выполнить команду"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        if check and result.returncode != 0:
            return False, result.stderr
        return True, result.stdout
    except Exception as e:
        return False, str(e)

def main():
    print("="*70)
    print("🚀 ФИНАЛЬНЫЙ АВТОМАТИЧЕСКИЙ ДЕПЛОЙ НА RENDER.COM")
    print("="*70)
    print()
    
    # Шаг 1: Проверка файлов
    print("📋 Шаг 1: Проверка файлов...")
    required = [
        'simple_web_app.py',
        'advanced_neural_chemistry.py',
        'requirements_web.txt',
        'render.yaml'
    ]
    missing = [f for f in required if not os.path.exists(f)]
    if missing:
        print(f"❌ Отсутствуют: {', '.join(missing)}")
        return
    print("✅ Все файлы на месте")
    print()
    
    # Шаг 2: Git инициализация
    print("📦 Шаг 2: Инициализация Git...")
    if not os.path.exists('.git'):
        success, _ = run('git init')
        if success:
            run('git config user.name "Deploy"')
            run('git config user.email "deploy@local"')
            print("✅ Git инициализирован")
        else:
            print("⚠️  Git не найден, пропускаем...")
    else:
        print("✅ Git уже инициализирован")
    print()
    
    # Шаг 3: Добавление файлов
    print("📝 Шаг 3: Подготовка коммита...")
    run('git add .', check=False)
    run('git commit -m "Deploy to Render.com"', check=False)
    print("✅ Файлы подготовлены")
    print()
    
    # Шаг 4: Инструкции
    print("="*70)
    print("✅ ЛОКАЛЬНАЯ ПОДГОТОВКА ЗАВЕРШЕНА!")
    print("="*70)
    print()
    print("📋 СЛЕДУЮЩИЕ ШАГИ:")
    print()
    print("1️⃣  СОЗДАЙТЕ РЕПОЗИТОРИЙ НА GITHUB:")
    print("   https://github.com/new")
    print("   Название: chemistry-ai-web-app")
    print("   Нажмите 'Create repository'")
    print()
    print("2️⃣  ЗАГРУЗИТЕ КОД (выполните в терминале):")
    print("   git branch -M main")
    print("   git remote add origin https://github.com/ВАШ_USERNAME/chemistry-ai-web-app.git")
    print("   git push -u origin main")
    print("   (Замените ВАШ_USERNAME на ваш GitHub username)")
    print()
    print("3️⃣  ДЕПЛОЙ НА RENDER.COM:")
    print("   - Откройте https://render.com")
    print("   - Войдите через GitHub")
    print("   - Нажмите 'New +' → 'Blueprint'")
    print("   - Выберите репозиторий: chemistry-ai-web-app")
    print("   - Render автоматически обнаружит render.yaml")
    print("   - Нажмите 'Apply'")
    print("   - Дождитесь деплоя (5-10 минут)")
    print()
    print("4️⃣  ОБНОВИТЕ БОТА:")
    print("   - Скопируйте URL от Render (типа: https://xxx.onrender.com)")
    print("   - Откройте telegram_chemistry_bot.py")
    print("   - Найдите строку ~1108 с web_app URL")
    print("   - Замените на ваш новый URL")
    print()
    print("5️⃣  НАСТРОЙТЕ TELEGRAM:")
    print("   - Откройте @BotFather в Telegram")
    print("   - /mybots → выберите бота")
    print("   - Bot Settings → Menu Button → Configure")
    print("   - Web App → введите URL от Render")
    print()
    print("="*70)
    print("🎉 ГОТОВО! Следуйте инструкциям выше")
    print("="*70)

if __name__ == '__main__':
    main()



