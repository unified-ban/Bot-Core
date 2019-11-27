#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message
from Utils.helpers import h_message, h_group
from Utils import sql

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


'''
Ban user from group
'''
@permissions.is_admin('admin_delete_init')
@message.delete_input
def init(update, context, unban=False):
	try:
		# get group language from config
		lang = h_group.get_language(update)
		
		bot = context.bot
		
		message = update.message
		chat_id = message.chat_id
		
		if message.reply_to_message:
			user = message.reply_to_message.from_user
			if unban == False:
				'''
				ban user (unban = False)
				'''
				bot.kick_chat_member(message.chat_id, user.id)
				output = bot.send_message(chat_id, lang.ban % user.name)
				db = sql.Database(update); db.insert_chatoperationslog("ban:%s" % user.id)
			else:
				'''
				unban user (unban = True)
				'''
				bot.unban_chat_member(message.chat_id, user.id)
				output = bot.send_message(chat_id, lang.unban % user.name)
				db = sql.Database(update); db.insert_chatoperationslog("unban:%s" % user.id)
			return h_message.delete(output, context, 5)
		else:
			return bot.send_message(chat_id, lang.no_user_specified)
	except Exception as e:
		logger.exception(e)


'''
Unban user from group
'''
def unban(update, context):
	return init(update, context, unban=True)