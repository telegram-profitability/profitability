# Profitability Telegram Bot

Этот бот поможет вам отслеживать ваш портфель ценных бумаг:
- Неважно, где вы покупаете и храните активы — вносите всё, чем владеете.
- Прибыльность активов отслеживается относительно момента покупки.
  - При внесении активов поделитесь датой и времем покупки, или вносите стоимость вручную.
- Поддерживается работа с несколькими покупками и/или продажами одного актива.

## Пример использования

1. Вы купили 2 акции YNDX 10 декабря 2023 года за 4674 RUB на платформе Тинькофф Инвестиции.
2. Открываете бота Profitability: вносите две купленные акции с указанием даты и времени покупки.
3. Далее вы купили еще 3 акции YNDX 12 января 2023 года за 3950 RUB на платформе ВТБ Инвестиции.
4. Вновь открываете бота Profitability: вносите три купленные акции с указанием даты и времени покупки.
5. Бот Profitability будет отслеживать ваши суммарные доходы и убытки в рублях. Бот всё посчитает относительно стоимостей активов в момент покупки!

## Скриншоты

![ProfitabilityConcept1](https://github.com/telegram-profitability/profitability/assets/72651791/dd094257-dbbb-4f87-9bda-31be31922e8c)

![ProfitabilityConcept2](https://github.com/telegram-profitability/profitability/assets/72651791/33221520-ba09-459d-b9fd-0dc5cca3acd9)

![ProfitabilityConcept3](https://github.com/telegram-profitability/profitability/assets/72651791/04470676-e26b-494f-a047-b593b01e9d75)

## Запуск проекта

1. Установите зависимости с помощью `pip install -r requirements.txt`.
2. Установите значения в переменные окружения. Названия переменных можно найти в `src/configs.py`.
   - На Windows это можно сделать с помощью `$Env:<key>="<value>"`. 
3. Запустите проект `python -m src.main`.
4. Готово.

## Запуск проекта с помощью Docker'а

1. Соберите проект `docker build -t profitability .`.
2. Скачайте образ PostgreSQL `docker pull postgres`.
3. Запустите контейнер с PostgreSQL `docker run -e POSTGRES_USER="..." -e POSTGRES_PASSWORD="..." -e POSTGRES_DB="..." -p 5432:5432 --name postgres postgres`.
4. Запустите контейнер с проектом `docker run -e CG_API_KEY="..." <more env variables> --name profitability profitability`.
5. Готово.
