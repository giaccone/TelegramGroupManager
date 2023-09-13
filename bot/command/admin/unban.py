# import modules
from util.decorator import restricted
import asyncio
import logging

# setup logger
logger = logging.getLogger(__name__)


@restricted
async def func(update, context):
    
    
    await context.bot.unban_chat_member(update.effective_message.chat_id, update.message.reply_to_message.from_user.id)
    await asyncio.sleep(1)
    # log message
    log_message="action: unban - Chat: {}" \
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
    
    
    
    # clean chat
    await context.bot.delete_message(update.message.chat_id, update.message.message_id)
    # log ban
    logger.info(log_message)