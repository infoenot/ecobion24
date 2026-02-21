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
    base_url="https://api.polza.ai/v1"
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
        collect_name = data.get("collect_name", "true") != "false"
        collect_phone = data.get("collect_phone", "true") != "false"

        files_result = supabase.table("knowledge_files").select("filename,content").execute()
        knowledge = ""
        if files_result.data:
            for f in files_result.data:
                knowledge += f"\n\n--- {f['filename']} ---\n{f['content']}"

        # Этапы воронки
        funnel = ""
        if funnel_questions:
            stages = []
            for q in funnel_questions:
                task = q.get("agent_task") or q.get("question", "")
                name = q.get("question", "")
                stages.append(f"- Этап '{name}': {task}")
            funnel = "\n\nЭТАПЫ ВОРОНКИ (задавай строго по одному, жди ответа):\n" + "\n".join(stages)

        # Контакты — всегда в самом конце воронки
        contact_steps = []
        if collect_name:
            contact_steps.append("- Узнай имя клиента (как к нему обращаться)")
        if collect_phone:
            contact_steps.append("- Узнай номер телефона для связи со специалистом")
        if contact_steps:
            funnel += "\n\nПОСЛЕ того как все этапы воронки пройдены — узнай контакты:\n" + "\n".join(contact_steps)

        # Собираем промпт: ниша → файлы знаний → системный промпт → воронка → жёсткие правила формата последними
        full_prompt = ""
        if niche:
            full_prompt += f"Ниша: {niche}\n\n"
        if knowledge:
            full_prompt += f"Файлы знаний:{knowledge}\n\n"
        full_prompt += prompt
        if funnel:
            full_prompt += funnel

        # Правила формата — последними, чтобы модель их не забывала
        full_prompt += "\n\n---\nФОРМАТ ОТВЕТА (обязательно):\n- Максимум 2-3 предложения. Это жёсткое ограничение.\n- Только обычный текст — никаких **, *, #, ` и других символов разметки.\n- Каждый ответ заканчивается одним вопросом или конкретным шагом."

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


def get_contact_settings():
    """Читает настройки сбора контактов"""
    try:
        result = supabase.table("settings").select("key,value").in_("key", ["collect_name", "collect_phone"]).execute()
        data = {row["key"]: row["value"] for row in (result.data or [])}
        collect_name = data.get("collect_name", "true") != "false"
        collect_phone = data.get("collect_phone", "true") != "false"
        return collect_name, collect_phone
    except Exception as e:
        logger.error(f"Error getting contact settings: {e}")
        return True, True


def extract_and_save_data(chat_id, username, funnel_questions, all_messages):
    """Извлекает данные из диалога, сохраняет в collected_data и обновляет этап"""
    try:
        if not all_messages:
            return

        collect_name, collect_phone = get_contact_settings()
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in all_messages[-20:]])

        # --- Извлекаем имя и телефон отдельно ---
        contact_update = {}
        if collect_name or collect_phone:
            contact_fields = []
            if collect_name:
                contact_fields.append("- Имя клиента (как представился)")
            if collect_phone:
                contact_fields.append("- Номер телефона (в любом формате)")

            contact_prompt = f"""Из диалога ниже извлеки только эти данные если они были упомянуты:
{chr(10).join(contact_fields)}

Диалог:
{history_text}

Ответь ТОЛЬКО JSON. Используй ключи: "name" и/или "phone".
Если не найдено — не включай ключ.
Пример: {{"name": "Михаил", "phone": "89219503860"}}"""

            resp = client.chat.completions.create(
                model="anthropic/claude-3-haiku",
                messages=[{"role": "user", "content": contact_prompt}],
                max_tokens=100
            )
            raw = re.sub(r'```json|```', '', resp.choices[0].message.content.strip()).strip()
            try:
                contacts = json.loads(raw)
                if collect_name and contacts.get("name"):
                    contact_update["username"] = contacts["name"]
                if collect_phone and contacts.get("phone"):
                    contact_update["phone"] = contacts["phone"]
            except Exception:
                pass

        # --- Извлекаем данные воронки ---
        extracted = {}
        if funnel_questions:
            fields = "\n".join([f"- {q['question']}" for q in funnel_questions])
            extraction_prompt = f"""Из диалога ниже извлеки следующие данные если они были упомянуты:
{fields}

Диалог:
{history_text}

Ответь ТОЛЬКО в формате JSON где ключи это названия полей а значения это найденные данные.
Если данные не найдены — не включай поле в ответ.
Пример: {{"Тип объекта": "дача"}}"""

            response = client.chat.completions.create(
                model="anthropic/claude-3-haiku",
                messages=[{"role": "user", "content": extraction_prompt}],
                max_tokens=300
            )
            raw = re.sub(r'```json|```', '', response.choices[0].message.content.strip()).strip()
            try:
                extracted = json.loads(raw)
            except Exception:
                pass

        # Получаем текущие данные лида
        existing = supabase.table("leads").select("id,collected_data").eq("chat_id", chat_id).execute()
        current_data = {}
        if existing.data:
            current_data = existing.data[0].get("collected_data") or {}
        current_data.update(extracted)

        # Определяем этап по заполненным полям воронки
        if funnel_questions:
            filled = sum(1 for q in funnel_questions if current_data.get(q['question']))
            total = len(funnel_questions)
            if filled >= total:
                stage = "deal_won"
            else:
                stage = "new_lead"
                for q in funnel_questions:
                    if not current_data.get(q['question']):
                        stage = f"question_{q['id']}"
                        break
        else:
            stage = "new_lead"

        # Формируем данные для сохранения
        lead_data = {
            "collected_data": current_data,
            "stage": stage,
            "username": contact_update.get("username", username),
        }
        if "phone" in contact_update:
            lead_data["phone"] = contact_update["phone"]

        if existing.data:
            supabase.table("leads").update(lead_data).eq("chat_id", chat_id).execute()
        else:
            lead_data["chat_id"] = chat_id
            supabase.table("leads").insert(lead_data).execute()

        logger.info(f"Lead {chat_id}: stage={stage}, contacts={contact_update}, funnel={extracted}")

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
            model="anthropic/claude-3-haiku",
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
