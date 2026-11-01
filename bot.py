import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.config import BOT_TOKEN
from app.db import init_db
from app.provider import fetch_match_by_number, MatchProviderNotConfigured

dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "SEGA FOOT ANALYST — prototype. Envoie le numéro numérique d'un événement."
    )

@dp.message()
async def receive_number(message: Message):
    value = (message.text or "").strip()
    if not value.isdigit():
        await message.answer("Envoie uniquement le numéro numérique de l'événement.")
        return
    try:
        data = await fetch_match_by_number(value)
        await message.answer(f"Données reçues : {data}")
    except MatchProviderNotConfigured as exc:
        await message.answer(
            f"Numéro reçu : {value}\n{exc}\nAucune donnée ni prédiction n'a été inventée."
        )

async def main():
    if not BOT_TOKEN:
        raise RuntimeError("Ajoute TELEGRAM_BOT_TOKEN dans le fichier .env")
    init_db()
    await dp.start_polling(Bot(BOT_TOKEN))

if __name__ == "__main__":
    asyncio.run(main())
