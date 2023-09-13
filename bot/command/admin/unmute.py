# import modules
from util.decorator import restricted
from telegram import ChatPermissions
from telegram.constants import ParseMode
import logging

# setup logger
logger = logging.getLogger(__name__)


@restricted
async def func(update, context):
    
    
    await context.bot.restrict_chat_member(update.message.chat_id,update.message.reply_to_message.from_user.id,
                                           ChatPermissions(can_send_messages=True,
                                                           can_send_other_messages=True,
                                                           can_add_web_page_previews=True,
                                                           can_send_polls=True))
    
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
    await update.message.reply_text(text="<b>Unmute process</b>\n\n"
                                            "User_id: <code>{}</code>\n"
                                            "Name: {}\n"
                                            "Username: @{}\n\n"
                                            "Succesfully unmuted".format(update.message.reply_to_message.from_user.id,
                                                                        update.message.reply_to_message.from_user.first_name,
                                                                        update.message.reply_to_message.from_user.username),
                                                                        parse_mode=ParseMode.HTML)
    # clean chat
    await context.bot.delete_message(update.message.chat_id, update.message.message_id)

