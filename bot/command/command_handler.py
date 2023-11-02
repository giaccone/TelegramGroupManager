# import modules
import command
from telegram.ext import CommandHandler


def admin_command(application):
    application.add_handler(CommandHandler("autoban", command.admin.autoban.func))
    application.add_handler(CommandHandler("autokick", command.admin.autokick.func))
    application.add_handler(CommandHandler("ban", command.admin.ban.func))
    application.add_handler(CommandHandler("kick", command.admin.kick.func))
    application.add_handler(CommandHandler("log", command.admin.log.func))
    application.add_handler(CommandHandler("mute", command.admin.mute.func))
    application.add_handler(CommandHandler("pin", command.admin.pin.func))
    application.add_handler(CommandHandler("slow", command.admin.slow.func))
    application.add_handler(CommandHandler("unban", command.admin.unban.func))
    application.add_handler(CommandHandler("unmute", command.admin.unmute.func))

def user_command(application):
    application.add_handler(CommandHandler("help", command.user.help.func))
    application.add_handler(CommandHandler("start", command.user.start.func))
    
