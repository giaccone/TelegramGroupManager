from telegram.constants import ParseMode


async def func(update, context):
    """
    'start' provides the start message

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    msg = "Ciao,\nsono <b>Group Manager</b>\n<code>(@gm_the_bot)</code>\n\n"
    msg += "I miei sviluppatori mi hanno programmato per funzionare solo nei loro gruppi.\n"
    msg += "Contatta loro se sei interessato ad utilizzarmi nel tuo gruppo."

    await context.bot.send_message(chat_id=update.message.chat_id,
                             text=msg,
                             parse_mode=ParseMode.HTML, disable_web_page_preview=True)