from pyrogram import filters
from pyrogram.types import Message
from Cashflow.utils.keyboards import note_menu_kb, cancel_kb
from Cashflow.utils.utils import safe_int, rupiah
from Cashflow.core.database.models import add_note
from datetime import datetime

# in-memory states: states[user_id] = {"type": "income"/"expense", "step": "amount"/"desc", "amount": int}
states = {}

def register(app):
    # /note command -> opens menu
    @app.on_message(filters.command("note"))
    async def note_cmd(client, message: Message):
        await message.reply("📓 Mau catat pemasukan atau pengeluaran?", reply_markup=note_menu_kb())

    # callback for starting the note flow
    @app.on_callback_query(filters.regex("^(note_income|note_expense|cancel_action)$"))
    async def note_cb(client, cq):
        await cq.answer()
        user_id = cq.from_user.id
        data = cq.data

        if data == "cancel_action":
            if user_id in states:
                del states[user_id]
            await cq.message.edit_text("✅ Dibatalkan.", reply_markup=None)
            return

        tipe = "income" if data == "note_income" else "expense"
        states[user_id] = {"type": tipe, "step": "amount"}
        await cq.message.edit_text(f"✍️ Masukkan jumlah untuk *{tipe}* (contoh: 50000)", reply_markup=cancel_kb())

    # message handler to collect amount and description
    @app.on_message(filters.text & ~filters.regex(r"^/"))
    async def note_input(client, message: Message):
        user_id = message.from_user.id
        if user_id not in states:
            return  # not in flow

        state = states[user_id]

        if state["step"] == "amount":
            try:
                amount = safe_int(message.text)
                if amount <= 0:
                    await message.reply("Jumlah harus lebih dari 0. Coba lagi:", reply_markup=cancel_kb())
                    return
                state["amount"] = int(amount)
                state["step"] = "desc"
                await message.reply("📝 Sekarang masukkan keterangan (contoh: makan siang, gaji):", reply_markup=cancel_kb())
            except Exception:
                await message.reply("Format angka salah. Masukkan jumlah tanpa titik/komma, contoh: 50000", reply_markup=cancel_kb())
                return

        elif state["step"] == "desc":
            desc = message.text.strip()
            tipe = state["type"]
            amount = state["amount"]
            nid = add_note(user_id, tipe, amount, desc)
            await message.reply(f"✅ Tercatat: *{tipe}* {rupiah(amount)} — {desc}\nID: `{nid}`")
            del states[user_id]
