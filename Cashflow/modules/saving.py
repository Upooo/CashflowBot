from pyrogram import filters
from pyrogram.types import Message
from Cashflow.core.database.models import get_wishlist, add_saving_record, update_wishlist_saved
from Cashflow.utils.utils import rupiah

# saving_states[user_id] = {"step": "choose" or "amount", "tujuan": "general" or wishlist_id}
saving_states = {}

def register(app):
    @app.on_message(filters.command("saving"))
    async def saving_cmd(client, message: Message):
        user_id = message.from_user.id
        wishes = get_wishlist(user_id)
        text = "Pilih tujuan menabung:\n- ketik `general` untuk tabungan umum\n- atau ketik ID (6 char awal) wishlist untuk pilih wishlist\n\nWishlist kamu:\n"
        if wishes:
            for w in wishes:
                text += f"- `{str(w.get('_id'))[:6]}` {w.get('name')} | Target: {rupiah(w.get('target_price'))} | Saved: {rupiah(w.get('saved'))}\n"
        else:
            text += "Belum ada wishlist."
        saving_states[user_id] = {"step": "choose"}
        await message.reply(text)

    @app.on_message(filters.text & ~filters.regex(r"^/"))
    async def saving_flow(client, message: Message):
        user_id = message.from_user.id
        if user_id not in saving_states:
            return
        state = saving_states[user_id]
        txt = message.text.strip()

        if state["step"] == "choose":
            if txt.lower() == "general":
                state["tujuan"] = "general"
                state["step"] = "amount"
                await message.reply("Masukkan jumlah yang ingin ditabung:")
                return
            # try match wishlist id prefix or exact name
            wishes = get_wishlist(user_id)
            matched = None
            for w in wishes:
                if str(w.get("_id")).startswith(txt) or w.get("name") == txt:
                    matched = w
                    break
            if matched:
                state["tujuan"] = str(matched.get("_id"))
                state["step"] = "amount"
                await message.reply(f"Menabung ke wishlist `{matched.get('name')}` — masukkan jumlah:")
            else:
                await message.reply("Gak ketemu wishlist. Ketik `general` atau ID (6 char awal) dari wishlist.")
            return

        if state["step"] == "amount":
            try:
                amount = int(txt.replace(".", "").replace(",", "").strip())
                tujuan = state["tujuan"]
                add_saving_record(user_id, tujuan, amount)
                if tujuan != "general":
                    update_wishlist_saved(user_id, tujuan, amount)
                await message.reply(f"✅ Berhasil menabung {rupiah(amount)} ke `{tujuan if tujuan=='general' else tujuan[:6]}`")
                del saving_states[user_id]
            except Exception:
                await message.reply("Format jumlah salah. Masukkan angka tanpa titik/komma.")
            return
