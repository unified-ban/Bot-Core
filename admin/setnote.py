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
Add note with hashtag for group
'''
@permissions.is_admin('admin_setnote_init')
@message.delete_input
def init(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot
		
		message = update.message
		text_list = str(message.text.lower()).split(" ")
		chat_id = message.chat_id
		
		if len(message.text.split(" ")) < 3 or not text_list[1].startswith("#"):
			'''
			The message does not respect the basic format
			output an error as message
			'''
			return bot.send_message(chat_id, lang.note_format_error, parse_mode=ParseMode.HTML)
		else:
			'''
			The message respects the basic format, inserts 
			it into the database, shows the success message 
			and logs the chat operation
			'''
			note = text_list[1]
			db = sql.Database(update); db.insert_notes(note, message.text[(10+len(note)):])
			output = bot.send_message(chat_id, lang.note_add % note, parse_mode=ParseMode.HTML)
			db = sql.Database(update); db.insert_chatoperationslog("note:%s" % note)
			return h_message.delete(output, context, 5)
		return False
	except Exception as e:
		logger.exception(e)


'''
Remove note for group
'''
@permissions.is_admin('admin_setnote_remove')
def removenote(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot
		
		message = update.message
		text_list = str(message.text.lower()).split(" ")
		chat_id = message.chat_id
		
		if len(message.text.split(" ")) > 2 or not text_list[1].startswith("#"):
			bot.send_message(chat_id, lang.note_format_error, parse_mode=ParseMode.HTML)
		else:
			note = text_list[1]
			db = sql.Database(update); db.delete_notes(note)
			output = bot.send_message(chat_id, lang.note_remove % note, parse_mode=ParseMode.HTML)
			db = sql.Database(update); db.insert_chatoperationslog("removenote:%s" % note)
		return h_message.delete(output, context, 5)
	except Exception as e:
		logger.exception(e)