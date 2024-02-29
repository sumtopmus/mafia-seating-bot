from dynaconf import settings
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters
import logging

import utils


def create_handlers() -> list:
    """Creates handlers that process nickname command."""
    return [CommandHandler('nickname', nickname, filters.User(username=settings.ADMINS))]


async def nickname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sets/displays nickname."""
    utils.log('nickname')
    try:
        if not context.args:
            utils.log('empty')
            # utils.log((f'User#{update.effective_user.id} ({update.effective_user.full_name}) has nickname '
            #            f'{context.user_data['nickname']}.'), logging.INFO)
            # message = f'Your current nickname is {context.user_data['nickname']}'
            # await context.bot.sendMessage(chat_id=update.message.chat.id, text=message)
        if len(context.args) > 1:
            raise ValueError()
        context.user_data['nickname'] = context.args[0]
    except Exception:
        context.bot.send_message(chat_id=update.message.chat.id, text='Something went wrong... Check your arguments.')
