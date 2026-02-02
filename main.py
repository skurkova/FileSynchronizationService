import os
import sys
import time
import datetime
import configparser

from loguru import logger

from cloud_service import CloudService


def setup_logging(log_file: str) -> None:
    """Настраиваем логгер"""
    logger.remove()
    log_format = 'FileSynchronizationService:{name}({function}) | {time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}'
    logger.add(sys.stderr, format=log_format)
    logger.add(log_file,
               format=log_format,
               rotation="10 MB",
               retention="1 month",
               compression="zip")


def run_cloud_service(local_folder: str, client: CloudService) -> None:
    """Запустить облачный сервис"""
    local_files = {file_name: datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(local_folder, file_name)))
                   for file_name in os.listdir(local_folder)}
    cloud_files = client.get_info()

    # Получаем только локальные файлы, которых нет в облачном хранилище
    only_local_files = local_files.keys() - cloud_files.keys()

    # Получаем только облачные файлы, которых нет в локальной папке
    only_cloud_files = cloud_files.keys() - local_files.keys()

    # Получаем только общие файлы облачного хранилища и локальной папки
    common_files = local_files.keys() & cloud_files.keys()

    # Записываем новые локальные файлы в облачное хранилище
    if only_local_files:
        for file_name in only_local_files:
            load = client.load(file_path=os.path.join(local_folder, file_name))
            if load.status_code == 201:
                logger.info(f'Файл {file_name} успешно записан в облачное хранилище')
            else:
                logger.error(f'Файл {file_name} не записан: {load.json().get("message", "error")}')

    # Удаляем файлы из облачного хранилища
    if only_local_files:
        for file_name in only_cloud_files:
            delete = client.delete(filename=file_name)
            if delete.status_code == 204:
                logger.info(f'Файл {file_name} успешно удален из облачного хранилища')
            else:
                logger.error(f'Ошибка удаления файла {file_name} из облачного хранилища: '
                             f'{delete.json().get("message", "error")}')

    # Сравниваем времена общих файлов
    if common_files:
        for file_name in common_files:
            if local_files[file_name].timestamp() > (datetime.datetime.fromisoformat(
                    cloud_files[file_name].replace('Z', '+00:00'))).timestamp():
                reload = client.reload(file_path=os.path.join(local_folder, file_name))
                if reload.status_code == 201:
                    logger.info(f'Файл {file_name} успешно перезаписан в облачном хранилище')
                else:
                    logger.error(f'Файл {file_name} не перезаписан: {reload.json().get("message", "error")}')


def main():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='UTF-8')

    LOCAL_FOLDER_PATH = config['DEFAULT']['LOCAL_FOLDER_PATH']
    LOCAL_FOLDER = config['DEFAULT']['LOCAL_FOLDER_PATH']
    SYNC_INTERVAL = int(config['DEFAULT']['SYNC_INTERVAL'])
    LOG_FILE = config['DEFAULT']['LOG_FILE']
    CLOUD_FOLDER = config['YandexDisk']['CLOUD_FOLDER']
    YANDEX_TOKEN = config['YandexDisk']['YANDEX_TOKEN']
    BASE_URL = config['YandexDisk']['BASE_URL']

    setup_logging(LOG_FILE)
    logger.info(f'Программа синхронизации файлов начинает работу с директорией {LOCAL_FOLDER_PATH}')

    if not os.path.isdir(LOCAL_FOLDER_PATH):
        logger.error(f'Локальная папка {LOCAL_FOLDER} не существует')
        sys.exit(1)

    try:
        logger.info(f'Инициализация сервиса синхронизации файлов')
        client = CloudService(cloud_folder=CLOUD_FOLDER,
                              token=YANDEX_TOKEN,
                              base_url=BASE_URL)
        response = client.check_existence_cloud_folder()
        if response.status_code == 200:
            logger.info(f'Папка {CLOUD_FOLDER} в облачном хранилище существует')
        elif response.status_code == 201:
            logger.info(f'Папка {CLOUD_FOLDER} в облачном хранилище успешно создана')
        else:
            logger.error(f'Ошибка создания папки {CLOUD_FOLDER} в облачном хранилище: '
                         f'{response.json().get("message")}')
    except Exception as exp:
        logger.error(f'Ошибка подключения к сервису синхронизации файлов локальной папки {LOCAL_FOLDER}: {exp}')
        sys.exit(1)

    logger.info(f'Первая синхронизация файлов локальной папки {LOCAL_FOLDER}')
    if not os.path.exists(LOCAL_FOLDER_PATH):
        logger.error(f'Локальная папка {LOCAL_FOLDER} для синхронизации в директории '
                     f'{LOCAL_FOLDER_PATH} отсутствует')
        sys.exit(1)

    try:
        run_cloud_service(LOCAL_FOLDER_PATH, client)
    except Exception as exp:
        logger.error(f'Ошибка первой синхронизации файлов локальной папки {LOCAL_FOLDER}: {exp}')

    logger.info(f'Цикл периодической синхронизации файлов локальной папки {LOCAL_FOLDER} запущен')
    while True:
        try:
            time.sleep(SYNC_INTERVAL)
            run_cloud_service(LOCAL_FOLDER_PATH, client)
        except KeyboardInterrupt:
            logger.error(f'Синхронизация файлов локальной папки {LOCAL_FOLDER} прервана пользователем')
        except Exception as exp:
            logger.error(f'Ошибка синхронизации файлов локальной папки {LOCAL_FOLDER}: {exp}')


if __name__ == '__main__':
    main()
