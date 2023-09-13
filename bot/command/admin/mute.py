from util.decorator import restricted
from telegram import ChatPermissions
from telegram.constants import ParseMode
import logging

# setup logger
logger = logging.getLogger(__name__)

@restricted
async def func(update, context):

    # mute action
    await context.bot.restrict_chat_member(update.message.chat_id,update.message.reply_to_message.from_user.id,
                                           ChatPermissions(can_send_messages=False))
    
    # log message
    log_message="action: mute - Chat: {}" \
                " - Chat_id: {}" \
                " - User_id: {}" \
                " - Name: {}" \
                " - Username: @{}" \
                " - Performed by admin: @{}".format(update.message.chat.title,
                                        update.message.chat_id,
                                        update.message.reply_to_message.from_user.id,
                                        update.message.reply_to_message.from_user.first_name,
                                        update.message.reply_to_message.from_user.username,
                                        update.message.from_user.username)
    # log ban
    logger.info(log_message)

    # report on chat
    await update.message.reply_text(text="<b>Mute process</b>\n\nUser_id: <code>{}</code>"
                                    "\nName: {}\nUsername: @{}"
                                    "\n\nSuccesfully muted".format(update.message.reply_to_message.from_user.id,
                                                                   update.message.reply_to_message.from_user.first_name,
                                                                   update.message.reply_to_message.from_user.username),
                                                                   parse_mode=ParseMode.HTML)
    # clean chat
    await context.bot.delete_message(update.message.chat_id, update.message.message_id)


