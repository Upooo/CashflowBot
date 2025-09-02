from pyrogram import filters
from pyrogram.types import Message
from Cashflow.core.database.models import get_notes
from Cashflow.core.helpers.utils import format_note_doc
import datetime

# check flow: /check -> choose day/month/year -> user inputs date string -> bot returns filtered notes

# simple state
check_states = {}

def register(app):
    @app.on_message(filters.command("check"))
    async def check_cmd(client, message: Message):
        await message.reply("Mau lihat transaksi per *hari*, *bulan*, atau *tahun*?\nKetik: hari / bulan / tahun")

    @app.on_message(filters.text & ~filters.regex(r"^/"))
    async def check_input(client, message: Message):
        user_id = message.from_user.id
        txt = message.text.strip().lower()
        if txt in ["hari", "day"]:
            check_states[user_id] = {"mode": "day"}
            await message.reply("Ketik tanggal dengan format `YYYY-MM-DD` contoh: `2025-09-02`")
            return
        if txt in ["bulan", "month"]:
            check_states[user_id] = {"mode": "month"}
            await message.reply("Ketik bulan dengan format `YYYY-MM` contoh: `2025-09`")
            return
        if txt in ["tahun", "year"]:
            check_states[user_id] = {"mode": "year"}
            await message.reply("Ketik tahun dengan format `YYYY` contoh: `2025`")
            return

        # if in mode, parse
        if user_id in check_states:
            mode = check_states[user_id]["mode"]
            try:
                if mode == "day":
                    dt = datetime.datetime.fromisoformat(txt)
                    start = datetime.datetime(dt.year, dt.month, dt.day)
                    end = start + datetime.timedelta(days=1)
                elif mode == "month":
                    year, month = map(int, txt.split("-"))
                    start = datetime.datetime(year, month, 1)
                    if month == 12:
                        end = datetime.datetime(year+1, 1, 1)
                    else:
                        end = datetime.datetime(year, month+1, 1)
                elif mode == "year":
                    year = int(txt)
                    start = datetime.datetime(year, 1, 1)
                    end = datetime.datetime(year+1, 1, 1)
                else:
                    await message.reply("Mode gak dikenali.")
                    del check_states[user_id]
                    return
            except Exception:
                await message.reply("Format salah. Coba lagi sesuai instruksi.")
                return

            # query DB by created_at range
            from Cashflow.core.database.mongo import notes_collection
            docs = list(notes_collection.find({
                "user_id": int(user_id),
                "created_at": {"$gte": start, "$lt": end}
            }).sort("created_at", -1).limit(200))

            if not docs:
                await message.reply("Tidak ada transaksi pada rentang itu.")
            else:
                text = "📋 Transaksi:\n\n" + "\n".join([format_note_doc(d) for d in docs])
                await message.reply(text)
            del check_states[user_id]
            return

        # otherwise ignore (not part of check flow)
