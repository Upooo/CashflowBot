from pyrogram import Client
from Cashflow.callbacks import start_cb, note_cb, wishlist_cb
from config import BOT_TOKEN, API_ID, API_HASH
from Cashflow.core.database import mongo, models
from Cashflow.modules import (
    start, note, delnote, check, saldo, wishlist, saving, reset
)

app = Client(
    "cashflow_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

def register_all(app):
    # init db indexes
    mongo.init_db()
    # register modules (handlers + callbacks inside them)
    start.register(app)
    note.register(app)
    delnote.register(app)
    check.register(app)
    saldo.register(app)
    wishlist_cb.register(app)
    saving.register(app)
    reset.register(app)
    start_cb.register(app)
    note_cb.register(app)
    wishlist_cb.register(app)

if __name__ == "__main__":
    register_all(app)
    print("✅ Cashflow Bot running...")
    app.run()
