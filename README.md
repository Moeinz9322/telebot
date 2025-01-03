# International News Bot

This Telegram bot provides various information, including gold and currency rates, cryptocurrency prices, Hafez divination, prices, and prayer times. The bot is designed in Persian.

## Setup

Follow these steps to set up the bot:

## Install dependencies: 

Make sure you have the telebot and requests libraries installed. You can use the following command to install them:

pip install pyTelegramBotAPI requests

## Configure tokens: 

Create a config.py file in your project directory and paste the following code, replacing the values with your own tokens and API keys:

#https://t.me/BotFather

token = 'paste here'

#https://t.me/navasan_contact_bot

api_token = "paste here"

#https://one-api.ir/

api_key = "paste here"

## When the bot starts,

it sends a welcome message and users can choose from the following options:

1. Gold and Currency Rates: Display gold and currency rates from the Navasan API.

2. Cryptocurrency Prices: Display current prices and 24-hour changes of cryptocurrencies.

3. Hafez Divination: Display Hafez divination from the API.

4. Prices: Display different categories of prices (currencies, gold, coin, oil and gas, metals, commodities).

5. Prayer Times: Display prayer times for different cities.

6. About Us: Display information about the developer.

## Main Functions

### send_welcome(message)

Sends a welcome message and displays the selection buttons.

### check_button(message)

Checks the selected button and calls the corresponding function.

### apiDigitPrice(message)

Requests and displays cryptocurrency information from the API.

### apiGodOptions(message)

Displays city selection buttons for prayer times.

### callback_god(call)

Calls the apiGod function to display prayer times for the selected city.

### apiGod(message, data)

Requests and displays prayer times from the API.

### sendPriceOptions(message)

Displays price category buttons.

### callback_price(call)

Calls the apiPrice function to display prices for the selected category.

### apiPrice(message, section)

Requests and displays prices from the API.

### apiFall(message)

Requests and displays Hafez divination from the API.

apiCurrency(message)
Requests and displays gold and currency rates from the Navasan API.

# Contact Us

Developer: Moein Zanjirian Zadeh

Email: moeinz9322@gmail.com
