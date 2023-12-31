# import modules
from util.decorator import restricted
import logging

# setup logger
logger = logging.getLogger(__name__)


@restricted
async def func(update, context):
    """
    This command is executed sending the command:
        /autoban reason
    
    where 'reason' is a message to explain to the user the reason of the ban

    The command must be used in reply to the user's message. The bot sends a message
    in the chat to the user providing the 'reason'. After 60 seconds the user is banned.
    """
    # decode command
    reason = update.message.text.replace('/autoban ', '').strip()
    # get username
    name = "@" + update.message.reply_to_message.from_user.username \
        if update.message.reply_to_message.from_user.username is not None \
        else update.message.reply_to_message.from_user.name

    # set and send message to the user
    msg = f"{name}, sarai bannato dal gruppo fra 60 secondi per questo motivo:\n\n{reason}"
    await update.message.reply_text(text=msg)
    # log message
    log_message="action: ban - Chat: {}" \
                " - Chat_id: {}" \
                " - User_id: {}" \
                " - Name: {}" \
                " - Username: @{}" \
                " - Performed by admin: @{}" \
                " - ban reason: {}".format(update.message.chat.title,
                                                     update.message.chat_id,
                                                     update.message.reply_to_message.from_user.id,
                                                     update.message.reply_to_message.from_user.first_name,
                                                     update.message.reply_to_message.from_user.username,
                                                     update.message.from_user.username,
                                                     reason)
    await context.bot.delete_message(update.message.chat_id, update.message.message_id)

    # set delayed action
    async def delayed_ban(context, update=update, log_message=log_message):
        await context.bot.ban_chat_member(chat_id=update.message.chat.id,
                                          user_id=update.message.reply_to_message.from_user.id)
        logger.info(log_message)
        

    # schedule action
    seconds = 60
    context.job_queue.run_once(delayed_ban, seconds)
