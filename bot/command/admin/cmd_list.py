from util.decorator import restricted
from telegram.constants import ParseMode


@restricted
async def func(update, context):
    msg = "<b>Comandi disponibili:</b>\n\n"
    msg+= "  <b>Admin:</b>\n"
    msg+= "  <code>\\autoban motivo</code> *\n"
    msg+= "  <code>\\autokick motivo</code> *\n"
    msg+= "  <code>\\ban</code> *\n"
    msg+= "  <code>\\unban</code> *\n"
    msg+= "  <code>\\kick</code> *\n"
    msg+= "  <code>\\mute</code> *\n"
    msg+= "  <code>\\unmute</code> *\n"
    msg+= "  <code>\\pin</code> *\n"
    msg+= "  <code>\\slow flag n_mex seconds</code> * *\n"
    msg+= "  <code>\\cmd_list</code>\n"
    msg+= "  <code>\\log</code>\n\n"
    msg+= "  <b>User:</b>\n"
    msg+= "  <code>\\start</code>\n"
    msg+= "  <code>\\help</code>\n\n\n"
    msg+= "* in risposta ad un messaggio\n"
    msg+= "* parametro \slow:\n"
    msg+= "   - <code>flag</code>: 0 disattico, 1 attovo\n"
    msg+= "   - <code>n_mex</code>: max messaggi consecutivi\n"
    msg+= "   - <code>seconds</code>: numero secondi di mute\n"

    # send command
    await context.bot.send_message(chat_id=update.message.from_user.id, text=msg, parse_mode=ParseMode.HTML)

    # clean chat
    await context.bot.delete_message(update.message.chat_id, update.message.message_id)
    