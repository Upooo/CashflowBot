from pyrogram import filters
from pyrogram.types import Message
from Cashflow.core.database.models import get_notes, delete_note_by_id
from Cashflow.utils.utils import format_note_doc

# delete flow uses plain messages: user runs /delnote then sends id-prefix or full id
def register(app):
    @app.on_message(filters.command("delnote"))
    async def delnote_cmd(client, message: Message):
        user_id = message.from_user.id
        notes = get_notes(user_id, limit=50)
        if not notes:
            await message.reply("Belum ada catatan buat dihapus.")
            return
        text = "Ketik ID (6 char awal) atau full ID note yang mau dihapus.\nContoh kirim: `abc123`\n\n"
        text += "\n".join([format_note_doc(n) for n in notes[:20]])
        await message.reply(text)

    @app.on_message(filters.text & ~filters.regex(r"^/"))
    async def delnote_input(client, message: Message):
        user_id = message.from_user.id
        txt = message.text.strip()
        # try match by prefix
        notes = get_notes(user_id, limit=200)
        match = None
        for n in notes:
            sid = str(n.get("_id"))
            if sid.startswith(txt):
                match = n
                break
        if match:
            nid = str(match.get("_id"))
            success = delete_note_by_id(user_id, nid)
            if success:
                await message.reply("✅ Note berhasil dihapus.")
            else:
                await message.reply("Gagal hapus note.")
            return

        # try full id deletion
        try:
            ok = delete_note_by_id(user_id, txt)
            if ok:
                await message.reply("✅ Note berhasil dihapus.")
            else:
                await message.reply("Gak ketemu ID yang cocok.")
        except Exception:
            await message.reply("Gagal hapus. Pastikan ID valid.")
