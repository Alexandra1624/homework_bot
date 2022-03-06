import json
import logging
import telegram
import os
import sys
import time

import requests
from dotenv import load_dotenv
from telegram import error
from http import HTTPStatus

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    format='%(asctime)s [%(levelname)s] %(message)s'
)

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


class PracticumException(Exception):
    """Исключения бота."""

    pass


def send_message(bot, message: str):
    """Отправка сообщения в телеграм."""
    log = message.replace('\n', '')
    logging.info(f'Отправка сообщения в телеграм: {log}')
    try:
        return bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except error.Unauthorized:
        timeout_and_logging(
            'Телеграм API: Не авторизован, проверьте TELEGRAM_TOKEN и '
            'TELEGRAM_CHAT_ID '
        )
    except error.BadRequest as e:
        timeout_and_logging(f'Ошибка работы с Телеграм: {e}')
    except error.TelegramError as e:
        timeout_and_logging(f'Ошибка работы с Телеграм: {e}')


def get_api_answer(current_timestamp: int) -> list:
    """Получение списка домашних работы от заданного времени."""
    logging.info('Получение ответа от сервера')
    try:
        homework_statuses = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params={'from_date': current_timestamp}
        )
    except requests.exceptions.RequestException as e:
        raise PracticumException(
            'При обработке вашего запроса возникла неоднозначная '
            f'исключительная ситуация: {e}'
        )
    except ValueError as e:
        raise PracticumException(f'Ошибка в значении {e}')
    except TypeError as e:
        raise PracticumException(f'Не корректный тип данных {e}')

    if homework_statuses.status_code != HTTPStatus.OK:
        logging.debug(homework_statuses.json())
        raise PracticumException(
            f'Ошибка {homework_statuses.status_code} practicum.yandex.ru')

    try:
        homework_statuses_json = homework_statuses.json()
    except json.JSONDecodeError:
        raise PracticumException(
            'Ответ от сервера должен быть в формате JSON'
        )
    logging.info('Получен ответ от сервера')
    return homework_statuses_json


def check_response(response: list) -> list:
    """Проверяет ответ API на корректность."""
    logging.debug('Проверка ответа API на корректность')
    if 'error' in response:
        if 'error' in response['error']:
            raise PracticumException(
                f"{response['error']['error']}"
            )

    if 'code' in response:
        raise PracticumException(
            f"{response['message']}"
        )

    if response['homeworks'] is None:
        raise PracticumException('Задания не обнаружены')

    if not isinstance(response['homeworks'], list):
        raise PracticumException(
            f"{response['homeworks']} не является списком"
        )
    return response['homeworks']


def parse_status(homework: dict) -> str:
    """Извлекает из информации о конкретной домашней работе статус."""
    logging.debug(f'Проверяем домашнее задание: {homework}')
    homework_name = homework['homework_name']
    homework_status = homework['status']

    if homework_status not in HOMEWORK_STATUSES:
        raise PracticumException(
            'Обнаружен новый статус, которого нет в списке!'
        )

    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """
    Проверка доступности переменных окружения.
    Проверяет доступность переменных окружения,
    которые необходимы для работы программы.
    Если отсутствует хотя бы одна переменная окружения —
    функция должна вернуть False, иначе — True.
    """
    token_tuple = (PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
    for token in token_tuple:
        if not token:
            return False
        return True


def timeout_and_logging(message: str = None, level_error=logging.error):
    """Запись в лог."""
    if message:
        level_error(message)


def main():
    """Описана основная логика работы программы."""
    if not check_tokens():
        logging.critical('Отсутствует хотя бы одна переменная окружения.')
        return 0
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = 0  # начальное значение timestamp или 0
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            logging.info("Список домашних работ получен")
            if ((type(homeworks) is list)
                    and (len(homeworks) > 0)
                    and homeworks):
                send_message(bot, parse_status(homeworks[0]))
            else:
                logging.info('Задания не обнаружены')
            current_timestamp = response['current_date']
            time.sleep(RETRY_TIME)

        except PracticumException as e:
            timeout_and_logging(f'practicum.yandex.ru: {e}')
        except Exception as e:
            timeout_and_logging(
                f'Сбой в работе программы: {e}',
                logging.critical
            )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Выход из программы')
        sys.exit(0)
