#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message
from Utils import logger, sql

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


'''
Start support session
'''
@permissions.is_operator('operator_startsupport_init')
@message.delete_input
def init(update, context):
	try:
		bot = context.bot

		db = sql.Database(update)
		db.insert_sessions()
		return logger.report(update, context, lang.report_startsession % (
				update.message.from_user.name,
				update.message.chat_id
			)
		)
	except Exception as e:
		logger.exception(e)


'''
Stop support session
'''
@permissions.is_operator('operator_stopsupport_init')
@message.delete_input
def stopsupport(update, context):
	try:
		db = sql.Database(update)
		db.update_sessions()
		return logger.report(update, context, lang.report_stopsession % (
				update.message.from_user.name,
				update.message.chat_id
			)
		)
	except Exception as e:
		logger.exception(e)