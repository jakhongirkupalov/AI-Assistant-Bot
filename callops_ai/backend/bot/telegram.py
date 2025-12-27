import os
import sys
import django
import asyncio
from aiogram import Bot, Dispatcher, types
from asgiref.sync import sync_to_async

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from django.conf import settings
from tickets.models import Ticket
from ai_engine.ai_reply import ai_answer

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text
    user_id = str(message.from_user.id)

    ticket = await sync_to_async(Ticket.objects.create)(
        user_id=user_id,
        message=user_text,
        status="new"
    )

    ai_result = ai_answer(user_text)

    await sync_to_async(Ticket.objects.filter(id=ticket.id).update)(
        ai_answer=ai_result,
        status="ai_answered"
    )

    if ai_result == "NOT_IN_SCOPE":
        await message.answer(
            "ℹ️ Men faqat CallOps xizmatlari bo‘yicha savollarga javob beraman.\n"
            "Iltimos, tariflar yoki buyurtma haqida so‘rang."
        )
        return

    if ai_result == "OPERATOR_NEEDED":
        await message.answer("📨 Savolingiz operatorga yuborildi.")
        return

    await message.answer(ai_result)


async def main():
    print("🤖 Bot ishga tushdi")
    await dp.start_polling(
        bot,
        polling_timeout=60,
        request_timeout=60
    )

if __name__ == "__main__":
    asyncio.run(main())
