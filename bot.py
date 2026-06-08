import telebot
import os
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not TELEGRAM_TOKEN or not GROQ_API_KEY:
    print("❌ Помилка: відсутні TELEGRAM_TOKEN або GROQ_API_KEY")
    exit()

bot = telebot.TeleBot(TELEGRAM_TOKEN)

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

SYSTEM_PROMPT = """
Ти — максимально злий, вульгарний і смішний український хуєсос-бот.
Аналізуй текст повідомлення і жорстко, персонально, з матом хуєсось автора.
Коротко (1-2 речення), влучно, з сарказмом і тролінгом. 
Не пояснюй нічого — тільки хуєсос.
"""

@bot.message_handler(func=lambda m: True)
def ai_huyesos(message):
    if not message.text or message.text.startswith('/') or message.from_user.is_bot:
        return

    user_name = message.from_user.first_name or "хуєсос"
    user_text = message.text.strip()

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{user_name} написав: {user_text}\nЗахуєсось його сильно!"}
            ],
            max_tokens=130,
            temperature=0.95,
        )
        insult = response.choices[0].message.content.strip()
        bot.reply_to(message, insult)

    except Exception as e:
        print("Помилка API:", e)
        bot.reply_to(message, f"Йобаний {user_name}, навіть бот не витримує тебе.")

print("🚀 Хуєсос AI бот запущений (Groq)...")
bot.infinity_polling()
