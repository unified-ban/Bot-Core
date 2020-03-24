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
Pin a group message on the top
'''
@permissions.is_admin('admin_pin_init')
@message.delete_input
def init(update, context):
	try:
		chat_id = update.message.chat_id

		bot = context.bot
		
		if update.message.reply_to_message:
			'''
			Pin the message mentioned in the group
			'''
			message_id = update.message.reply_to_message.message_id
			return bot.pin_chat_message(chat_id, message_id)
		else:
			'''
			Message to pin was not passed
			output an error message
			'''
			# get group language from config
			lang = h_group.get_language(update)
			return bot.send_message(chat_id, lang.pin_no_message)
	except Exception as e:
		logger.exception(e)