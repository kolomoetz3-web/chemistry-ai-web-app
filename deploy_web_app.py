#!/usr/bin/env python3
"""
🚀 Скрипт для развертывания Telegram Web App

Инструкции по развертыванию веб-приложения на различных платформах
"""

import os
import subprocess
import sys

def check_requirements():
    """Проверка наличия необходимых зависимостей"""
    print("📦 Проверка зависимостей...")

    required_packages = [
        'flask',
        'tensorflow',
        'numpy',
        'pandas',
        'scikit-learn'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")

    if missing_packages:
        print(f"\n⚠️  Отсутствующие пакеты: {', '.join(missing_packages)}")
        print("Установите их командой:")
        print(f"pip install {' '.join(missing_packages)}")
        return False

    print("✅ Все зависимости установлены!")
    return True

def run_local_server():
    """Запуск локального сервера для тестирования"""
    print("🌐 Запуск локального сервера...")
    print("📱 Веб-приложение будет доступно по адресу:")
    print("http://localhost:5000")
    print()
    print("📋 Инструкции:")
    print("1. Откройте браузер")
    print("2. Перейдите по ссылке выше")
    print("3. Протестируйте приложение")
    print("4. Для остановки нажмите Ctrl+C")
    print()

    # Запуск Flask сервера
    os.system("python web_app.py")

def create_deployment_guide():
    """Создание руководства по развертыванию"""
    print("🚀 РУКОВОДСТВО ПО РАЗВЕРТЫВАНИЮ")
    print("=" * 50)

    print("\n1️⃣ ЛОКАЛЬНЫЙ ЗАПУСК:")
    print("python web_app.py")
    print("URL: http://localhost:5000")

    print("\n2️⃣ RENDER.COM (Бесплатно):")
    print("• Зарегистрируйтесь на render.com")
    print("• Создайте новый Web Service")
    print("• Подключите GitHub репозиторий")
    print("• Настройки:")
    print("  - Runtime: Python 3")
    print("  - Build Command: pip install -r requirements.txt")
    print("  - Start Command: python web_app.py")
    print("• Получите URL типа: https://your-app.onrender.com")

    print("\n3️⃣ HEROKU:")
    print("• Установите Heroku CLI")
    print("• Создайте приложение: heroku create")
    print("• Разверните: git push heroku main")
    print("• URL: https://your-app.herokuapp.com")

    print("\n4️⃣ PYTHONANYWHERE.COM:")
    print("• Зарегистрируйтесь на pythonanywhere.com")
    print("• Создайте новое веб-приложение")
    print("• Загрузите файлы через FTP или Git")
    print("• Настройте WSGI файл")

    print("\n5️⃣ НАСТРОЙКА БОТА:")
    print("• В коде бота замените URL:")
    print('  web_app={"url": "https://your-app.onrender.com"}')
    print("• Перезапустите бота")

    print("\n📱 ТЕСТИРОВАНИЕ:")
    print("• Откройте Telegram")
    print("• Найдите вашего бота")
    print("• Отправьте /start")
    print("• Нажмите '🌐 Открыть Веб-Приложение'")
    print("• Приложение откроется внутри Telegram!")

def main():
    print("🚀 Chemistry AI Web App - Развертывание")
    print("=" * 50)

    if not check_requirements():
        return

    print("\nВыберите действие:")
    print("1. Запустить локально для тестирования")
    print("2. Показать руководство по развертыванию")
    print("3. Выход")

    choice = input("\nВаш выбор (1-3): ").strip()

    if choice == "1":
        run_local_server()
    elif choice == "2":
        create_deployment_guide()
    elif choice == "3":
        print("👋 До свидания!")
    else:
        print("❌ Неверный выбор. Попробуйте снова.")
        main()

if __name__ == "__main__":
    main()