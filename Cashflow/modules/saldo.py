from pyrogram import filters
from pyrogram.types import Message
from Cashflow.core.database.models import sum_balance
from Cashflow.core.helpers.utils import rupiah

def register(app):
    @app.on_message(filters.command("saldo"))
    async def saldo_cmd(client, message: Message):
        user_id = message.from_user.id
        bal = sum_balance(user_id)
        await message.reply(f"💰 Saldo akhir: {rupiah(bal)}")
