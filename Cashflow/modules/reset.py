from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Cashflow.core.database.mongo import notes_collection, wishlist_collection, saving_collection

def register(app):
    @app.on_message(filters.command("reset"))
    async def reset_cmd(client, message: Message):
        user_id = message.from_user.id
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Iya, reset semua data saya", callback_data=f"confirm_reset_{user_id}")],
            [InlineKeyboardButton("❌ Batal", callback_data="cancel_action")]
        ])
        await message.reply("⚠️ Yakin mau reset semua data? (akan menghapus semua notes, wishlist, saving milik lu)", reply_markup=kb)

    @app.on_callback_query(filters.regex("^confirm_reset_"))
    async def confirm_reset(client, cq):
        await cq.answer()
        data = cq.data
        try:
            uid = int(data.split("_")[-1])
        except:
            await cq.message.edit_text("Invalid request.")
            return
        # only requestor can confirm
        if cq.from_user.id != uid:
            await cq.answer("Lu bukan pemilik request ini.", show_alert=True)
            return
        notes_collection.delete_many({"user_id": uid})
        wishlist_collection.delete_many({"user_id": uid})
        saving_collection.delete_many({"user_id": uid})
        await cq.message.edit_text("✅ Semua data lu udah direset.")
