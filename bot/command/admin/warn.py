# import modules
import sqlite3
import logging
from util.decorator import restricted
from telegram.constants import ParseMode
from util.database_functions import isin, add_user, update_user

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
        /warn reason
    
    where 'reason' is a message to explain to the user the reason of the warn

    The command must be used in reply to the user's message. The bot sends a message
    in the chat to the user providing the number of 'warn' collected so far and 'reason'.
    The third warn corresponds to a automatic ban (delayed by 60 seconds).
    """

    # get additional parameters
    msg_arg = context.args
    # get reason
    if not msg_arg:
        reason = "starndard warn"
    else:
        reason = " ".join(msg_arg)

    # get data
    chat_title = update.message.chat.title
    chat_id = update.message.chat_id
    user_id = update.message.reply_to_message.from_user.id
    name = update.message.reply_to_message.from_user.first_name
    username = update.message.reply_to_message.from_user.username
    admin_name = update.message.from_user.username

    if isin(conn, user_id, chat_id):
        counter = update_user(conn, user_id, chat_id, +1)
        if counter == 3:
            # set and send message to the user
            msg = f"<b>User</b>: {update.message.reply_to_message.from_user.mention_html()}\n" \
                  f"<b>Warn 3/3</b>.\n" \
                  f"<b>Motivo</b>: {reason}.\n\n" \
                  f"Limite raggiunto, sarai bannato dal gruppo fra 60 secondi."
            await context.bot.send_message(chat_id=update.message.chat_id,
                                           text=msg,
                                           parse_mode=ParseMode.HTML,
                                           reply_parameters=update.message.reply_to_message)


            # log message
            log_message="action: ban - Chat: {}" \
                " - Chat_id: {}" \
                " - User_id: {}" \
                " - Name: {}" \
                " - Username: @{}" \
                " - Performed by admin: @{}" \
                " - ban reason: 3 warnings reached".format(chat_title,
                                                           chat_id,
                                                           user_id,
                                                           name,
                                                           username,
                                                           admin_name)

            # set delayed action
            async def delayed_ban(context, update=update, log_message=log_message):
                await context.bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
                
                logger.info(log_message)
            

            # schedule action
            seconds = 60
            context.job_queue.run_once(delayed_ban, seconds)
        else:
            # set and send message to the user
            msg = f"<b>User</b>: @{update.message.reply_to_message.from_user.mention_html()}\n" \
                  f"<b>Warn {counter}/3</b>.\n" \
                  f"<b>Motivo</b>: {reason}.\n\n" \
                  f"(attenzione, tre warn = ban)"
            await context.bot.send_message(chat_id=update.message.chat_id,
                                           text=msg,
                                           parse_mode=ParseMode.HTML,
                                           reply_parameters=update.message.reply_to_message)

            # log message
            log_message="action: warn - Chat: {}" \
                " - Chat_id: {}" \
                " - User_id: {}" \
                " - Name: {}" \
                " - Username: @{}" \
                " - Performed by admin: @{}" \
                " - warn reason: {}" \
                " - counter: {}".format(chat_title,
                                           chat_id,
                                           user_id,
                                           name,
                                           username,
                                           admin_name,
                                           reason,
                                           counter)
            logger.info(log_message)

    
    else:
        counter = add_user(conn, user_id, username, name, chat_id, chat_title)

        # set and send message to the user
        msg = f"<b>User</b>: @{update.message.reply_to_message.from_user.mention_html()}\n" \
              f"<b>Warn {counter}/3</b>.\n" \
              f"<b>Motivo</b>: {reason}.\n\n" \
              f"(attenzione, tre warn = ban)"
        await context.bot.send_message(chat_id=update.message.chat_id,
                                           text=msg,
                                           parse_mode=ParseMode.HTML,
                                           reply_parameters=update.message.reply_to_message)

        # log message
        log_message="action: warn - Chat: {}" \
                " - Chat_id: {}" \
                " - User_id: {}" \
                " - Name: {}" \
                " - Username: @{}" \
                " - Performed by admin: @{}" \
                " - warn reason: {}" \
                " - counter: {}".format(chat_title,
                                           chat_id,
                                           user_id,
                                           name,
                                           username,
                                           admin_name,
                                           reason,
                                           counter)
        logger.info(log_message)
    

    # clean chat
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

