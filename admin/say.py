#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils import logger
from Utils.helpers import h_group
from Utils.decorators import permissions, message
from telegram import ParseMode

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


'''
Say staff message as bot
'''
@permissions.is_admin('admin_say_init')
@message.delete_input
def init(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot
		
		message = update.message.text[3:]
		chat_id = update.message.chat_id
		
		if message is not "":
			'''
			The text of the message has been passed
			say it as a bot and pin the output
			'''
			output = bot.send_message(chat_id, lang.say % message, parse_mode=ParseMode.HTML)
			return bot.pin_chat_message(chat_id, output.message_id)
		else:
			'''
			Text to say was not passed
			output an error message
			'''
			return bot.send_message(chat_id, lang.say_no_text)
	except Exception as e:
		logger.exception(e)