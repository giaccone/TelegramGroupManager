from util.decorator import restricted
from telegram.constants import ParseMode


@restricted
async def func(update, context):

    # send file
    await context.bot.send_document(chat_id=update.message.from_user.id, document=open('Nika.log', 'rb'))
    
    # clean chat
    await context.bot.delete_message(update.message.chat_id, update.message.message_id)
    