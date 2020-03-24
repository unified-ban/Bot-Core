#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message
from Utils import logger
import time

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language

'''
Delete messages
'''
@permissions.is_admin('admin_delete_init')
@message.delete_input
def init(update, context):
	try:
		bot = context.bot

		counter = 0
		num = update.message.text[4:]
		chat_id = update.message.chat.id
		message_id = update.message.reply_to_message.message_id
		
		if num:
			'''
			Delete more than one message by the number 
			provided with the command
			'''
			num = int(float(num))
			if num > 20:
				bot.send_message(chat_id, lang.delete_max)
			else:
				for i in range(0, num):
					counter+=1
					if counter % 10 == 0:
						time.sleep(5)
					message_id = int(message_id)+1
					try:
						bot.deleteMessage(chat_id, message_id)
					except:
						pass
				return True
		else:
			'''
			Delete only one message
			'''
			message = update.message.reply_to_message
			return bot.deleteMessage(chat_id, message_id)
	except Exception as e:
		logger.exception(e)