#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message
from Utils.helpers import h_message, h_group
from Utils import logger, sql
import datetime

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


'''
Limit user for 24h in group
'''
@permissions.is_admin('admin_limit_init')
@message.delete_input
def init(update, context, unlimit=False):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot
		
		message = update.message
		chat_id = message.chat_id
		
		if message.reply_to_message:
			user = message.reply_to_message.from_user
			if unlimit == False:
				'''
				limit user (unlimit = False)
				'''
				bot.restrict_chat_member(
					message.chat_id, 
					user.id,
					datetime.datetime.now() + datetime.timedelta(days=1)
				)
				output = bot.send_message(chat_id, lang.limit % user.name)
				db = sql.Database(update); db.insert_chatoperationslog("limit:%s" % user.id)
			else:
				'''
				unlimit user (unlimit = True)
				'''
				bot.restrict_chat_member(
					message.chat_id, 
					user.id, 
					can_send_messages=True, 
					can_send_media_messages=True, 
					can_send_other_messages=True, 
					can_add_web_page_previews=True
				)
				output = bot.send_message(chat_id, lang.unlimit % user.name)
				db = sql.Database(update); db.insert_chatoperationslog("unlimit:%s" % user.id)
			return h_message.delete(output, context, 5)
		else:
			return bot.send_message(chat_id, lang.no_user_specified)
	except Exception as e:
		logger.exception(e)


'''
Unlimit user from group
'''
def unlimit(update, context):
	bot = context.bot

	return init(update, context, unlimit=True)