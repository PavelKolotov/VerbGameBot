# VerbGameBot


Данный проект представляет собой чат [бота телеграм](https://t.me/VerbGameDVMN_bot) и бота [в группе Вконтакте](https://vk.com/public221583857) интегрированных с API [DialogFlow](https://dialogflow.cloud.google.com/). 
С помощью DialogFlow можно обучить ботов и они будут закрывать все типичные вопросы, а вот что-то посложнее – перенаправлять на операторов.

Пример:

![Телеграм бот](https://dvmn.org/filer/canonical/1569214094/323/)

## Как установить

Скачайте или клонируйте репозиторий.

```bash
$ git clone git@github.com:PavelKolotov/VerbGameBot.git
```

Python3 должен быть уже установлен.

Установите виртуальное окружение

```bash
$ python3 -m venv env
```
В папке с проектом 

```bash
$ source env/bin/activate
```

Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:

```bash
$ pip install -r requirements.txt
```

[Включите API](https://cloud.google.com/dialogflow/es/docs/quick/setup#api) DialogFlow на вашем Google-аккаунте

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступные переменные:

- `TG_BOT_API_KEY=6304033371:AAHaUFVA...` - API ключ, который вы получаете при создании бота в Telegram
- `GOOGLE_APPLICATION_CREDENTIALS=/путь/до/credentials.json` -  файл с ключами от вашего Google-аккаунта, credentials.json который вы получили через [Консольную утилиту gcloud](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk)
- `PROJECT_ID=VerbGame...` - ProjectID, который вы получили, когда создавали проект в [DialogFlow](https://dialogflow.cloud.google.com/)
- `SUFFIX=VerbGame...` - название проекта
- `SESSION_ID=9331...` - id пользователя из Telegram
- `LANGUAGE_CODE=RU` - язык на который реагирует [DialogFlow](https://dialogflow.cloud.google.com/), в нашем случае русский
- `VK_API_KEY=vk1.a.cTJXQeleFA2_tWhIfWTa...` - API ключ, который вы получаете при создании группы в ВКонтакте

## Тренировка бота

Тренировку бота можно осуществлять через интерфейс [DialogFlow](https://dialogflow.cloud.google.com/) или загрузить из файла.json с помощью скрипта:

- по умолчанию указан файл questions.json
```bash
$ python create_dialogflow_intent.py
```

- если хотите указать свой путь к файлу
```bash
$ python create_dialogflow_intent.py -j путь/к/файлу.json
```

Для примера в корне проекта лежит файл  `questions.json` в котором содержаться тренировочные фразы и ответы. При создании своих тренировочных фраз соблюдайте структуру .json файла.


## Запуск скрипта

- телеграм бот
```bash
$ python tg_bot.py
```
- бот ВКонтакте
```bash
$ python vk_bot.py
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
