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

## Docker

1. `docker build -t profitability .`
2. `docker run -e CG_API_KEY="..." <more env variables> --name profitability profitability`
3. `docker pull postgres`
4. `docker run -e POSTGRES_USER="..." -e POSTGRES_PASSWORD="..." -e POSTGRES_DB="..." -p 5432:5432 --name postgres postgres`
