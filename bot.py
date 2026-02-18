import os
import logging
from groq import Groq
from supabase import create_client
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

groq_client = Groq(api_key=GROQ_API_KEY)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_system_prompt():
    try:
        result = supabase.table("settings").select("value").eq("key", "system_prompt").execute()
        if result.data:
            return result.data[0]["value"]
    except Exception as e:
        logger.error(f"Error getting system prompt: {e}")
    return "Ты вежливый помощник-консультант."

def get_chat_history(chat_id):
    try:
        result = supabase.table("messages").select("role,content").eq("chat_id", chat_id).order("created_at").limit(20).execute()
        return result.data if result.data else []
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        return []

def save_message(chat_id, username, role, content):
    try:
        supabase.table("messages").insert({
            "chat_id": chat_id,
            "username": username,
            "role": role,
            "content": content
        }).execute()
    except Exception as e:
        logger.error(f"Error saving message: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    username = update.message.from_user.username or update.message.from_user.first_name
    user_message = update.message.text

    logger.info(f"Message from {chat_id} ({username}): {user_message}")
    await update.message.chat.send_action("typing")

    save_message(chat_id, username, "user", user_message)

    system_prompt = get_system_prompt()
    history = get_chat_history(chat_id)

    messages = [{"role": "system", "content": system_prompt}] + history

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1000
        )
        reply = response.choices[0].message.content
    except Exception as e:
        logger.error(f"Groq error: {e}")
        reply = "Произошла ошибка, попробуйте позже."

    save_message(chat_id, username, "assistant", reply)
    await update.message.reply_text(reply)

def main():
    logger.info("Starting bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot is running!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
