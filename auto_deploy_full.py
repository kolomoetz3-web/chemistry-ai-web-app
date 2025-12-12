#!/usr/bin/env python3
"""
Полностью автоматический деплой на Render.com
Выполняет все возможные шаги автоматически
"""

import os
import subprocess
import sys
import json
import requests
from pathlib import Path

def run_command(cmd, check=True):
    """Выполнить команду и вернуть результат"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        if check and result.returncode != 0:
            print(f"❌ Ошибка: {result.stderr}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ Ошибка выполнения команды: {e}")
        return None

def check_files():
    """Проверка наличия необходимых файлов"""
    required_files = [
        'simple_web_app.py',
        'advanced_neural_chemistry.py',
        'requirements_web.txt',
        'render.yaml'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"❌ Отсутствуют файлы: {', '.join(missing)}")
        return False
    
    print("✅ Все необходимые файлы найдены")
    return True

def init_git():
    """Инициализация git репозитория"""
    if os.path.exists('.git'):
        print("✅ Git репозиторий уже инициализирован")
        return True
    
    print("📦 Инициализация Git репозитория...")
    run_command("git init")
    run_command('git config user.name "Chemistry AI Bot"')
    run_command('git config user.email "bot@chemistry-ai.local"')
    print("✅ Git репозиторий инициализирован")
    return True

def create_github_repo_via_cli():
    """Создание репозитория через GitHub CLI"""
    print("🔍 Проверка GitHub CLI...")
    gh_check = run_command("gh --version", check=False)
    
    if gh_check:
        print("✅ GitHub CLI найден")
        repo_name = "chemistry-ai-web-app"
        
        print(f"📦 Создание репозитория {repo_name} на GitHub...")
        result = run_command(f'gh repo create {repo_name} --public --source=. --remote=origin --push', check=False)
        
        if result is not None:
            print("✅ Репозиторий создан и код загружен!")
            return True
        else:
            print("⚠️  Не удалось создать репозиторий через CLI")
            return False
    else:
        print("⚠️  GitHub CLI не найден")
        return False

def commit_and_push():
    """Коммит и пуш изменений"""
    print("📝 Добавление файлов в Git...")
    run_command("git add .")
    
    print("💾 Создание коммита...")
    run_command('git commit -m "Deploy to Render.com"')
    
    # Проверка наличия remote
    remote_check = run_command("git remote get-url origin", check=False)
    if remote_check:
        print("🚀 Отправка изменений на GitHub...")
        result = run_command("git push -u origin main", check=False)
        if result is not None:
            print("✅ Код загружен на GitHub!")
            return True
    
    print("⚠️  Remote origin не настроен")
    return False

def create_render_service_via_api():
    """Создание сервиса на Render через API"""
    print("🔍 Попытка создания сервиса через Render API...")
    print("⚠️  Для автоматического создания нужен Render API ключ")
    print("📖 Инструкция: https://render.com/docs/api")
    return False

def main():
    print("="*60)
    print("🚀 ПОЛНОСТЬЮ АВТОМАТИЧЕСКИЙ ДЕПЛОЙ НА RENDER.COM")
    print("="*60)
    print()
    
    # Шаг 1: Проверка файлов
    if not check_files():
        print("\n❌ Исправьте ошибки и попробуйте снова")
        sys.exit(1)
    
    # Шаг 2: Инициализация Git
    if not init_git():
        print("\n❌ Ошибка инициализации Git")
        sys.exit(1)
    
    # Шаг 3: Попытка создать репозиторий через GitHub CLI
    repo_created = create_github_repo_via_cli()
    
    if not repo_created:
        # Шаг 4: Коммит и пуш (если remote уже настроен)
        commit_and_push()
        
        print("\n" + "="*60)
        print("📋 РУЧНЫЕ ШАГИ (если автоматизация не сработала):")
        print("="*60)
        print("\n1. Создайте репозиторий на GitHub:")
        print("   https://github.com/new")
        print("   Название: chemistry-ai-web-app")
        print()
        print("2. Выполните команды:")
        print("   git add .")
        print("   git commit -m 'Deploy to Render.com'")
        print("   git branch -M main")
        print("   git remote add origin https://github.com/ВАШ_USERNAME/chemistry-ai-web-app.git")
        print("   git push -u origin main")
        print()
        print("3. На Render.com:")
        print("   - New + → Blueprint")
        print("   - Подключите репозиторий")
        print("   - Apply")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("✅ КОД ЗАГРУЖЕН НА GITHUB!")
        print("="*60)
        print("\n📋 СЛЕДУЮЩИЙ ШАГ:")
        print("1. Перейдите на https://render.com")
        print("2. New + → Blueprint")
        print("3. Подключите репозиторий chemistry-ai-web-app")
        print("4. Render автоматически обнаружит render.yaml")
        print("5. Нажмите Apply")
        print("6. Дождитесь деплоя (5-10 минут)")
        print("7. Скопируйте URL и обновите telegram_chemistry_bot.py")
        print("="*60)

if __name__ == '__main__':
    main()



