import os
import logging
from openai import OpenAI
from supabase import create_client
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_funnel_questions():
    try:
        result = supabase.table("funnel_questions").select("id,question,agent_task,is_required").eq("is_required", True).order("order_index").execute()
        return result.data if result.data else []
    except Exception as e:
        logger.error(f"Error getting funnel questions: {e}")
        return []

def get_system_prompt(funnel_questions):
    try:
        result = supabase.table("settings").select("key,value").execute()
        data = {row["key"]: row["value"] for row in result.data}
        niche = data.get("niche", "")
        prompt = data.get("system_prompt", "Ты вежливый помощник-консультант.")

        files_result = supabase.table("knowledge_files").select("filename,content").execute()
        knowledge = ""
        if files_result.data:
            for f in files_result.data:
                knowledge += f"\n\n--- {f['filename']} ---\n{f['content']}"

        funnel = ""
        if funnel_questions:
            stages = []
            for q in funnel_questions:
                task = q.get("agent_task") or q.get("question", "")
                name = q.get("question", "")
                stages.append(f"- Этап '{name}': {task}")
            funnel = "\n\nЭтапы воронки — задавай по одному, жди ответа перед следующим:\n" + "\n".join(stages)

        full_prompt = prompt
        if niche:
            full_prompt = f"Ниша: {niche}\n\n{full_prompt}"
        if funnel:
            full_prompt += funnel
        if knowledge:
            full_prompt += f"\n\nФайлы знаний:{knowledge}"

        return full_prompt
    except Exception as e:
        logger.error(f"Error getting system prompt: {e}")
    return "Ты вежливый помощник-консультант."

def get_chat_history(chat_id, exclude_last=1):
    try:
        result = supabase.table("messages").select("role,content").eq("chat_id", chat_id).order("created_at").limit(20).execute()
        data = result.data if result.data else []
        if exclude_last and data:
            data = data[:-exclude_last]
        return data
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

def update_lead_stage(chat_id, username, funnel_questions, all_messages):
    """Определяет текущий этап лида и обновляет в таблице leads"""
    try:
        if not funnel_questions:
            return

        # Считаем сколько этапов пройдено
        # Логика: смотрим на количество сообщений пользователя
        # Каждое сообщение пользователя после первого = прогресс по воронке
        user_messages = [m for m in all_messages if m["role"] == "user"]
        user_msg_count = len(user_messages)

        total_stages = len(funnel_questions)

        if user_msg_count == 0:
            stage = "new_lead"
        elif user_msg_count >= total_stages:
            stage = "deal_won"
        else:
            # Текущий этап — вопрос который сейчас задаётся
            current_question = funnel_questions[min(user_msg_count - 1, total_stages - 1)]
            stage = f"question_{current_question['id']}"

        supabase.table("leads").upsert({
            "chat_id": chat_id,
            "username": username,
            "stage": stage
        }, on_conflict="chat_id").execute()

        logger.info(f"Lead {chat_id} stage updated to: {stage}")
    except Exception as e:
        logger.error(f"Error updating lead stage: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    first_name = update.message.from_user.first_name or ""
    username = update.message.from_user.username or first_name

    try:
        result = supabase.table("settings").select("value").eq("key", "welcome_message").execute()
        welcome = result.data[0]["value"] if result.data else "Добрый день! Чем могу помочь?"
    except Exception as e:
        logger.error(f"Error getting welcome message: {e}")
        welcome = "Добрый день! Чем могу помочь?"

    # Персонализируем приветствие если есть имя
    if first_name:
        welcome = welcome.replace("Добрый день!", f"Добрый день, {first_name}!")

    # Кнопка запроса номера телефона
    keyboard = [[KeyboardButton("📱 Поделиться номером", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    save_message(chat_id, username, "assistant", welcome)
    await update.message.reply_text(welcome, reply_markup=reply_markup)

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    first_name = update.message.from_user.first_name or ""
    username = update.message.from_user.username or first_name
    phone = update.message.contact.phone_number

    # Сохраняем номер в settings для этого пользователя
    try:
        supabase.table("leads").upsert({
            "chat_id": chat_id,
            "username": username,
            "data": phone
        }, on_conflict="chat_id").execute()
    except Exception as e:
        logger.error(f"Error saving phone: {e}")

    reply = f"Отлично, {first_name}! Номер сохранён — наш специалист свяжется с вами по номеру {phone}. Расскажите подробнее о вашей задаче?"
    save_message(chat_id, username, "assistant", reply)
    await update.message.reply_text(reply, reply_markup=ReplyKeyboardRemove())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    username = update.message.from_user.username or update.message.from_user.first_name
    user_message = update.message.text

    logger.info(f"Message from {chat_id} ({username}): {user_message}")
    await update.message.chat.send_action("typing")

    save_message(chat_id, username, "user", user_message)

    funnel_questions = get_funnel_questions()
    system_prompt = get_system_prompt(funnel_questions)
    history = get_chat_history(chat_id, exclude_last=1)
    all_messages_for_stage = get_chat_history(chat_id, exclude_last=0)

    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": user_message}]

    try:
        response = client.chat.completions.create(
            model="anthropic/claude-haiku-4-5",
            messages=messages,
            max_tokens=300
        )
        reply = response.choices[0].message.content.strip()
        if not reply:
            reply = "Уточните, пожалуйста, ваш вопрос."
    except Exception as e:
        logger.error(f"OpenRouter error: {e}")
        reply = "Произошла ошибка, попробуйте позже."

    save_message(chat_id, username, "assistant", reply)

    # Обновляем этап лида после ответа
    update_lead_stage(chat_id, username, funnel_questions, all_messages_for_stage + [{"role": "user", "content": user_message}])

    await update.message.reply_text(reply)

def main():
    logger.info("Starting bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot is running!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
