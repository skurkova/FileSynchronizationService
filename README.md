# File Synchronization Service

**Сервис синхронизации файлов между локальной папкой и Яндекс.Диском.**

## Требования
- Python 3.11+
- Библиотеки: `requests`, `loguru`, `configparser`

## Установка
```bash
# 1. Клонируйте репозиторий
git clone https://github.com/skurkova/FileSynchronizationService.git
cd FileSynchronizationService

# 2. Создайте виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate 

# 3. Установите зависимости
pip install requirements.txt

# 4. Настройте конфигурацию: укажите свои пути и токен
cp config.ini.example config.ini

# 5. Запустите сервис
python main.py