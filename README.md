# homework_bot
python telegram bot

Действия Telegram-бота:
- раз в 10 минут опрашивает API сервиса Практикум.Домашка и проверяет статус отправленной на ревью домашней работы;
- при обновлении статуса анализирует ответ API и отправляет вам соответствующее уведомление в Telegram;
- логирует свою работу и сообщает вам о важных проблемах сообщением в Telegram.

# API сервиса Практикум.Домашка

Эндпоинт API Практикум.Домашка: https://practicum.yandex.ru/api/user_api/homework_statuses/.  
Получить токен можно по адресу: https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a.


# .env

PRACTICUM_TOKEN = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  
TELEGRAM_TOKEN = 0123456789:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     
TELEGRAM_CHAT_ID = 0123456789
