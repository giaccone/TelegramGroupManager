# import modules
from util.decorator import restricted


@restricted
async def func(update, context):
    # pin message
    await context.bot.pin_chat_message(chat_id=update.message.chat_id,
                                       message_id=update.message.reply_to_message.message_id,
                                       disable_notification=False)
    
    # clean chat
    await context.bot.delete_message(update.message.chat_id, update.message.message_id)