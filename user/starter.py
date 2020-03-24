#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.helpers import h_chat, h_group
from Utils.decorators import chat
from Utils import logger
from telegram import ParseMode

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language

@chat.only_private
def init(update, context):
	try:
		bot = context.bot
		
		chat_id = update.message.chat_id
		return bot.send_message(chat_id, lang.start_text, parse_mode=ParseMode.HTML)
	except Exception as e:
		logger.exception(e)