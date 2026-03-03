# 📦 File Synchronization Service

**Сервис синхронизации файлов между локальной папкой и облачным хранилищем.**

## 📋 Требования
- **Язык программирования**: Python 3.9+
- **Библиотеки**: `requests`, `loguru`, `configparser`

## 📁 Структура проекта 
![Структура проекта FileSynchronizationService.png](%D0%A1%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%D0%B0%20%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B0%20FileSynchronizationService.png)

## 🚀 Установка
```
1. Клонируйте репозиторий
   git clone https://github.com/skurkova/FileSynchronizationService.git
   cd FileSynchronizationService

2. Создайте виртуальное окружение
   python3 -m venv venv
   source venv/bin/activate 

3. Установите зависимости
   python3 -m pip install -r requirements.txt

4. Настройте конфигурацию, указав необходимые данные: 
   cp config.ini.example config.ini

5. Запустите сервис
   python3 main.py
```

Сервис будет работать в фоновом режиме, с заданной периодичностью проверяя изменения в файлах.
