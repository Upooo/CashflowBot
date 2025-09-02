from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Catat", callback_data="note")],
        [InlineKeyboardButton("➖ Hapus Catatan", callback_data="delnote")],
        [InlineKeyboardButton("🎯 Wishlist", callback_data="wishlist")],
        [InlineKeyboardButton("🏦 Saving", callback_data="saving")],
        [InlineKeyboardButton("💰 Saldo", callback_data="saldo")],
        [InlineKeyboardButton("♻ Reset", callback_data="reset")],
    ])

def note_menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📈 Pemasukan", callback_data="note_income")],
        [InlineKeyboardButton("📉 Pengeluaran", callback_data="note_expense")],
        [InlineKeyboardButton("⬅ Kembali", callback_data="back_menu")],
    ])

def cancel_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Batal", callback_data="cancel_action")]
    ])

def wishlist_confirm_kb(ok_data="whish_success", cancel_data="whish_cancel"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Selesai (success)", callback_data=ok_data)],
        [InlineKeyboardButton("❌ Batal (cancel)", callback_data=cancel_data)],
        [InlineKeyboardButton("⬅ Kembali", callback_data="back_menu")]
    ])
