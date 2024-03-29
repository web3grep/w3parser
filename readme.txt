
Проект w3parcer представляет собой инструмент для отслеживания и пересылки сообщений из различных каналов Telegram в ваш собственный канал на основе ключевых слов.

### Настройка

1. **Получение API ID и API HASH**:
   - Перейдите на сайт [my.telegram.org](https://my.telegram.org/) и войдите в свой аккаунт.
   - Перейдите в раздел "API development tools" и создайте новое приложение.
   - Запишите свой `API_ID` и `API_HASH`.

2. **Создание бота**:
   - Напишите [@BotFather](https://t.me/botfather) в Telegram.
   - Создайте нового бота и получите токен для вашего бота.

3. **Настройка файла `settings.py`**:
   - Укажите ваш `BOT_TOKEN` от BotFather.
   - Укажите `API_ID` и `API_HASH`, полученные на предыдущем шаге.
   - Укажите `YOUR_USER_ID` - ваш ID пользователя в Telegram. Вы можете узнать его, написав [@userinfobot](https://t.me/userinfobot) в Telegram.
   - Укажите `MY_CHANNEL_ID` - ID вашего канала, где бот является администратором. Убедитесь, что бот добавлен в канал в качестве администратора.

### Использование

1. Запустите `bot.py`. Этот скрипт будет слушать команды, отправленные вашему боту, и позволит вам добавлять каналы для отслеживания, устанавливать ключевые слова и т. д.

2. Запустите `user.py`. Этот скрипт будет отслеживать сообщения из добавленных каналов и пересылать их в ваш канал (указанный в `MY_CHANNEL_ID`), если они содержат ключевые слова.

3. Взаимодействуйте с вашим ботом в Telegram, отправляя ему команды для добавления каналов, ключевых слов и т. д.

### Примечания

- Убедитесь, что user является администратором в вашем канале и имеет права на отправку сообщений.
- Если вы столкнетесь с ошибками или проблемами, убедитесь, что все переменные в `settings.py` корректно установлены.

---

Использование бота
После успешной настройки и запуска bot.py вы можете взаимодействовать с вашим ботом в Telegram. Вот некоторые основные команды и их функции:

Добавление канала для отслеживания:

/add_chan [ID/@username/ссылка]: Добавляет канал для отслеживания. Вы можете указать ID канала, его @username или прямую ссылку на канал.
Удаление канала из списка отслеживания:

/rm_chan [ID/@username/ссылка]: Удаляет канал из списка отслеживания.
Просмотр списка отслеживаемых каналов:

/view_channels: Показывает список всех каналов, которые вы отслеживаете.
Добавление ключевых слов:

/add_keywords [слово1 слово2 ...]: Добавляет ключевые слова, по которым будет производиться фильтрация сообщений.
Удаление ключевых слов:

/rm_kwd [слово]: Удаляет указанное ключевое слово из списка.
Просмотр списка ключевых слов:

/view_keywords: Показывает список всех ключевых слов, по которым производится фильтрация.
Изменение статуса отслеживания канала:

/change_status [имя канала] [off/kwd/all]: Изменяет статус отслеживания для указанного канала. Статусы:
off: не отслеживать канал.
kwd: отслеживать только сообщения, содержащие ключевые слова.
all: отслеживать все сообщения из канала.
Вступление в канал:

/join [@username/ссылка]: Команда для вступления бота в канал по @username или прямой ссылке.