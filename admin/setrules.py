#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from telegram import ParseMode
from Utils.decorators import permissions, message
from Utils.helpers import h_message, h_sql, h_group
from Utils import logger, sql

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language

'''
Update rules message
'''
@permissions.is_admin('admin_setrules_init')
@message.delete_input
def init(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot
		
		db = sql.Database(update)
		message = update.message
		chat_id = message.chat_id
		rules_text = update.message.text[10:]
		
		if rules_text:
			'''
			Rules text is defined, save it in the database
			'''
			output = bot.send_message(chat_id, lang.rules_set, parse_mode=ParseMode.HTML)
			db.update_groups('RulesText', rules_text)
			db = sql.Database(update); db.insert_chatoperationslog("SetRules")
			return h_message.delete(output, context, 5)
		else:
			'''
			Rules text was not defined
			output an error message'''
			bot.send_message(chat_id, lang.rules_help, parse_mode=ParseMode.HTML)
			return False
	except Exception as e:
		logger.exception(e)