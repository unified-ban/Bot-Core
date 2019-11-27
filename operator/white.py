#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message
from Utils import logger, sql
from telegram import ParseMode

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


'''
Remove user from blacklist
'''
@permissions.is_privileged_operator('operator_white_init')
@message.delete_input
def init(update, context):
	try:
		bot = context.bot

		db = sql.Database(update)
		
		message = update.message
		operator_id = message.from_user.id
		
		if message.reply_to_message:
			# white from reply
			user_id = message.reply_to_message.from_user.id
		elif message.text[7:] != "":
			# white from user_id
			user_id = message.text[7:]
		else:
			return bot.send_message(chat_id, lang.no_user_specified)
		
		db.delete_blacklist(user_id)
		
		return logger.report(update, context, lang.report_white % (
			operator_id,
			user_id
		))
	except Exception as e:
		logger.exception(e)