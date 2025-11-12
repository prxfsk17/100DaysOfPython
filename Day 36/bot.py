from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext
import os

class Bot:

    def __init__(self, text):
        self.TOKEN = os.environ.get("TOKEN")
        self.application = Application.builder().token(self.TOKEN).build()
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("aapl", self.aapl))
        self.application.add_handler(CommandHandler("help", self.help))
        self.text = text
        self.application.run_polling()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sends a welcome message when the /start command is issued."""
        user = update.effective_user
        username = user.username
        if username:
            await update.message.reply_text(f"Привет, @{username}!")
        else:
            await update.message.reply_text("Привет!")

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Shows users what bot can do."""
        await update.message.reply_text("Вот, что я умею:\n1. /start - Приветствие с пользователем. \n2. /help - Что бот умеет делать. \n"
                                        "3. /aapl - Узнать об акциях Apple Inc. за последний торговый день.")

    async def aapl(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Apple stock"""
        await update.message.reply_text(self.text)

