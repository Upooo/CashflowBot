from pyrogram import filters
from pyrogram.types import Message
from Cashflow.core.database.models import (
    add_wishlist, get_wishlist, delete_wishlist_by_name,
    set_wishlist_status, update_wishlist_saved
)
from Cashflow.core.helpers.utils import rupiah

# simple states for add/del flows
wish_states = {}

def register(app):
    @app.on_message(filters.command("addwhist"))
    async def add_whist_cmd(client, message: Message):
        user_id = message.from_user.id
        wish_states[user_id] = {"step": "name"}
        await message.reply("🎯 Masukkan nama keinginan (contoh: PS5):")

    @app.on_message(filters.command("whislist"))
    async def list_whis(client, message: Message):
        user_id = message.from_user.id
        wishes = get_wishlist(user_id)
        if not wishes:
            await message.reply("Belum ada wishlist nih.")
            return
        text = "🎯 Wishlist:\n"
        for w in wishes:
            text += f"- `{str(w.get('_id'))[:6]}` {w.get('name')} | Target: {rupiah(w.get('target_price'))} | Saved: {rupiah(w.get('saved'))} | Status: {w.get('status')}\n"
        await message.reply(text)

    @app.on_message(filters.command("delwhist"))
    async def del_whis_cmd(client, message: Message):
        user_id = message.from_user.id
        wishes = get_wishlist(user_id)
        if not wishes:
            await message.reply("Belum ada wishlist buat dihapus.")
            return
        text = "Ketik nama wishlist yang mau dihapus (nama persis):\n"
        text += "\n".join([f"- {w.get('name')} (ID:`{str(w.get('_id'))[:6]}`)" for w in wishes])
        wish_states[user_id] = {"step": "del_confirm"}
        await message.reply(text)

    @app.on_message(filters.text & ~filters.regex(r"^/"))
    async def wish_flow(client, message: Message):
        user_id = message.from_user.id
        if user_id not in wish_states:
            return
        state = wish_states[user_id]

        if state["step"] == "name":
            name = message.text.strip()
            state["name"] = name
            state["step"] = "price"
            await message.reply("Masukkan target harga (contoh: 2500000):")
            return

        if state["step"] == "price":
            try:
                price = int(message.text.replace(".", "").replace(",", "").strip())
                nid = add_wishlist(user_id, state["name"], price)
                await message.reply(f"✅ Wishlist ditambah: {state['name']} | Target: {rupiah(price)}\nID: `{nid}`")
                del wish_states[user_id]
            except Exception:
                await message.reply("Format harga salah. Coba lagi tanpa tanda titik/komma.")
            return

        if state["step"] == "del_confirm":
            name = message.text.strip()
            ok = delete_wishlist_by_name(user_id, name)
            if ok:
                await message.reply(f"✅ Wishlist `{name}` dihapus.")
            else:
                await message.reply("Gagal menemukan wishlist dengan nama itu. Pastikan nama persis.")
            del wish_states[user_id]
            return
