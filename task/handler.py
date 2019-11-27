#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.helpers import h_group
from Utils.decorators import bypass
from Utils import logger, sql
from Core import admin, operator
from . import anticlone, antiflood, antiscam, antispam, blacklist, hammer, language, offensive, registration, reportchannel, support, welcome, notes

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language

@bypass.has_privileges
def load_tasks(update, context, group, lang):
	try:
		bot = context.bot

		language.init(update, context, group, lang)
		anticlone.init(update, context, group, lang)
		antiflood.init(update, context, group, lang)
		antiscam.init(update, context, group, lang)
		antispam.init(update, context, group, lang)
		blacklist.init(update, context, group, lang)
		hammer.init(update, context, group, lang)
		offensive.init(update, context, group, lang)
		welcome.init(update, context, group, lang)
	except Exception as e:
		logger.exception(e)
	
def init(update, context):
	try:
		bot = context.bot

		if update.edited_message is not None:
			update.message = update.edited_message
		db = sql.Database(update);group = db.get_groups()
		lang = h_group.get_language(update)
		
		if group is None:
			group = False
		
		registration.init(update, context, group, lang)
		notes.init(update, context)
		
		if group != False:
			reportchannel.init(update, context, lang)
			support.init(update, context, lang)
			
			load_tasks(update, context, group, lang)
	except Exception as e:
		logger.exception(e)