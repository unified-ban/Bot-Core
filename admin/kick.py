#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from Utils.decorators import permissions, message
from Utils.helpers import h_message, h_group
from Utils import logger, sql
import Params
import datetime

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


'''
Kick user from group
'''
@permissions.is_admin('admin_kick_init')
@message.delete_input
def init(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot
		
		message = update.message
		chat_id = message.chat_id
		
		if message.reply_to_message:
			'''
			The user is provided by quoting a message
			get user_id from the source
			'''
			user = message.reply_to_message.from_user
			
			bot.kick_chat_member(
				message.chat_id, 
				user.id
			)
			bot.unban_chat_member(
				message.chat_id, 
				user.id
			)
			output = bot.send_message(chat_id, lang.kick % user.name)
			db = sql.Database(update); db.insert_chatoperationslog("kick:%s" % user.id)
			return h_message.delete(output, context, 5)
		else:
			'''
			No message has been quoted
			output an error message
			'''
			return bot.send_message(chat_id, lang.no_user_specified)
	except Exception as e:
		logger.exception(e)