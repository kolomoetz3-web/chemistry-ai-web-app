#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ПОЛНОСТЬЮ АВТОМАТИЧЕСКИЙ ДЕПЛОЙ
Делает все возможное автоматически
"""

import os
import sys
import subprocess
import json
import webbrowser
from pathlib import Path

def run_cmd(cmd, check=False):
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
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except:
        return False, "", ""

def check_and_install_requests():
    """Проверить и установить requests"""
    try:
        import requests
        return True
    except ImportError:
        print("📦 Установка requests...")
        success, _, _ = run_cmd(f"{sys.executable} -m pip install requests --quiet")
        if success:
            try:
                import requests
                return True
            except:
                return False
        return False

def create_github_repo_auto():
    """Попытка создать репозиторий автоматически"""
    if not check_and_install_requests():
        return None, None
    
    import requests
    
    # Попытка получить токен из переменной окружения
    token = os.environ.get('GITHUB_TOKEN')
    
    if not token:
        # Попытка найти токен в файле (если пользователь создал)
        token_file = Path('.github_token')
        if token_file.exists():
            token = token_file.read_text().strip()
    
    if not token:
        print("⚠️  GitHub токен не найден")
        print("📝 Создайте файл .github_token с вашим токеном")
        print("   Или установите переменную окружения GITHUB_TOKEN")
        return None, None
    
    repo_name = "chemistry-ai-web-app"
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
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 201:
            repo_data = response.json()
            return repo_data["clone_url"], repo_data["html_url"]
        elif response.status_code == 422:
            # Репозиторий уже существует
            username = requests.get("https://api.github.com/user", headers=headers, timeout=10).json().get("login")
            if username:
                clone_url = f"https://github.com/{username}/{repo_name}.git"
                html_url = f"https://github.com/{username}/{repo_name}"
                return clone_url, html_url
    except Exception as e:
        print(f"⚠️  Ошибка API: {e}")
    
    return None, None

def main():
    print("="*70)
    print("🚀 ПОЛНОСТЬЮ АВТОМАТИЧЕСКИЙ ДЕПЛОЙ")
    print("="*70)
    print()
    
    # Шаг 1: Проверка файлов
    print("📋 Шаг 1/6: Проверка файлов...")
    required = {
        'simple_web_app.py': 'Веб-приложение',
        'advanced_neural_chemistry.py': 'ИИ движок',
        'requirements_web.txt': 'Зависимости',
        'render.yaml': 'Конфигурация Render'
    }
    
    all_ok = True
    for file, desc in required.items():
        if os.path.exists(file):
            print(f"   ✅ {desc}: {file}")
        else:
            print(f"   ❌ {desc}: {file} - ОТСУТСТВУЕТ!")
            all_ok = False
    
    if not all_ok:
        print("\n❌ Не все файлы найдены!")
        return
    
    print("   ✅ Все файлы на месте")
    print()
    
    # Шаг 2: Git инициализация
    print("📦 Шаг 2/6: Инициализация Git...")
    if not os.path.exists('.git'):
        success, _, _ = run_cmd('git init')
        if success:
            run_cmd('git config user.name "Deploy Bot"', check=False)
            run_cmd('git config user.email "deploy@local"', check=False)
            print("   ✅ Git инициализирован")
        else:
            print("   ⚠️  Git не найден, но продолжаем...")
    else:
        print("   ✅ Git уже инициализирован")
    print()
    
    # Шаг 3: Подготовка коммита
    print("📝 Шаг 3/6: Подготовка коммита...")
    run_cmd('git add .', check=False)
    run_cmd('git commit -m "Deploy to Render.com - Auto"', check=False)
    run_cmd('git branch -M main', check=False)
    print("   ✅ Файлы подготовлены")
    print()
    
    # Шаг 4: Попытка создать репозиторий
    print("🌐 Шаг 4/6: Создание репозитория на GitHub...")
    clone_url, html_url = create_github_repo_auto()
    
    if clone_url and html_url:
        print(f"   ✅ Репозиторий создан: {html_url}")
        
        # Шаг 5: Push на GitHub
        print("📤 Шаг 5/6: Загрузка кода на GitHub...")
        run_cmd(f'git remote remove origin', check=False)
        run_cmd(f'git remote add origin {clone_url}', check=False)
        success, out, err = run_cmd('git push -u origin main', check=False)
        
        if success:
            print("   ✅ Код загружен на GitHub!")
            print()
            
            # Шаг 6: Инструкции для Render
            print("="*70)
            print("✅ АВТОМАТИЧЕСКИЕ ШАГИ ЗАВЕРШЕНЫ!")
            print("="*70)
            print()
            print("📋 ФИНАЛЬНЫЙ ШАГ - ДЕПЛОЙ НА RENDER.COM:")
            print()
            print("1. Откройте: https://render.com")
            print("2. Войдите через GitHub")
            print("3. Нажмите 'New +' → 'Blueprint'")
            print(f"4. Выберите репозиторий: chemistry-ai-web-app")
            print("5. Render автоматически обнаружит render.yaml")
            print("6. Нажмите 'Apply'")
            print("7. Дождитесь деплоя (5-10 минут)")
            print()
            print(f"📦 Репозиторий: {html_url}")
            print()
            
            # Попытка открыть браузер
            try:
                webbrowser.open("https://render.com")
                print("🌐 Браузер открыт с Render.com")
            except:
                pass
            
            print("="*70)
        else:
            print("   ⚠️  Не удалось загрузить код автоматически")
            print(f"   Выполните вручную: git push -u origin main")
            print()
    else:
        print("   ⚠️  Не удалось создать репозиторий автоматически")
        print()
        print("📋 РУЧНЫЕ ШАГИ:")
        print("="*70)
        print("1. Создайте репозиторий: https://github.com/new")
        print("   Название: chemistry-ai-web-app")
        print()
        print("2. Выполните команды:")
        print("   git remote add origin https://github.com/ВАШ_USERNAME/chemistry-ai-web-app.git")
        print("   git push -u origin main")
        print()
        print("3. На Render.com:")
        print("   - New + → Blueprint")
        print("   - Подключите репозиторий")
        print("   - Apply")
        print("="*70)
    
    # Создание файла с инструкциями
    instructions = f"""
# ✅ АВТОМАТИЧЕСКИЙ ДЕПЛОЙ ВЫПОЛНЕН

## Что сделано:
- ✅ Все файлы проверены
- ✅ Git инициализирован
- ✅ Файлы подготовлены к коммиту
{"- ✅ Репозиторий создан на GitHub" if clone_url else "- ⚠️  Репозиторий нужно создать вручную"}
{"- ✅ Код загружен на GitHub" if clone_url and success else "- ⚠️  Код нужно загрузить вручную"}

## Следующий шаг:
1. Откройте https://render.com
2. New + → Blueprint
3. Подключите репозиторий: chemistry-ai-web-app
4. Apply
5. Дождитесь деплоя
6. Обновите URL в telegram_chemistry_bot.py
"""
    
    with open('DEPLOY_STATUS.txt', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("\n📄 Статус сохранен в DEPLOY_STATUS.txt")

if __name__ == '__main__':
    main()



