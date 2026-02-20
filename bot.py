import os
import re
import json
import logging
from openai import OpenAI
from supabase import create_client
from telegram import Update
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

        full_prompt += "\n\nВАЖНО: Никогда не используй markdown форматирование — никаких **, *, #, `, _ и других символов разметки. Пиши обычным текстом."

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


def extract_and_save_data(chat_id, username, funnel_questions, all_messages):
    """Извлекает данные из диалога, сохраняет в collected_data и обновляет этап"""
    try:
        if not funnel_questions or not all_messages:
            return

        fields = "\n".join([f"- {q['question']}" for q in funnel_questions])
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in all_messages[-20:]])

        extraction_prompt = f"""Из диалога ниже извлеки следующие данные если они были упомянуты:
{fields}

Диалог:
{history_text}

Ответь ТОЛЬКО в формате JSON где ключи это названия полей а значения это найденные данные.
Если данные не найдены — не включай поле в ответ.
Пример: {{"Имя": "Михаил", "Телефон": "89219503860"}}"""

        response = client.chat.completions.create(
            model="anthropic/claude-haiku-4-5",
            messages=[{"role": "user", "content": extraction_prompt}],
            max_tokens=300
        )

        raw = response.choices[0].message.content.strip()
        raw = re.sub(r'```json|```', '', raw).strip()
        extracted = json.loads(raw)

        # Получаем текущие данные лида
        existing = supabase.table("leads").select("id,collected_data").eq("chat_id", chat_id).execute()
        current_data = {}
        if existing.data:
            current_data = existing.data[0].get("collected_data") or {}
        current_data.update(extracted)

        # Определяем этап по заполненным полям
        filled = sum(1 for q in funnel_questions if current_data.get(q['question']))
        total = len(funnel_questions)

        if filled == 0:
            stage = "new_lead"
        elif filled >= total:
            stage = "deal_won"
        else:
            stage = "new_lead"
            for q in funnel_questions:
                if not current_data.get(q['question']):
                    stage = f"question_{q['id']}"
                    break

        # Сохраняем данные и этап
        if existing.data:
            supabase.table("leads").update({
                "collected_data": current_data,
                "stage": stage,
                "username": username
            }).eq("chat_id", chat_id).execute()
        else:
            supabase.table("leads").insert({
                "chat_id": chat_id,
                "username": username,
                "collected_data": current_data,
                "stage": stage
            }).execute()

        logger.info(f"Lead {chat_id}: stage={stage}, filled={filled}/{total}, data={extracted}")

    except Exception as e:
        logger.error(f"Error extracting data: {e}")


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

    if first_name:
        welcome = welcome.replace("Добрый день!", f"Добрый день, {first_name}!")

    save_message(chat_id, username, "assistant", welcome)
    await update.message.reply_text(welcome)


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
    all_messages = get_chat_history(chat_id, exclude_last=0)

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

    # Извлекаем данные и обновляем этап
    all_msgs = all_messages + [{"role": "user", "content": user_message}]
    extract_and_save_data(chat_id, username, funnel_questions, all_msgs)

    await update.message.reply_text(reply)


def main():
    logger.info("Starting bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot is running!")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
