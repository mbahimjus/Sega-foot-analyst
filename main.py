import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import BOT_TOKEN
from db import init_db
from provider import fetch_match_by_number, MatchProviderNotConfigured


logging.basicConfig(level=logging.INFO)

dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Bienvenue sur Sega Foot Analyst ! ⚽\n\n"
        "Utilise /help pour voir les commandes disponibles."
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Commandes disponibles :\n"
        "/start - Démarrer le bot\n"
        "/help - Afficher l'aide\n"
        "/match NUMERO - Rechercher un match"
    )


@dp.message(Command("match"))
async def match_command(message: Message):
    parts = (message.text or "").split(maxsplit=1)

    if len(parts) < 2:
        await message.answer(
            "Utilisation : /match NUMERO\n"
            "Exemple : /match 12345"
        )
        return

    event_number = parts[1].strip()

    try:
        match = await fetch_match_by_number(event_number)
        await message.answer(str(match))

    except MatchProviderNotConfigured as error:
        await message.answer(
            f"Le service de récupération des matchs n'est pas encore activé.\n{error}"
        )

    except Exception:
        logging.exception("Erreur pendant la recherche du match")
        await message.answer("Une erreur est survenue. Réessaie plus tard.")


async def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "Le jeton Telegram est absent. Vérifie la variable TELEGRAM_BOT_TOKEN."
        )

    init_db()

    bot = Bot(token=BOT_TOKEN)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
