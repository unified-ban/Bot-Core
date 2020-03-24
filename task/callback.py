#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.helpers import h_group
from Utils.decorators import permissions, message
from Utils import logger, sql
from Core import admin, operator
from . import antiflood, welcome

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


def init(update, context):
	try:
		bot = context.bot
		
		admin.config.update(update, context)
		admin.feedback.update(update, context)
		operator.black.update(update, context)
		antiflood.update(update, context)
		welcome.update(update, context)
	except Exception as e:
		logger.exception(e)