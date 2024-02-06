from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import config
from telegram import ChatMember, ChatPermissions
from random import randint, sample, shuffle
import logging
import uuid
import asyncio

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


def generate_capthca():
    """generate data for captcha"""
    
    x = randint(0, 5)
    y = randint(0, 5)
    x_plus_y = x + y
    answers = sample([k for k in range(11) if k !=x_plus_y], 3) + [x_plus_y]
    shuffle(answers)
    
    return x, y, x_plus_y, answers


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
    question_text = "Buongiorno {}\n\nPotrai scrivere nel gruppo solo dopo aver risposto alla seguente domanda.\n\n<b>Quanto fa {} + {}?</b>"
    # handle new user
    if not was_member and is_member:
        # mute new member
        await context.bot.restrict_chat_member(update.chat_member.chat.id,
                                               update.chat_member.new_chat_member.user.id,
                                               ChatPermissions(can_send_messages=False))

        # generate capthca
        x, y, x_plus_y, answers = generate_capthca()

        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(answers[0], callback_data=answers[0]),
                                              InlineKeyboardButton(answers[1], callback_data=answers[1])],
                                              [InlineKeyboardButton(answers[2], callback_data=answers[2]),
                                               InlineKeyboardButton(answers[3], callback_data=answers[3])]])
        
        # send CAPTCHA (in main thread if topics are enabled)
        msg = await context.bot.send_message(chat_id=update.chat_member.chat.id,
                                           text=question_text.format(member_name, x, y),
                                           reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        
        
        # set delayed kick for users that do not respond to the captcha after a given delay
        async def delayed_ban(context, update=update, msg=msg):
            # kick
            await context.bot.ban_chat_member(chat_id=update.chat_member.chat.id,
                                              user_id=update.chat_member.new_chat_member.user.id)
            await asyncio.sleep(2)
            await context.bot.unban_chat_member(chat_id=update.chat_member.chat.id,
                                                user_id=update.chat_member.new_chat_member.user.id)
            # clean chat
            await context.bot.delete_message(chat_id=update.chat_member.chat.id,
                                            message_id=msg.message_id)
            # log CAPTCHA sent
            logger.info("action: kick. id: %s - name: %s - chat: %s - chat id: %s - reason: CAPTCHA timeout",
                        update.chat_member.new_chat_member.user.id,
                        update.chat_member.new_chat_member.user.name,
                        update.chat_member.chat.title,
                        update.chat_member.chat.id)

        seconds = 600  # 10 minutes
        job = context.job_queue.run_once(delayed_ban, seconds)
        
        # generate a random key
        key = str(uuid.uuid4())
        # bind InlineKeyboard to user by means of chat_data and user_data
        context.chat_data[msg.message_id] = dict()
        context.chat_data[msg.message_id]['question_key'] = key
        context.chat_data[msg.message_id]['answer'] = x_plus_y
        context.chat_data[msg.message_id]['job'] = job
        context.user_data[update.chat_member.new_chat_member.user.id] = key
        
        # log CAPTCHA sent
        logger.info("CAPTCHA sent. id: %s - name: %s - chat: %s - chat id: %s",
                    update.chat_member.new_chat_member.user.id,
                    update.chat_member.new_chat_member.user.name,
                    update.chat_member.chat.title,
                    update.chat_member.chat.id)
        
    
    # hndle user who leave the group
    elif was_member and not is_member:
        await context.bot.send_message(chat_id=config.group['log']['id'],
                                       text="<b>LOST USER:</b>\n * id: {}\n * name: {}\n * chat id: {}\n * chat: {}".format(update.chat_member.new_chat_member.user.id,
                                                                                                                            update.chat_member.new_chat_member.user.name,
                                                                                                                            update.chat_member.chat.id,
                                                                                                                            update.chat_member.chat.title),
                                       parse_mode=ParseMode.HTML)

        logger.info("LOST USER. id: %s - name: %s - chat: %s - chat id: %s",
                        update.chat_member.new_chat_member.user.id,
                        update.chat_member.new_chat_member.user.name,
                        update.chat_member.chat.title,
                        update.chat_member.chat.id)
