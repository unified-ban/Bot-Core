#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from telegram import ParseMode
from Utils.decorators import permissions, message
from Utils.helpers import h_message, h_group
from Utils import logger, sql

'''
Load default language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language

'''
Add bad word for group
'''
@permissions.is_admin('admin_bad_init')
@message.delete_input
def init(update, context, unbad=False):
	try:
		# get group language from config
		lang = h_group.get_language(update)
		
		bot = context.bot

		db = sql.Database(update)
		message = update.message
		chat_id = message.chat_id
		
		if unbad == False:
			'''
			bad word (unbad = False)
			'''
			word = message.text[5:].lower()
			db.insert_badwords(word)
			output = bot.send_message(chat_id, lang.bad % word, parse_mode=ParseMode.HTML)
			db = sql.Database(update); db.insert_chatoperationslog("bad:%s" % word)
		else:
			'''
			unbad word (unbad = True)
			'''
			word = message.text[7:].lower()
			db.delete_badwords(word)
			output = bot.send_message(chat_id, lang.unbad % word, parse_mode=ParseMode.HTML)
			db = sql.Database(update); db.insert_chatoperationslog("unbad:%s" % word)
		return h_message.delete(output, context, 5)
	except Exception as e:
		logger.exception(e)


'''
Remove bad word for group
'''
@permissions.is_admin('admin_bad_unbad')
def unbad(update, context):
	return init(update, context, unbad=True)


'''
Show bad words list for group
'''
@permissions.is_admin('admin_bad_badlist')
def badlist(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)
		
		bot = context.bot
		
		message = update.message
		chat_id = message.chat_id
		bot.send_message(chat_id, lang.badlist, parse_mode=ParseMode.HTML)
	except Exception as e:
		logger.exception(e)