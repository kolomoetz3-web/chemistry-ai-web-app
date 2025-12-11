#!/usr/bin/env python3
"""
Настройка GitHub репозитория для Chemistry AI Web App
"""

import os
import subprocess
import sys

def create_github_repo():
    """Создание GitHub репозитория"""
    print("🚀 Настройка GitHub репозитория для Chemistry AI")
    print("=" * 50)

    print("\n📋 ШАГ 1: Создание репозитория на GitHub")
    print("1. Откройте https://github.com")
    print("2. Нажмите 'New repository'")
    print("3. Введите данные:")
    print("   • Repository name: chemistry-ai-web-app")
    print("   • Description: Chemistry AI Solver - Neural Network for Chemical Reactions")
    print("   • Public или Private (рекомендую Public для Render.com)")
    print("4. НЕ ставьте галочку 'Add a README file'")
    print("5. Нажмите 'Create repository'")

    repo_url = input("\n🔗 Введите URL созданного репозитория: ").strip()

    if not repo_url:
        print("❌ URL не введен. Попробуйте снова.")
        return

    print(f"\n✅ Репозиторий: {repo_url}")

    return repo_url

def setup_local_repo(repo_url):
    """Настройка локального репозитория"""
    print("\n📋 ШАГ 2: Настройка локального репозитория")

    try:
        # Инициализация git
        print("🔧 Инициализация Git...")
        subprocess.run(["git", "init"], check=True, capture_output=True)

        # Добавление файлов
        print("📁 Добавление файлов...")
        subprocess.run(["git", "add", "."], check=True, capture_output=True)

        # Первый коммит
        print("💾 Создание коммита...")
        subprocess.run(["git", "commit", "-m", "Initial commit: Chemistry AI Web App"], check=True, capture_output=True)

        # Добавление remote
        print("🔗 Подключение к GitHub...")
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True, capture_output=True)

        # Push
        print("⬆️ Отправка на GitHub...")
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True, capture_output=True)

        print("✅ Репозиторий успешно создан и настроен!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка Git: {e}")
        print("Убедитесь, что Git установлен и настроен.")
        return False

def create_deploy_files():
    """Создание файлов для развертывания"""
    print("\n📋 ШАГ 3: Создание файлов развертывания")

    # Создание .gitignore
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Database
*.db
*.sqlite3

# Neural Network models
*.h5
*.pkl
model_*/
"""

    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content.strip())

    # Создание runtime.txt для Render.com
    with open('runtime.txt', 'w') as f:
        f.write('python-3.9.16\n')

    # Создание render.yaml для Render.com
    render_yaml = """
services:
  - type: web
    name: chemistry-ai-web-app
    runtime: python3
    buildCommand: pip install -r requirements.txt
    startCommand: python simple_web_app.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.16
"""

    with open('render.yaml', 'w') as f:
        f.write(render_yaml.strip())

    print("✅ Файлы развертывания созданы")

def show_next_steps(repo_url):
    """Показать следующие шаги"""
    print("\n🎯 СЛЕДУЮЩИЕ ШАГИ:")
    print("=" * 30)

    print("1️⃣ ПЕРЕЙТИ НА RENDER.COM:")
    print("   • Откройте https://render.com")
    print("   • Нажмите 'New +' → 'Web Service'")
    print("   • Подключите ваш GitHub репозиторий")

    print("\n2️⃣ НАСТРОЙКИ В RENDER.COM:")
    print("   • Name: chemistry-ai-web-app")
    print("   • Runtime: Python 3")
    print("   • Build Command: pip install -r requirements.txt")
    print("   • Start Command: python simple_web_app.py")

    print("\n3️⃣ ПОЛУЧЕНИЕ URL:")
    print("   • После развертывания скопируйте URL")
    print("   • Он будет типа: https://chemistry-ai-web-app.onrender.com")

    print("\n4️⃣ BOTFATHER:")
    print("   • Откройте @BotFather")
    print("   • /newapp → Выберите бота")
    print("   • Название: Chemistry AI Solver")
    print("   • Web App → Вставьте ваш URL")

    print(f"\n🔗 ВАШ РЕПОЗИТОРИЙ: {repo_url}")
    print("\n✅ ГОТОВО К РАЗВЕРТЫВАНИЮ!")

def main():
    print("🎉 Chemistry AI - Настройка GitHub репозитория")
    print("=" * 55)

    # Проверка Git
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ Git установлен")
    except:
        print("❌ Git не установлен!")
        print("Скачайте с https://git-scm.com/")
        return

    # Создание репозитория
    repo_url = create_github_repo()
    if not repo_url:
        return

    # Настройка локального репозитория
    if setup_local_repo(repo_url):
        create_deploy_files()
        show_next_steps(repo_url)
    else:
        print("❌ Ошибка настройки репозитория")

if __name__ == "__main__":
    main()