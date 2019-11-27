#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from telegram import ParseMode
from Utils.decorators import permissions, message
from Utils.helpers import h_message, h_spam, h_group
from Utils import logger, sql
import re

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


'''
Add telegram link (channel/group) to 
the safe list for group
'''
@permissions.is_admin('admin_safe_init')
@message.delete_input
def init(update, context, unsafe=False):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot
		
		db = sql.Database(update)
		message = update.message
		chat_id = message.chat_id
		
		'''
		Find all @username in user message
		'''
		domains = re.findall(r'(?i)\@\w+', message.text)
		output_domains = []
		
		for domain in domains:
			output_domains.append(domain)
			if unsafe == False:
				'''
				safe word (unsafe = False)
				'''
				if h_spam.is_telegram_domain('https://t.me/'+domain[1:]):
					'''
					The provided @username is a valid Telegram link
					add to the group safelist
					'''
					db.insert_safenames(domain)
				else:
					'''
					The username provided is not a valid Telegram link
					output an error message
					'''
					output = bot.send_message(chat_id, lang.wrongsafe % domain, parse_mode=ParseMode.HTML)
					return False
			else:
				db.delete_safenames(domain)
		
		'''
		Based on the result, send the correct message
		to the group and log chat operation
		'''
		if unsafe == False:
			output = bot.send_message(chat_id, lang.safe % str(output_domains), parse_mode=ParseMode.HTML)
			db = sql.Database(update); db.insert_chatoperationslog("safe:%s" % output_domains)
		else:
			output = bot.send_message(chat_id, lang.unsafe % str(output_domains), parse_mode=ParseMode.HTML)
			db = sql.Database(update); db.insert_chatoperationslog("unsafe:%s" % output_domains)
		return h_message.delete(output, context, 5)
	except Exception as e:
		logger.exception(e)


'''
Remove safe telegram link for group
'''
@permissions.is_admin('admin_safe_unsafe')
def unsafe(update, context):
	bot = context.bot
	return init(update, context, unsafe=True)


'''
Show safe list for group
'''
@permissions.is_admin('admin_safe_safelist')
def safelist(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot
		
		message = update.message
		chat_id = message.chat_id
		bot.send_message(chat_id, lang.safelist, parse_mode=ParseMode.HTML)
	except Exception as e:
		logger.exception(e)