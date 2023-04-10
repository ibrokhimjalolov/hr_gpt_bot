from .loader import updater
from .handlers import *  # to register handlers

updater.start_polling()
