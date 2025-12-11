#!/bin/bash
# Скрипт для автоматического деплоя на Render.com

echo "🚀 Подготовка к деплою на Render.com..."

# Проверка наличия файлов
if [ ! -f "simple_web_app.py" ]; then
    echo "❌ Ошибка: файл simple_web_app.py не найден!"
    exit 1
fi

if [ ! -f "requirements_web.txt" ]; then
    echo "❌ Ошибка: файл requirements_web.txt не найден!"
    exit 1
fi

if [ ! -f "advanced_neural_chemistry.py" ]; then
    echo "❌ Ошибка: файл advanced_neural_chemistry.py не найден!"
    exit 1
fi

echo "✅ Все необходимые файлы найдены"

# Проверка git
if ! command -v git &> /dev/null; then
    echo "❌ Git не установлен. Установите Git для продолжения."
    exit 1
fi

echo ""
echo "📋 Инструкции по деплою:"
echo "1. Создайте репозиторий на GitHub"
echo "2. Выполните следующие команды:"
echo ""
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial commit'"
echo "   git branch -M main"
echo "   git remote add origin https://github.com/ВАШ_USERNAME/chemistry-ai-web-app.git"
echo "   git push -u origin main"
echo ""
echo "3. Перейдите на render.com и создайте новый Web Service"
echo "4. Подключите ваш GitHub репозиторий"
echo "5. Render автоматически обнаружит конфигурацию и задеплоит приложение"
echo ""
echo "📖 Подробная инструкция в файле DEPLOY_RENDER.md"


