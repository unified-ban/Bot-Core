#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message
from Utils.helpers import h_group
from Utils import logger
from telegram import ParseMode
import psutil, subprocess

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


'''
Show server and bot status
'''
@permissions.is_privileged_operator('operator_status_init')
@message.delete_input
def init(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot

		ps = subprocess.check_output(['ps', '-A'])
		if str.encode('mysqld') in ps:
			status_mysql = lang.status_running
		else:
			status_mysql = lang.status_stopped
		status_cpu = psutil.cpu_percent()
		status_memory = psutil.virtual_memory()[2]
		
		status = lang.status.format(
			cpu = status_cpu,
			memory = status_memory,
			mysql = status_mysql
		)
		bot.send_message(update.message.chat.id, status, parse_mode=ParseMode.HTML)
	except Exception as e:
		logger.exception(e)