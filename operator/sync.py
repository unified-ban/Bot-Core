#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from telegram import ParseMode
from telegram.ext.dispatcher import run_async
from Utils.decorators import permissions, message
from Utils.helpers import h_group
from Utils import logger, blacklist

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


'''
Synchronize the chat with the blacklist
'''
@permissions.is_operator('operator_sync_init')
@message.delete_input
@run_async
def init(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot
		
		chat_id = update.message.chat_id
		counter = blacklist.sync(update, context)
		logger.report(update, context, lang.report_sync % (
				update.message.chat_id,
				counter
			)
		)
		return bot.send_message(chat_id, lang.sync % counter, parse_mode=ParseMode.HTML)
	except Exception as e:
		logger.exception(e)