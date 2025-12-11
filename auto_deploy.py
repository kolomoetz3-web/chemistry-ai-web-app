#!/usr/bin/env python3
"""
Автоматический деплой на Render.com
Этот скрипт поможет подготовить проект к деплою
"""

import os
import subprocess
import sys

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

def check_git():
    """Проверка инициализации git"""
    if not os.path.exists('.git'):
        print("⚠️  Git репозиторий не инициализирован")
        return False
    print("✅ Git репозиторий найден")
    return True

def create_readme():
    """Создание README для GitHub"""
    readme_content = """# 🧠 Chemistry AI Web App

Веб-приложение с ИИ для решения химических реакций.

## 🚀 Быстрый старт

Это приложение автоматически деплоится на Render.com при пуше в GitHub.

## 📋 Требования

- Python 3.11+
- Flask
- Все зависимости в `requirements_web.txt`

## 🔧 Локальный запуск

```bash
pip install -r requirements_web.txt
python simple_web_app.py
```

## 🌐 Деплой

Следуйте инструкциям в `DEPLOY_RENDER.md`
"""
    
    if not os.path.exists('README_WEB.md'):
        with open('README_WEB.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("✅ Создан README_WEB.md")
    else:
        print("ℹ️  README_WEB.md уже существует")

def main():
    print("🚀 Подготовка к деплою на Render.com\n")
    
    if not check_files():
        print("\n❌ Исправьте ошибки и попробуйте снова")
        sys.exit(1)
    
    check_git()
    create_readme()
    
    print("\n" + "="*50)
    print("📋 СЛЕДУЮЩИЕ ШАГИ:")
    print("="*50)
    print("\n1. Создайте репозиторий на GitHub:")
    print("   - Перейдите на https://github.com/new")
    print("   - Название: chemistry-ai-web-app")
    print("   - Создайте репозиторий")
    
    print("\n2. Загрузите код в GitHub:")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit'")
    print("   git branch -M main")
    print("   git remote add origin https://github.com/ВАШ_USERNAME/chemistry-ai-web-app.git")
    print("   git push -u origin main")
    
    print("\n3. Деплой на Render.com:")
    print("   - Перейдите на https://render.com")
    print("   - Нажмите 'New +' → 'Blueprint'")
    print("   - Подключите ваш GitHub репозиторий")
    print("   - Render автоматически обнаружит render.yaml")
    print("   - Нажмите 'Apply'")
    
    print("\n4. После деплоя:")
    print("   - Скопируйте URL вашего приложения")
    print("   - Обновите URL в telegram_chemistry_bot.py (строка ~1108)")
    print("   - Настройте Web App в @BotFather")
    
    print("\n📖 Подробная инструкция: DEPLOY_RENDER.md")
    print("="*50)

if __name__ == '__main__':
    main()


