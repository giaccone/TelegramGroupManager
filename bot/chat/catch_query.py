import asyncio
import logging
from telegram import ChatPermissions
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import config
from telegram.constants import ParseMode

# setup logger
logger = logging.getLogger(__name__)

async def func(update, context):

    # get query
    query = update.callback_query

    # check if the user is answering to his own question
    if context.user_data[query.from_user.id] == context.chat_data[query.message.message_id]['question_key']:
        # if answer is correct send welcome message
        if int(query.data) == context.chat_data[query.message.message_id]['answer']:
            # delet captcha
            await context.bot.delete_message(query.message.chat_id, query.message.message_id)
            
            # unmute member
            await context.bot.restrict_chat_member(query.message.chat.id,
                                                   query.from_user.id,
                                                   ChatPermissions(can_send_messages=True,
                                                                   can_send_other_messages=True,
                                                                   can_add_web_page_previews=True,
                                                                   can_send_polls=True))
            
            # welcome message
            welcome_text = "Benvenuto {} in <b>{}</b>!\n\nTi preghiamo di rispettare le regole per non ricevere sanzioni e ti invitiamo anche a visitare gli altri gruppi del nostro network!"
            welcome_inactive = "Benvenuto {}!\nQuesto gruppo è stato disattivato. Questi sono i nostri gruppi attivi.\n Se stai cercando il mercatino. Adesso è integrato nel gruppo Google Pixel Italia (link qui sotto)."
            member_name = query.from_user.mention_html()

            if query.message.chat.id == config.group['pixel']['id']:
                
                keyboard = [
                    [InlineKeyboardButton("Somme Regole 📜", url='https://telegra.ph/Google-Pixel-Italia-07-29')],
                    [InlineKeyboardButton("macOS Italia", url='https://t.me/macOSItalia')],
                    [InlineKeyboardButton("FOSS Italia", url='https://t.me/fossitaly')]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await context.bot.send_message(chat_id=config.group['pixel']['id'],
                                            text=welcome_text.format(member_name, update.chat_member.chat.title),
                                            message_thread_id=config.group['pixel']['main_topic'],
                                            reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            
            elif query.message.chat.id == config.group['macos']['id']:
                
                keyboard = [
                    [InlineKeyboardButton("Somme Regole 📜", url='https://telegra.ph/Google-Pixel-Italia-07-29')],
                    [InlineKeyboardButton("Google Pixel Italia", url='https://t.me/googlepixelit')],
                    [InlineKeyboardButton("FOSS Italia", url='https://t.me/fossitaly')]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await context.bot.send_message(chat_id=config.group['macos']['id'],
                                                text=welcome_text.format(member_name, update.chat_member.chat.title),
                                                reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            
            elif query.message.chat.id == config.group['foss']['id']:
                
                keyboard = [
                    [InlineKeyboardButton("Somme Regole 📜", url='https://telegra.ph/Google-Pixel-Italia-07-29')],
                    [InlineKeyboardButton("Google Pixel Italia", url='https://t.me/googlepixelit')],
                    [InlineKeyboardButton("macOS Italia", url='https://t.me/macOSItalia')]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await context.bot.send_message(chat_id=config.group['foss']['id'],
                                            text=welcome_text.format(member_name, update.chat_member.chat.title),
                                            reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            
            elif (query.message.chat.id == config.group['modding']['id']) or (query.message.chat.id == config.group['watch']['id']):

                keyboard = [
                    [InlineKeyboardButton("Google Pixel Italia", url='https://t.me/googlepixelit')],
                    [InlineKeyboardButton("macOS Italia", url='https://t.me/macOSItalia')],
                    [InlineKeyboardButton("FOSS Italia", url='https://t.me/fossitaly')]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await context.bot.send_message(chat_id=update.chat_member.chat.id,
                                            text=welcome_inactive.format(member_name),
                                            reply_markup=reply_markup, parse_mode=ParseMode.HTML)

            else:
                
                keyboard = [
                    [InlineKeyboardButton("Somme Regole 📜", url='https://telegra.ph/Google-Pixel-Italia-07-29')],
                    [InlineKeyboardButton("Google Pixel Italia", url='https://t.me/googlepixelit')],
                    [InlineKeyboardButton("macOS Italia", url='https://t.me/macOSItalia')],
                    [InlineKeyboardButton("FOSS Italia", url='https://t.me/fossitaly')]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await context.bot.send_message(chat_id=query.message.chat.id,
                                            text=welcome_text.format(member_name, query.message.chat.title),
                                            reply_markup=reply_markup, parse_mode=ParseMode.HTML)


            # log new unrestricted user
            logger.info("NEW USER. id: %s - name: %s - chat: %s - chat id: %s",
                    query.from_user.id,
                    query.from_user.name,
                    query.message.chat.id,
                    query.message.chat.title)
        
        # if answer is wrong kick user
        else:
            # delet captcha
            await context.bot.delete_message(query.message.chat_id, query.message.message_id)

            # kick
            await context.bot.ban_chat_member(query.message.chat.id,
                                              query.from_user.id)
            await asyncio.sleep(2)
            await context.bot.unban_chat_member(query.message.chat.id,
                                                query.from_user.id)
            
            # log message
            log_message="action: kick - Chat: {}" \
                        " - Chat_id: {}" \
                        " - User_id: {}" \
                        " - Name: {}" \
                        " - Username: @{}" \
                        " - ban reason: CAPTCHA failed".format(query.message.chat.title,
                                                               query.message.chat.id,
                                                               query.from_user.id,
                                                               query.from_user.first_name,
                                                               query.from_user.username)
            # log kink
            logger.info(log_message)

        