#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message, chat
from Utils.helpers import h_user
from Utils import logger, sql
from telegram import ParseMode
import psutil, subprocess

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


'''
Force group registration
'''
@permissions.is_privileged_operator('operator_register_init')
@message.delete_input
@chat.only_groups
def init(update, context):
	try:
		bot = context.bot

		db = sql.Database(update); group = db.get_groups()
		
		if group is None:
			db = sql.Database(update); db.insert_groups()
			return logger.report(update, context, lang.report_registration % (
					update.message.chat.title,
					update.message.chat_id
				)
			)
	except Exception as e:
		logger.exception(e)