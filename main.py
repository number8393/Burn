import time
import yfinance as yf
import telebot
import datetime

# Токен Telegram-бота
TOKEN = '8094752756:AAFUdZn4XFlHiZOtV-TXzMOhYFlXKCFVoEs'
bot = telebot.TeleBot(TOKEN)

# Твой Telegram ID
CHAT_ID = '5556108366'

# Валютные пары
symbols = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "USD/CHF": "CHF=X",
    "AUD/USD": "AUDUSD=X",
    "NZD/USD": "NZDUSD=X",
    "USD/CAD": "CAD=X"
}

def analyze(name, symbol):
    try:
        data = yf.download(tickers=symbol, interval="1m", period="5m")
        if data.empty or len(data) < 2:
            return f"Doshik:\n❌ Ошибка {name}: Нет данных", None

        last = data.iloc[-1]
        close_price = float(last['Close'])
        open_price = float(last['Open'])

        if close_price > open_price:
            signal = "📈 Покупка"
            confidence = round((close_price - open_price) / open_price * 100, 2)
        elif close_price < open_price:
            signal = "📉 Продажа"
            confidence = round((open_price - close_price) / open_price * 100, 2)
        else:
            signal = "⏸ Нет сигнала"
            confidence = 0

        if confidence >= 0.1:
            return f"🔔 {name}\nСигнал: {signal}\nУверенность: {confidence}%", None
        else:
            return f"🔕 {name}: Нет сильного сигнала", None

    except Exception as e:
        return f"Doshik:\n❌ Ошибка {name}: {str(e)}", None

def run_bot():
    while True:
        now = datetime.datetime.now()
        if 6 <= now.hour < 22:
            for name, symbol in symbols.items():
                message, _ = analyze(name, symbol)
                bot.send_message(CHAT_ID, message)
        else:
            bot.send_message(CHAT_ID, "⏰ Вне времени торговли (06:00 - 22:00 по Астане).")
        time.sleep(30)

if __name__ == "__main__":
    run_bot()
