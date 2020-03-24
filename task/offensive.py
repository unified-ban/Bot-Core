#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.helpers import h_message, h_group
from Utils import logger, sql

def init(update, context, group, lang):
	try:
		bot = context.bot

		if group[5] == 1:
			if update.message.text is not None:
				db = sql.Database(update)
				
				for word in db.get_badwords():
					if word[0] in update.message.text.lower():
						h_message.delete(update, context)
						db = sql.Database(update); db.insert_blockedcontent("offensive:%s" % word[0])
						
						return logger.report(update, context, lang.report_bad % (
								update.message.chat.title,
								'Bad word',
								word[0],
								update.message.from_user.name,
								update.message.from_user.id
							)
						)
		else:
			return False
	except Exception as e:
		logger.exception(e)