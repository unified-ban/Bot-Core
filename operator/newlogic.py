#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message
from Utils import logger, sql
from telegram import ParseMode
import psutil, subprocess, re

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


'''
Create new spam logic
'''
@permissions.is_privileged_operator('operator_newlogic_init')
@message.delete_input
def init(bot, update):
	try:
		cmd = update.message.text[10:].split(" ")
		name = cmd[0]
		syntax = cmd[1]
		method = re.search('{(.*)}', syntax).group(1)
		params = syntax.replace("{"+method+"}", "")
		
		db = sql.Database(update)
		db.insert_spamlogics(name, method, params)
			
		return bot.send_message(update.message.chat.id, lang.spamlogic_created % (
			name, 
			syntax,
			method,
			params
		), parse_mode=ParseMode.HTML)
	except Exception as e:
		logger.exception(e)