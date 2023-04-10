from telegram.ext.updater import Updater
from telegram.update import Update

from django.conf import settings


updater = Updater(settings.BOT_TOKEN, use_context=True)
