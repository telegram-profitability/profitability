START_TEXT = """
Привет! 👋 Я помогу тебе отслеживать твой портфель ценных бумаг и криптовалют.

Доступные команды:
➕ /add — добавить покупку или продажу ценной бумаги или криптовалюты.
📊 /stats — твой портфель.
❔ /help — список доступных команд.
"""
HELP_TEXT = """
Доступные команды:
➕ /add — добавить покупку или продажу ценной бумаги или криптовалюты.
📊 /stats — твой портфель.

Нашел ошибку или есть предложение? Напиши нам! 
@kfcgenius @theoilside @drapkinamaria
"""
ADD_CRYPTO_TEXT = """
Чтобы добавить покупку или продажу криптовалюты\, введи команду\: `/coin \{Криптовалюта\} \{Количество\} \{Дата\}`

→ *Криптовалюта* — ID криптовалюты на CoinGecko \(например\, _bitcoin_ или _binancecoin_\)\.
→ *Количество* — количество криптовалюты \(например\, _2_ или _3\.2_\)\. При продаже укажи отрицательное число\.
→ *Дата* — дата покупки или продажи в формате DD\-MM\-YYYY \(например\, _12\-11\-2021_\)\. Можно не указывать при покупке\: тогда возьмем сегодняшнюю дату\.

Пример команды\: `/coin bitcoin 2 30\-11\-2021`
"""
ADD_STOCK_TEXT = """
Чтобы добавить покупку или продажу ценной бумаги\, введи команду\: `/stock \{Тикер\} \{Количество\} \{Дата\}`

→ *Название* — тикер на Тинькофф Инвестициях \(например\, _aapl_ или _vtbr_\)\.
→ *Количество* — количество ценных бумаг\. При продаже укажи отрицательное число\.
→ *Дата* — дата покупки или продажи в формате DD\-MM\-YYYY \(например, _12\-11\-2021_\)\. Можно не указывать при покупке\: тогда возьмем сегодняшнюю дату\.

Пример команды\: `/stock aapl 2 20\-03\-2022`
"""
OPERATION_COMPLETED_TEXT = """
🟢 Операция сохранена. 
→ Твой портфель: /stats
→ Добавить еще одну покупку или продажу: /add 
"""
ADD_OPERATIONS = """
🟠 Ты пока не добавил ни одного актива в свой портфель. 
→ Добавить покупку или продажу: /add 
"""
ERROR_TEXT = """
🔴 Ошибка! Такой команды нет.
→ Список доступных команд: /help
"""
USER_FETCH_ERROR_TEXT = """
🔴 Ошибка! 
Что-то пошло не так при получении данных о пользователе.
→ Помощь: /help
"""
OPERATION_ERROR_TEXT = """
🔴 Ошибка! 
Что-то пошло не так при получении данных об операции.
→ Помощь: /help
"""
