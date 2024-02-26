from util.decorator import restricted
from telegram.constants import ParseMode


@restricted
async def func(update, context):
    """
    'say' send a message in the group through the bot
    usage: /say message of the text
    """
    # get text
    msg = update.message.text.replace('/say ','')
    
    #clean chat
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    
    if update.message.reply_to_message is None:
        await context.bot.send_message(chat_id=update.message.chat_id,
                                       text=msg,
                                       parse_mode=ParseMode.HTML,
                                       disable_web_page_preview=True)
    else:
        await context.bot.send_message(chat_id=update.message.chat_id,
                                       text=msg,
                                       parse_mode=ParseMode.HTML,
                                       disable_web_page_preview=True,
                                       reply_parameters =update.message.reply_to_message)