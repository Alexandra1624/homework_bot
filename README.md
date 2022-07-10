# Бот-ассистент
## _Описание_

Действия **Telegram-бота**:
- раз в 10 минут опрашивает ***API*** сервиса ***Практикум.Домашка*** и проверяет статус отправленной на ревью домашней работы;
- при обновлении статуса анализирует ответ ***API*** и отправляет вам соответствующее уведомление в ***Telegram***;
- логирует свою работу и сообщает вам о важных проблемах сообщением в ***Telegram***.

### API сервиса Практикум.Домашка

Эндпоинт ***API*** Практикум.Домашка: https://practicum.yandex.ru/api/user_api/homework_statuses/.    
Получить ***токен*** можно по адресу: https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a.

### Статус домашней работы (значение по ключу status ) может быть трёх типов:
- **reviewing**: работа взята в ревью;
- **approved**: ревью успешно пройдено;
- **rejected**: в работе есть ошибки, нужно поправить

## Технологии
- Python 3.7.9
- Django 2.2.16
- Django Rest Framework 3.12.4
- Pytest 6.2.4

## Установка
1. **Клонируйте репозиторий:**
```sh
git clone https://github.com/Alexandra1624/hw04_tests.git
```

2. **Cоздать и активировать виртуальное окружение:**
```sh
python -m venv venv
source venv/Scripts/activate
```

3. **Обновить pip и установить зависимости из файла requirements.txt:**
```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
``` 

4. **Добавьте файл ".env"**
```sh
PRACTICUM_TOKEN = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX          
TELEGRAM_TOKEN = 0123456789:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX         
TELEGRAM_CHAT_ID = 0123456789
```

## Автор

**_Александра Радионова_**  
https://github.com/Alexandra1624  
https://t.me/alexandra_R1624  
sashamain@yandex.ru
