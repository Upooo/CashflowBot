from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def register(app: Client):

    @app.on_callback_query(filters.regex("^wishlist$"))
    async def wishlist_menu(client, callback_query):
        await callback_query.message.edit_text(
            "🎯 Mau ngapain di Wishlist?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Tambah", callback_data="wishlist_add")],
                [InlineKeyboardButton("❌ Hapus", callback_data="wishlist_del")],
                [InlineKeyboardButton("⬅ Kembali", callback_data="menu")]
            ])
        )
