import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from openai import OpenAI

# ENV'den alıyoruz
BOT_TOKEN = os.getenv("BOT_TOKEN")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Sen samimi, kanka ağzı konuşan bir Telegram botsun.
Kısa, net ve cool cevap ver.
Saçma, alakasız veya çok uzun sorulara cevap verme.
"""

# SADECE bunlar varsa cevap verir
ALLOWED_KEYWORDS = ["selam", "fiyat", "yardım", "bilgi"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Selam kanka 😎 Ne lazım?")

async def cevap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # Filtre: uygun kelime yoksa SUS
    if not any(kelime in text for kelime in ALLOWED_KEYWORDS):
        return

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        max_tokens=100
    )

    await update.message.reply_text(completion.choices[0].message.content)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cevap))
app.run_polling()
