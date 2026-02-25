# File Synchronization Service

**Сервис синхронизации файлов между локальной папкой и облачным хранилищем.**

## Требования
- **Язык программирования**: Python 3.9+
- **Библиотеки**: `requests`, `loguru`, `configparser`

## Установка
```bash
# 1. Клонируйте репозиторий
git clone https://github.com/skurkova/FileSynchronizationService.git
cd FileSynchronizationService

# 2. Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate 

# 3. Установите зависимости
python3 -m pip install -r requirements.txt

# 4. Настройте конфигурацию, указав необходимые данные: 
cp config.ini.example config.ini

# 5. Запустите сервис
python3 main.py