#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message
from Utils import logger
from Utils.helpers import h_language, h_message
import html

def init(update, context, group, lang):
	try:
		bot = context.bot
		
		if group[11] == 1:
			if h_language.only_roman_chars(update.message.text) == False:
				h_message.delete(update, context)
				return logger.report(update, context, lang.report_nonwest % (
						update.message.chat.title,
						'Non West',
						html.escape(update.message.text),
						update.message.from_user.name,
						update.message.from_user.id
					)
				)
		else:
			return False
	except Exception as e:
		logger.exception(e)