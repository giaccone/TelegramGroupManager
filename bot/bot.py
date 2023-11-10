# PTB modules
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler
from telegram.ext import ChatMemberHandler
from telegram.ext import filters
# import token
from config import TOKEN
import chat
from command import command_handler

# other modules
# ------------
import logging

# set basic logging
# -----------------
logging.basicConfig(filename='Nika.log',
                    encoding='utf-8',
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# set higher logging level for httpx/apscheduler to avoid excessive verbosity
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# bot - main
# ==========
def main():
    # initialize bot
    application = ApplicationBuilder().token(TOKEN).build()

    # Handle members joining/leaving chats
    application.add_handler(ChatMemberHandler(chat.captcha.func, ChatMemberHandler.CHAT_MEMBER))

    # Admin commands
    command_handler.admin_command(application)

    # User commands
    command_handler.user_command(application)

    # query reaction for inline buttons
    application.add_handler(CallbackQueryHandler(chat.catch_query.func))

    # check message text and react accordingly
    application.add_handler(MessageHandler(filters.TEXT, chat.conversation_handler.init))


    # Run the bot until the user presses Ctrl-C
    # We pass 'allowed_updates' handle *all* updates including `chat_member` updates
    # To reset this, simply pass `allowed_updates=[]`
    application.run_polling(allowed_updates=Update.ALL_TYPES)


# run the bot
# ===========
if __name__ == '__main__':
    main()
