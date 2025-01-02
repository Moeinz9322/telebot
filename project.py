import telebot
from config import token, api_key, api_token
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
import requests

bot = telebot.TeleBot(token)

userId = []

reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
button1 = KeyboardButton(text="نرخ طلا و ارز")
button2 = KeyboardButton(text="ارز دیجیتال")
button3 = KeyboardButton(text="فال حافظ")
button4 = KeyboardButton(text="قیمت ها")
button5 = KeyboardButton(text="اوقات شرعی")
button6 = KeyboardButton(text="درباره ما")
reply_keyboard.add(button1, button2, button3, button4, button5, button6)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    welcome_message = "سلام و درود\n\n🌹به ربات خبری اینترنشنال خوش آمدید🌹\n\nما تعهد میدهیم آخرین اخبار روز دنیا با سرعت بالا و بدون سانسور در اختیار شما قرار خواهد گرفت\n\n لطفا حوزه های خبری که به آن علاقه مند هستید را انتخاب کنید تا به بهبود ارائه خدمات منجر شود"
    bot.send_message(message.chat.id, welcome_message, reply_markup=reply_keyboard)

    if message.chat.id not in userId:
        userId.append(message.chat.id)


@bot.message_handler(func=lambda message: True)
def check_button(message):
    if message.text == "نرخ طلا و ارز":
        apiCurrency(message)
    elif message.text == "ارز دیجیتال":
        apiDigitPrice(message)
    elif message.text == "فال حافظ":
        apiFall(message)
    elif message.text == "قیمت ها":
        sendPriceOptions(message)
    elif message.text == "اوقات شرعی":
        apiGodOptions(message)
    else:
        bot.send_message(
            message.chat.id,
            f"درباره ما:\n برنامه نویس: معین زنجیریان زاده\n ایمیل: moeinz9322@gmail.com",
        )


def apiDigitPrice(message):
    en_num = "true"
    url = f"https://one-api.ir/DigitalCurrency/?token={api_token}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("result", [])
        if data:
            message_text = ""
            for item in data[:10]:
                message_text += f"نام: {item['name']} ({item['name_en']})\n"
                message_text += f"قیمت فعلی: {item['price']} دلار\n"
                message_text += (
                    f"تغییر قیمت در ۲۴ ساعت گذشته: {item['price_change_24h']} دلار\n"
                )
                message_text += (
                    f"تغییر درصد در ۲۴ ساعت گذشته: {item['percent_change_24h']}%\n\n"
                )
            if message_text.strip():
                bot.send_message(message.chat.id, message_text)
            else:
                bot.send_message(message.chat.id, "داده‌ای موجود نیست.")
        else:
            bot.send_message(message.chat.id, "داده‌ای موجود نیست.")
    else:
        bot.send_message(message.chat.id, "خطایی در دریافت اطلاعات رخ داده است.")


def apiGodOptions(message):
    markup = InlineKeyboardMarkup()
    sections = [
        "یزد",
        "تهران",
        "مشهد",
        "شیراز",
        "اصفهان",
        "کرمان",
        "ساری",
    ]

    for section in sections:
        markup.add(InlineKeyboardButton(text=section, callback_data=section))

    bot.send_message(
        message.chat.id, "لطفاً یک شهر را انتخاب کنید:", reply_markup=markup
    )


@bot.callback_query_handler(
    func=lambda call: call.data
    in ["یزد", "تهران", "مشهد", "شیراز", "اصفهان", "کرمان", "ساری"]
)
def callback_god(call):
    apiGod(call.message, call.data)


def apiGod(message, data):
    city = data
    en_num = "true"
    url = f"https://one-api.ir/owghat/?token={api_token}&city={city}&en_num={en_num}"
    response = requests.get(url)
    title = {
        "city": "شهر",
        "azan_sobh": "اذان صبح",
        "toloe_aftab": "طلوع آفتاب",
        "azan_zohre": "اذان ظهر",
        "ghorob_aftab": "غروب آفتاب",
        "azan_maghreb": "اذان مغرب",
        "nime_shabe_sharie": "نیمه شب شرعی",
        "month": "ماه",
        "day": "روز",
        "longitude": "طول جغرافیایی",
        "latitude": "عرض جغرافیایی",
    }
    if response.status_code == 200:
        data = response.json().get("result", {})
        message1 = ""
        for item in data:
            message1 += title[item] + ": " + data[item] + "\n"
        bot.send_message(message.chat.id, message1)


def sendPriceOptions(message):
    markup = InlineKeyboardMarkup()
    sections = [
        "currencies",
        "gold",
        "coin",
        "coin_retail",
        "oil",
        "metals",
        "commodity",
    ]
    section_titles = {
        "currencies": "ارزها 💵",
        "gold": "طلا 🏆",
        "coin": "سکه 💍",
        "coin_retail": "سکه خرده‌فروشی 💍",
        "oil": "نفت و گاز ⛽",
        "metals": "فلزات 🔧",
        "commodity": "کالاها 🌾",
    }

    for section in sections:
        markup.add(
            InlineKeyboardButton(text=section_titles[section], callback_data=section)
        )

    bot.send_message(
        message.chat.id, "لطفاً یک دسته‌بندی را انتخاب کنید:", reply_markup=markup
    )


@bot.callback_query_handler(
    func=lambda call: call.data
    in ["currencies", "gold", "coin", "coin_retail", "oil", "metals", "commodity"]
)
def callback_price(call):
    apiPrice(call.message, call.data)


def apiPrice(message, section):
    url = f"https://one-api.ir/price/?token={api_token}&action=tgju"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json().get("result", {})
        section_titles = {
            "currencies": "ارزها 💵",
            "gold": "طلا 🏆",
            "coin": "سکه 💍",
            "coin_retail": "سکه خرده‌فروشی 💍",
            "oil": "نفت و گاز ⛽",
            "metals": "فلزات 🔧",
            "commodity": "کالاها 🌾",
        }

        if section in data:
            message_text = f"**💰 قیمت‌ها - {section_titles[section]} 💰**\n"
            items = data[section]
            for key, value in items.items():
                message_text += f"{key}:\n قیمت: {value['p']}\n بیشترین: {value.get('h', 'N/A')}\n کمترین: {value.get('l', 'N/A')}\n تغییر: {value.get('d', 'N/A')}\n"

            bot.send_message(message.chat.id, message_text, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "خطایی رخ داده است. لطفا با ما تماس بگیرید.")
        print("!!!!!!!!!!!بدبخت شدیم!!!!!!!!!!!")


def apiFall(message):
    url = f"https://one-api.ir/hafez/?token={api_token}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("result", {})
        title = data.get("TITLE", "بدون عنوان")
        rhyme = data.get("RHYME", "بدون متن")
        meaning = data.get("MEANING", "بدون معنی")
        fall_message = f"""
📜 **فال حافظ**
            
**عنوان:** {title}

**متن:**
{rhyme}

**معنی:**
{meaning}
            
        """
        bot.send_message(message.chat.id, fall_message, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "خطایی رخ داده است. لطفا با ما تماس بگیرید.")
        print("!!!!!!!!!!!بدبخت شدیم!!!!!!!!!!!")


def apiCurrency(message):
    url = f"http://api.navasan.tech/latest/?api_key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        relevant_data = []

        coins_of_interest = [
            "18ayar",
            "abshodeh",
            "sekkeh",
            "bahar",
            "nim",
            "gerami",
            "usd_sell",
            "usd_buy",
            "eur",
        ]
        title = {
            "18Ayar": "18 عیار",
            "Abshodeh": "آبشده",
            "Sekkeh": "سکه امامی",
            "Bahar": "سکه بهار آزادی",
            "Nim": "نیم سکه",
            "Gerami": "گرمی",
            "Usd Sell": "دلار قیمت فروش",
            "Usd Buy": "دلار قیمت خرید",
            "Eur": "یورو",
        }

        for key in coins_of_interest:
            if key in data:
                value = data[key]
                relevant_data.append(
                    {
                        "Item": key.replace("_", " ").title(),
                        "Value (IRR)": f"{int(value['value']):,}",
                        "Change": value.get("change", "N/A"),
                        "Date": value.get("date", "N/A"),
                    }
                )

        if not relevant_data:
            bot.send_message(message.chat.id, "No relevant data found.")
        else:
            date = relevant_data[0]["Date"]
            message_text = f"📊 نرخ طلا و ارز:\n\n📅 تاریخ: {date}\n\n"
            message_text += f"{'Item':<30} | {'Value (IRR)':<15} | {'Change'}\n"
            message_text += "-" * 70 + "\n"

            for item in relevant_data:
                change_symbol = "🟢" if item["Change"] >= 0 else "🔴"
                message_text += f"{title[item['Item']]} :\n{item['Value (IRR)']} \n{change_symbol} {item['Change']}\n\n"

            bot.send_message(message.chat.id, message_text)
    else:
        bot.send_message(message.chat.id, "خطایی رخ داده است. لطفا با ما تماس بگیرید.")
        print("!!!!!!!!!!!بدبخت شدیم!!!!!!!!!!!")


bot.infinity_polling()
