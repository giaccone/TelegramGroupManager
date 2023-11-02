from util.decorator import restricted
import asyncio
import logging

# setup logger
logger = logging.getLogger(__name__)


@restricted
async def func(update, context):

    # get reason
    text = context.args
    if not text:
        text = "starndard kick"
    else:
        text = " ".join(text)

    # kick
    await context.bot.ban_chat_member(update.message.chat.id, update.message.reply_to_message.from_user.id)
    await asyncio.sleep(2)
    await context.bot.unban_chat_member(update.message.chat.id, update.message.reply_to_message.from_user.id)
    # log message
    log_message="action: ban - Chat: {}" \
                " - Chat_id: {}" \
                " - User_id: {}" \
                " - Name: {}" \
                " - Username: @{}" \
                " - Performed by admin: @{}" \
                " - kick reason: {}".format(update.message.chat.title,
                                        update.message.chat_id,
                                        update.message.reply_to_message.from_user.id,
                                        update.message.reply_to_message.from_user.first_name,
                                        update.message.reply_to_message.from_user.username,
                                        update.message.from_user.username,
                                        text)
   
    
    
    # log kick
    logger.info(log_message)

    # clean chat
    await context.bot.delete_message(update.message.chat_id, update.message.message_id)

