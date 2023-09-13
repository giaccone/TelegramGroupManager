from functools import wraps
from telegram.error import BadRequest
import logging

# get logger
logger = logging.getLogger(__name__)


# only people from config.LIST_OF_ADMINS can perform that command
def restricted(func):
    @wraps(func)
    async def wrapped(update, context):
        # get user id
        user_id = update.effective_user.id
        # get admin list
        try:
            admin_list = await context.bot.get_chat_administrators(update.effective_chat.id)
            admin_list = [ele.user.id for ele in admin_list]
        except BadRequest:
            logger.warning("PRIVATE CHAT. user id: %s - username %s", user_id, update.effective_user.name)
            return None
        # run 'func' inly if user is admin
        if user_id not in admin_list:
            logger.warning("UNAUTHORIZED access. user id: %s - username: %s - chat_id: %s - chat_title: %s", user_id,
                                                                                                            update.effective_user.name,
                                                                                                            update.effective_chat.id,
                                                                                                            update.effective_chat.title)
            return
        return await func(update, context)
    return wrapped

