#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message
from Utils.helpers import h_user
from Utils import logger

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


'''
Get message details
'''
@permissions.is_operator('operator_get_init')
@message.delete_input
def init(update, context):
	try:
		bot = context.bot
		if update.message.reply_to_message:
			reply = update.message.reply_to_message
			
			# from forwarded message
			if update.message.reply_to_message.forward_from:
				fwd_user = update.message.reply_to_message.forward_from
				chat_id = "Not defined"
				message_id = reply.message_id
				user_id = fwd_user.id
				username = fwd_user.username
				is_bot = fwd_user.is_bot
			else:
				# from the quoted message
				chat_id = "Not defined"
				message_id = reply.message_id
				user_id = reply.from_user.id
				username = h_user.get_user_name(update)
				is_bot = reply.from_user.is_bot
		else:
			# from the input message
			message = update.message
			chat_id = message.chat.id
			message_id = message.message_id
			user_id = message.from_user.id
			username = message.from_user.name
			is_bot = message.from_user.is_bot
		
		return logger.report(update, context, lang.report_get % (
				chat_id or "private",
				message_id,
				user_id,
				username or "n/a",
				is_bot
			)
		)
	except Exception as e:
		logger.exception(e)