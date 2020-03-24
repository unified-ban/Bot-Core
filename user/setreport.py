#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils import logger
from Utils.helpers import h_group
from telegram import ParseMode

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


def init(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot
		
		chat_id = update.message.chat_id
		return bot.send_message(chat_id, lang.reportchannel_start, parse_mode=ParseMode.HTML)
	except Exception as e:
		logger.exception(e)