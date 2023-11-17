# import modules
from util.decorator import restricted
from util.common import id_by_username
from telegram.error import BadRequest
import asyncio
import logging

# setup logger
logger = logging.getLogger(__name__)


@restricted
async def func(update, context):

    # get additional parameters
    text = context.args

    if (update.message.reply_to_message is None) or (update.message.reply_to_message.text is None):
        # get user_id or username
        if not text:
            logger.error("unban command called with no 'id' or 'username'".format(text[0]))
            return
        elif len(text) == 1:
            user_input = text[0]
        elif len(text) > 1:
            logger.error("unban command called with more than one argument".format(text[0]))
        
        # get userid
        try:
            user_id = int(user_input)
        except ValueError:
            user_id = id_by_username(user_input)
        # if user is None stop execution
        if user_id is None:
            logger.error("user {} not found".format(text[0]))
            return
        
        # get data
        chat_title = update.message.chat.title
        chat_id = update.message.chat_id
        try:
            user_info = await context.bot.get_chat_member(chat_id, user_id)
        except BadRequest:
            logger.error("user {} not found".format(user_id))
            return
        first_name = user_info.user.first_name
        username = user_info.user.username
        admin_name = update.message.from_user.username
        

    else:
        # get data
        chat_title = update.message.chat.title
        chat_id = update.message.chat_id
        user_id = update.message.reply_to_message.from_user.id
        first_name = update.message.reply_to_message.from_user.first_name
        username = update.message.reply_to_message.from_user.username
        admin_name = update.message.from_user.username
    
    
    await context.bot.unban_chat_member(chat_id, user_id)
    await asyncio.sleep(1)
    # log message
    log_message="action: unban - Chat: {}" \
                " - Chat_id: {}" \
                " - User_id: {}" \
                " - Name: {}" \
                " - Username: @{}" \
                " - Performed by admin: @{}".format(chat_title,
                                                    chat_id,
                                                    user_id,
                                                    first_name,
                                                    username,
                                                    admin_name)
    
    
    
    # clean chat
    await context.bot.delete_message(chat_id, update.message.message_id)
    # log ban
    logger.info(log_message)