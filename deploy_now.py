#!/usr/bin/env python3
"""
Автоматический деплой на Render.com через GitHub
Использует GitHub API для создания репозитория
"""

import os
import subprocess
import sys
import json
import base64
from pathlib import Path

try:
    import requests
except ImportError:
    print("❌ Установите requests: pip install requests")
    sys.exit(1)

def run_cmd(cmd):
    """Выполнить команду"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_git():
    """Проверка Git"""
    success, _, _ = run_cmd("git --version")
    return success

def init_git_repo():
    """Инициализация Git репозитория"""
    if os.path.exists('.git'):
        print("✅ Git уже инициализирован")
        return True
    
    print("📦 Инициализация Git...")
    success, _, _ = run_cmd("git init")
    if success:
        run_cmd('git config user.name "Deploy Bot"')
        run_cmd('git config user.email "deploy@local"')
        print("✅ Git инициализирован")
        return True
    return False

def create_github_repo(token, repo_name="chemistry-ai-web-app"):
    """Создание репозитория на GitHub через API"""
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "description": "Chemistry AI Web App - Neural Network for Chemical Reactions",
        "private": False,
        "auto_init": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            repo_data = response.json()
            return True, repo_data["clone_url"], repo_data["html_url"]
        else:
            return False, None, f"Ошибка: {response.status_code} - {response.text}"
    except Exception as e:
        return False, None, str(e)

def push_to_github(repo_url):
    """Отправка кода на GitHub"""
    print("📤 Отправка кода на GitHub...")
    
    # Добавление remote
    run_cmd(f'git remote remove origin')
    success, _, _ = run_cmd(f'git remote add origin {repo_url}')
    if not success:
        return False
    
    # Добавление файлов
    run_cmd("git add .")
    
    # Коммит
    run_cmd('git commit -m "Deploy to Render.com"')
    
    # Создание ветки main
    run_cmd("git branch -M main")
    
    # Push
    success, _, err = run_cmd("git push -u origin main")
    return success

def main():
    print("="*60)
    print("🚀 АВТОМАТИЧЕСКИЙ ДЕПЛОЙ НА RENDER.COM")
    print("="*60)
    print()
    
    # Проверка Git
    if not check_git():
        print("❌ Git не установлен. Установите Git: https://git-scm.com/")
        sys.exit(1)
    
    # Инициализация Git
    if not init_git_repo():
        print("❌ Ошибка инициализации Git")
        sys.exit(1)
    
    # Запрос GitHub токена
    print("\n📋 Для автоматического создания репозитория нужен GitHub токен:")
    print("   1. Перейдите: https://github.com/settings/tokens")
    print("   2. Generate new token (classic)")
    print("   3. Выберите scope: repo")
    print("   4. Скопируйте токен")
    print()
    
    token = input("Введите GitHub токен (или Enter для пропуска): ").strip()
    
    if token:
        repo_name = input("Название репозитория [chemistry-ai-web-app]: ").strip() or "chemistry-ai-web-app"
        
        print(f"\n📦 Создание репозитория {repo_name}...")
        success, clone_url, info = create_github_repo(token, repo_name)
        
        if success:
            print(f"✅ Репозиторий создан: {info}")
            
            # Push кода
            if push_to_github(clone_url):
                print("✅ Код загружен на GitHub!")
                print("\n" + "="*60)
                print("✅ ГОТОВО! СЛЕДУЮЩИЕ ШАГИ:")
                print("="*60)
                print(f"1. Перейдите на Render.com: https://render.com")
                print("2. New + → Blueprint")
                print(f"3. Подключите репозиторий: {repo_name}")
                print("4. Render автоматически обнаружит render.yaml")
                print("5. Нажмите Apply")
                print("6. Дождитесь деплоя (5-10 минут)")
                print("7. Скопируйте URL и обновите telegram_chemistry_bot.py")
                print("="*60)
            else:
                print("⚠️  Код не загружен. Выполните вручную:")
                print(f"   git remote add origin {clone_url}")
                print("   git add .")
                print("   git commit -m 'Deploy'")
                print("   git branch -M main")
                print("   git push -u origin main")
        else:
            print(f"❌ Ошибка создания репозитория: {info}")
    else:
        print("\n📋 РУЧНЫЕ ШАГИ:")
        print("="*60)
        print("1. Создайте репозиторий: https://github.com/new")
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

if __name__ == '__main__':
    main()


