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
Change group language
'''
@permissions.is_admin('admin_language_init')
@message.delete_input
def init(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot
		
		db = sql.Database(update)
		message = update.message
		chat_id = message.chat_id
		language_text = update.message.text[10:]
		
		if language_text and len(language_text) <= 5 and language_text in Params.common.supported_languages:
			'''
			Check if the string passed matches in length
			and is a supported language
			'''
			output = bot.send_message(chat_id, lang.language_set, parse_mode=ParseMode.HTML)
			db.update_groups('ConfLang', h_sql.string(language_text))
			db = sql.Database(update); db.insert_chatoperationslog("ConfLang")
			return h_message.delete(output, context, 5)
		else:
			'''
			Language string was not passed
			output an error message'''
			bot.send_message(chat_id, lang.language_help, parse_mode=ParseMode.HTML)
			return False
	except Exception as e:
		logger.exception(e)