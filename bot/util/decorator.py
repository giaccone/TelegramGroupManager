from functools import wraps
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
        admin_list = await context.bot.get_chat_administrators(update.effective_chat.id)
        admin_list = [ele.user.id for ele in admin_list]
        # run 'func' inly if user is admin
        if user_id not in admin_list:
            logger.warning("Unauthorized access denied for {}.".format(user_id))
            return
        return await func(update, context)
    return wrapped

