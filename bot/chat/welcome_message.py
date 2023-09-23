from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import config
from telegram import ChatMember
import logging

# setup logger
logger = logging.getLogger(__name__)

# detect statu of the member entering or leaving the chat
def extract_status_change(chat_member_update):
    """Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
    of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
    the status didn't change.
    """
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    is_member = new_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)

    return was_member, is_member


# welcome message
async def func(update, context):
    """Welcome new users in chats and announces when someone leaves"""

    result = extract_status_change(update.chat_member)
    if result is None:
        return

    # detect change (user enters or exits the chat)
    was_member, is_member = result
    member_name = update.chat_member.new_chat_member.user.mention_html()
    
    # # detect change (user enters or exits the chat)
    # was_member, is_member = update.chat_member.difference().get("is_member", (None, None))
    # member_name = update.chat_member.new_chat_member.user.mention_html()
    # welcome text
    welcome_text = "Benvenuto {} in <b>{}</b>!\n\nTi preghiamo di rispettare le regole per non ricevere sanzioni e ti invitiamo anche a visitare gli altri gruppi del nostro network!"
    
    # hndle new user
    if not was_member and is_member:
        if update.chat_member.chat.id == config.group['pixel']['id']:
            
            keyboard = [
                [InlineKeyboardButton("Somme Regole 📜", url='https://telegra.ph/Google-Pixel-Italia-07-29')],
                [InlineKeyboardButton("macOS Italia", url='https://t.me/macOSItalia')],
                [InlineKeyboardButton("FOSS Italia", url='https://t.me/fossitaly')]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(chat_id=config.group['pixel']['id'],
                                           text=welcome_text.format(member_name, update.chat_member.chat.title),
                                           message_thread_id=config.group['pixel']['main_topic'],
                                           reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        
        elif update.chat_member.chat.id == config.group['macos']['id']:
            
            keyboard = [
                [InlineKeyboardButton("Somme Regole 📜", url='https://telegra.ph/Google-Pixel-Italia-07-29')],
                [InlineKeyboardButton("Google Pixel Italia", url='https://t.me/googlepixelit')],
                [InlineKeyboardButton("FOSS Italia", url='https://t.me/fossitaly')]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(chat_id=config.group['macos']['id'],
                                            text=welcome_text.format(member_name, update.chat_member.chat.title),
                                            reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        
        elif update.chat_member.chat.id == config.group['foss']['id']:
            
            keyboard = [
                [InlineKeyboardButton("Somme Regole 📜", url='https://telegra.ph/Google-Pixel-Italia-07-29')],
                [InlineKeyboardButton("Google Pixel Italia", url='https://t.me/googlepixelit')],
                [InlineKeyboardButton("macOS Italia", url='https://t.me/macOSItalia')]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(chat_id=config.group['foss']['id'],
                                        text=welcome_text.format(member_name, update.chat_member.chat.title),
                                        reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        
        else:
            
            keyboard = [
                [InlineKeyboardButton("Somme Regole 📜", url='https://telegra.ph/Google-Pixel-Italia-07-29')],
                [InlineKeyboardButton("Google Pixel Italia", url='https://t.me/googlepixelit')],
                [InlineKeyboardButton("macOS Italia", url='https://t.me/macOSItalia')],
                [InlineKeyboardButton("FOSS Italia", url='https://t.me/fossitaly')]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(chat_id=update.chat_member.chat.id,
                                           text=welcome_text.format(member_name, update.chat_member.chat.title),
                                           reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            
        
        logger.info("NEW USER. id: %s - name: %s - chat: %s - chat id: %s",
                    update.chat_member.new_chat_member.user.id,
                    update.chat_member.new_chat_member.user.name,
                    update.chat_member.chat.title,
                    update.chat_member.chat.id)
        
    # hndle user who leave the group
    elif was_member and not is_member:
        await update.effective_chat.send_message(chat_id=config.group['log']['id'],
                                                 text=f"{member_name} ha lasciato il gruppo {update.chat_member.chat.title}",
                                                 parse_mode=ParseMode.HTML)

        logger.info("LOST USER. id: %s - name: %s - chat: %s - chat id: %s",
                        update.chat_member.new_chat_member.user.id,
                        update.chat_member.new_chat_member.user.name,
                        update.chat_member.chat.title,
                        update.chat_member.chat.id)
