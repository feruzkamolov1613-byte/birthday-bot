import os
import json
from datetime import datetime, timezone, timedelta
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, JobQueue
)

TOKEN = os.environ.get("BOT_TOKEN")
GROUP_ID = int(os.environ.get("GROUP_ID", "0"))
DATA_FILE = "birthdays.json"

# O'zbekiston vaqti UTC+5
UZT = timezone(timedelta(hours=5))


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def today_uzt():
    return datetime.now(UZT).strftime("%d.%m")


async def send_greetings(bot, today):
    data = load_data()
    birthdays_today = [name for name, date in data.items() if date == today]
    if birthdays_today and GROUP_ID != 0:
        for name in birthdays_today:
            await bot.send_message(
                chat_id=GROUP_ID,
                text=(
                    f"🎂 *Hurmatli {name}!*\n\n"
                    f"Safia jamoasi nomidan tug'ilgan kuningiz bilan samimiy tabriklaymiz! 🎉\n"
                    f"Hayotingizning har bir kuni yangi yutuqlar va quvonchlarga to'la bo'lsin! "
                    f"Ishingizda va karyerangizda yangi yutuqlar, har bir qadamingizda muvaffaqiyat, "
                    f"oilangizda doim tinchlik, baxt va sog'lik hukm sursin! "
                    f"Siz uchun eng yaxshi tilaklar! 🥳\n\n"
                    f"*Safia jamoasi* 🎂"
                ),
                parse_mode="Markdown"
            )
    return birthdays_today


# /add Ism KK.OO
async def add(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    args = ctx.args
    if len(args) < 2:
        await update.message.reply_text("❌ Format: /add Ism KK.OO\nMasalan: /add Ali 15.07")
        return
    name = args[0]
    date_str = args[1]
    try:
        datetime.strptime(date_str, "%d.%m")
    except ValueError:
        await update.message.reply_text("❌ Sana noto'g'ri. Format: KK.OO (masalan 15.07)")
        return
    data = load_data()
    data[name] = date_str
    save_data(data)
    await update.message.reply_text(f"✅ {name} — {date_str} saqlandi!")


# /list
async def list_bd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    if not data:
        await update.message.reply_text("📭 Hozircha hech kim yo'q. /add orqali qo'shing.")
        return
    sorted_items = sorted(data.items(), key=lambda x: (int(x[1].split(".")[1]), int(x[1].split(".")[0])))
    text = "🎂 *Tug'ilgan kunlar ro'yxati:*\n\n"
    for name, date in sorted_items:
        text += f"• {name} — {date}\n"
    await update.message.reply_text(text, parse_mode="Markdown")


# /delete Ism
async def delete(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("❌ Format: /delete Ism")
        return
    name = ctx.args[0]
    data = load_data()
    if name in data:
        del data[name]
        save_data(data)
        await update.message.reply_text(f"🗑️ {name} o'chirildi.")
    else:
        await update.message.reply_text(f"❌ {name} topilmadi.")


# /start
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎂 *Tug'ilgan kun bot!*\n\n"
        "Buyruqlar:\n"
        "/add Ism KK.OO — qo'shish\n"
        "/list — ro'yxat\n"
        "/delete Ism — o'chirish\n"
        "/check — bugun tug'ilgan kunlarni tekshirish\n"
        "/sendnow — hozir gruppaga tabrik yuborish",
        parse_mode="Markdown"
    )


# /check
async def check(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    today = today_uzt()
    data = load_data()
    birthdays_today = [name for name, date in data.items() if date == today]
    if birthdays_today:
        names = ", ".join(birthdays_today)
        await update.message.reply_text(f"🎉 Bugun tug'ilgan kun: {names}")
    else:
        await update.message.reply_text(f"😊 Bugun ({today}) hech kimning tug'ilgan kuni yo'q.")


# /sendnow — hozir gruppaga yuborish (test uchun)
async def sendnow(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    today = today_uzt()
    birthdays_today = await send_greetings(ctx.bot, today)
    if birthdays_today:
        names = ", ".join(birthdays_today)
        await update.message.reply_text(f"✅ Tabrik yuborildi: {names}")
    else:
        await update.message.reply_text(f"😊 Bugun ({today}) hech kimning tug'ilgan kuni yo'q.")


# Har kuni soat 09:00 O'zbekiston vaqtida (04:00 UTC)
async def daily_check(ctx: ContextTypes.DEFAULT_TYPE):
    today = today_uzt()
    await send_greetings(ctx.bot, today)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_bd))
    app.add_handler(CommandHandler("delete", delete))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("sendnow", sendnow))

    # Har kuni soat 09:00 O'zbekiston = 04:00 UTC
    job_queue = app.job_queue
    job_queue.run_daily(
        daily_check,
        time=datetime(2000, 1, 1, 4, 0, 0, tzinfo=timezone.utc).timetz()
    )

    print("✅ Bot ishga tushdi!")
    app.run_polling()


if __name__ == "__main__":
    main()
