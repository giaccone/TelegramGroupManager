import sqlite3
import logging
from util.decorator import restricted
from telegram.constants import ParseMode
from util.database_functions import isin, remove_user

# setup logger
logger = logging.getLogger(__name__)

# open database
database = 'warning-database.db'
conn = sqlite3.connect(database)
# get cursor
cursor = conn.cursor()
# create table (if not present)
cursor.execute("CREATE TABLE IF NOT EXISTS warning_list ( \
            user_id int, \
            username text, \
            name text, \
            chat_id text, \
            chat_title text, \
            warn_count int)")
conn.commit()

@restricted
async def func(update, context):
    """
    This command is executed sending the command:
        /clearwarn

    The command must be used in reply to the user's message. The bot removes all 'warn' of the
    user. The user is removed from the database completely. A message is sent in the chat notifying
    the user that he has 0 warnings.
    """

    # get data
    chat_title = update.message.chat.title
    chat_id = update.message.chat_id
    user_id = update.message.reply_to_message.from_user.id
    name = update.message.reply_to_message.from_user.first_name
    username = update.message.reply_to_message.from_user.username
    admin_name = update.message.from_user.username

    if isin(conn, user_id, chat_id):
        remove_user(conn, user_id, chat_id)

        # set and send message to the user
        msg = f"<b>All 'warn' removed:</b>\n" \
            f"Current status:\n" \
            f"<b>  * User</b>: @{username}\n" \
            f"<b>  * Warn 0/3</b>.\n"
        await context.bot.send_message(chat_id=update.message.chat_id,
                                        text=msg,
                                        parse_mode=ParseMode.HTML,
                                        reply_parameters=update.message.reply_to_message)

        # log message
        log_message="action: unwarn - Chat: {}" \
                    " - Chat_id: {}" \
                    " - User_id: {}" \
                    " - Name: {}" \
                    " - Username: @{}" \
                    " - Performed by admin: @{}".format(chat_title,
                                                        chat_id,
                                                        user_id,
                                                        name,
                                                        username,
                                                        admin_name)
        
        logger.info(log_message)

    # clean chat
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

    