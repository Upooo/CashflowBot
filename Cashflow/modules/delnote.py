from pyrogram import filters
from pyrogram.types import Message
from Cashflow.core.database.models import get_notes, delete_note_by_id
from Cashflow.core.helpers.utils import format_note_doc

# states for deletion: del_states[user_id] = {"step": "choose" or "confirm", "id": note_id}
del_states = {}

def register(app):
    @app.on_message(filters.command("delnote"))
    async def delnote_cmd(client, message: Message):
        user_id = message.from_user.id
        notes = get_notes(user_id, limit=50)
        if not notes:
            await message.reply("Belum ada catatan buat dihapus.")
            return
        text = "Pilih ID note yang mau dihapus (copy ID depan dalam tanda [])\nContoh: kirim `abc123` (6 char pertama)\n\n"
        text += "\n".join([format_note_doc(n) for n in notes[:10]])
        await message.reply(text)

    @app.on_message(filters.text & ~filters.regex(r"^/"))
    async def delnote_input(client, message: Message):
        user_id = message.from_user.id
        txt = message.text.strip()
        # user may send the 6-char id; we try to find match
        notes = get_notes(user_id, limit=200)
        match = None
        for n in notes:
            sid = str(n.get("_id"))
            if sid.startswith(txt):
                match = n
                break
        if not match:
            # maybe it's a full id
            try:
                success = delete_note_by_id(user_id, txt)
                if success:
                    await message.reply("✅ Note berhasil dihapus.")
                else:
                    await message.reply("Gagal hapus. Pastikan ID benar.")
            except Exception:
                await message.reply("Gak ketemu ID-nya. Kirim ID yang valid (6 char awal bisa dipakai).")
            return
        # found note, ask confirm
        nid = str(match.get("_id"))
        # attempt deletion directly (or ask confirm)
        success = delete_note_by_id(user_id, nid)
        if success:
            await message.reply("✅ Note berhasil dihapus.")
        else:
            await message.reply("Gagal hapus note.")
