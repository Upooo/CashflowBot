from pyrogram import filters
from pyrogram.types import Message
from Cashflow.utils.keyboards import main_menu

def register(app):
    @app.on_message(filters.command("start"))
    async def start_handler(client, message: Message):
        text = (
            "👋 Halo cuy!\n"
            "Gue *Cashflow Bot* — bantuin lu catet pemasukan & pengeluaran.\n\n"
            "Pilih menu di bawah buat mulai:"
        )
        await message.reply(text, reply_markup=main_menu())
