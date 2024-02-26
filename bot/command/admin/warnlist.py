# import modules
import sqlite3
import logging
from util.decorator import restricted
from telegram.constants import ParseMode

# setup logger
logger = logging.getLogger(__name__)


@restricted
async def func(update, context):
    """
    This command is executed sending the command:
        /warnlist

    The bot sends a txt file including all users in the warn_database for the given chat.
    """

    # open database
    database = 'warning-database.db'
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM warning_list WHERE :chat_id", {"chat_id":update.message.chat_id})
    
    with open('warning_list.txt', 'w') as file:
        for k, ele in enumerate(cursor.fetchall()):
            file.write("{}) user_id: {}, username: {}, name: {}, chat_id: {}, chat_title: {}, warn_count: {}\n".format(k + 1, *ele))
    
    # # send file
    await context.bot.send_document(chat_id=update.message.from_user.id, document=open('warning_list.txt', 'rb'))

    # clean chat
    await context.bot.delete_message(update.message.chat_id, update.message.message_id)
