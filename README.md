# homework_bot
python telegram bot

Действия Telegram-бота:
- раз в 10 минут опрашивает API сервис Практикум.Домашка и проверяет статус отправленной на ревью домашней работы;
- при обновлении статуса анализирует ответ API и отправляет вам соответствующее уведомление в Telegram;
- логирует свою работу и сообщает вам о важных проблемах сообщением в Telegram.


# .env

PRACTICUM_TOKEN = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

TELEGRAM_TOKEN = 0123456789:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

TELEGRAM_CHAT_ID = 0123456789
