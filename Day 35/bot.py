from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

class Bot:

    def __init__(self, fl):
        self.TOKEN = os.environ.get("TOKEN")
        self.application = Application.builder().token(self.TOKEN).build()
        self.application.add_handler(CommandHandler("start", self.start))
        self.fl = fl
        self.application.run_polling()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sends a welcome message when the /start command is issued."""
        if self.fl:
            await update.message.reply_text("It looks like precipitation is expected in next the 12 hours. You might want to bring an umbrella.")
        else:
            await update.message.reply_text("It's ok")
