from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def register(app: Client):

    @app.on_callback_query(filters.regex("^note$"))
    async def note_menu(client, callback_query):
        await callback_query.message.edit_text(
            "📓 Mau catat *Pemasukan* atau *Pengeluaran*?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📈 Pemasukan", callback_data="note_income")],
                [InlineKeyboardButton("📉 Pengeluaran", callback_data="note_expense")],
                [InlineKeyboardButton("⬅ Kembali", callback_data="menu")]
            ])
        )

    @app.on_callback_query(filters.regex("^note_income$"))
    async def note_income(client, callback_query):
        await callback_query.message.edit_text(
            "Masukin nominal pemasukan lu, cuy 💵"
        )
        # nanti di sini lu tambahin state machine biar bot tau input selanjutnya angka

    @app.on_callback_query(filters.regex("^note_expense$"))
    async def note_expense(client, callback_query):
        await callback_query.message.edit_text(
            "Masukin nominal pengeluaran lu, bro 💸"
        )
        # sama kaya di atas, tinggal tambahin handler text
