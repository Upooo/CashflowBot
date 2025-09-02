from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Cashflow.utils.keyboards import main_menu

def register(app: Client):

    @app.on_callback_query(filters.regex("^menu$"))
    async def back_menu(client, callback_query):
        await callback_query.message.edit_text(
            "👋 Balik ke menu utama:",
            reply_markup=main_menu()
        )

    @app.on_callback_query(filters.regex("^saldo$"))
    async def show_saldo(client, callback_query):
        # sementara placeholder
        await callback_query.message.edit_text("💰 Saldo lu bakal ditampilin disini.")
